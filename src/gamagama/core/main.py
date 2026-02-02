import argparse
import readline
import shlex
import sys

from .. import commands
from .parsers import NoHelpArgumentParser
from .completer import Completer
from .registry import CommandTree, ArgparseBuilder, CommandSpec
from .tree import Branch
from .session import Session
from .config import load_config
from gamagama.systems import SYSTEMS, RolemasterSystem


def run():
    """Main entry point for the gamagama CLI."""
    # 1. Load Config
    config = load_config()
    config_system = config.get("core", {}).get("system")

    # 2. Parse global options (like --system) first
    parser = argparse.ArgumentParser(add_help=False)
    
    system_choices = sorted(SYSTEMS.keys())
    parser.add_argument(
        "--system", 
        choices=system_choices,
        help="The game system to use."
    )
    
    # parse_known_args returns the parsed args and the 'rest' of the list
    args, remaining_args = parser.parse_known_args()

    # 3. Determine the System
    # Priority: CLI Arg > Config > Default
    system_name = args.system or config_system or "rolemaster"

    if system_name in SYSTEMS:
        system_class = SYSTEMS[system_name]
    else:
        print(f"Error: System '{system_name}' not found. Available: {', '.join(system_choices)}")
        sys.exit(1)

    # 4. Build the command tree
    tree = CommandTree()
    commands.discover_commands(tree)

    # 5. Decide Mode based on whether there are remaining arguments
    if remaining_args:
        run_cli_mode(tree, system_class, remaining_args)
    else:
        run_interactive_mode(tree, system_class)


def run_cli_mode(tree, system_class, cli_args):
    """Runs the application in stateless CLI mode using argparse."""
    parser = argparse.ArgumentParser(
        prog="gg",
        description="A Game Master Game Manager for tabletop RPGs.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Re-add system arg so it shows in help, even though we handled it
    system_choices = sorted(SYSTEMS.keys())
    parser.add_argument(
        "--system", 
        choices=system_choices,
        help="The game system to use."
    )

    # Build argparse structure from tree
    builder = ArgparseBuilder(tree)
    builder.build(parser)

    args = parser.parse_args(cli_args)
    
    if hasattr(args, "func"):
        # Create a transient session for this command execution
        session = Session(tree, system=system_class())
        setattr(args, "_session", session)
        setattr(args, "_interactive", False)

        args.func(args)
    else:
        parser.print_help()


def run_interactive_mode(tree, system_class):
    """Runs the application in stateful interactive mode."""
    session = Session(tree, system=system_class())
    
    completer = Completer(tree, session)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")

    print(f"Welcome to gamagama! (System: {session.system.name})")
    print("Type 'quit' to exit.")

    while not session.should_exit:
        try:
            # Build prompt based on current path
            prompt_path = _build_prompt_path(session.current_node)
            prompt = f"gg{prompt_path}> "
            
            line = input(prompt)
            if not line.strip():
                continue

            parts = shlex.split(line)
            if not parts:
                continue

            # 1. Resolve the first part (bubbling lookup)
            first_node = _resolve_node(session.current_node, parts[0])
            
            if not first_node:
                print(f"Command not found: {parts[0]}")
                continue

            # 2. Walk down the tree with the remaining parts (strict lookup)
            curr_node = first_node
            remaining_args = parts[1:]
            
            while remaining_args and isinstance(curr_node, Branch):
                next_child = curr_node.get_child(remaining_args[0])
                if next_child:
                    curr_node = next_child
                    remaining_args.pop(0)
                else:
                    # Next arg is not a child, so stop walking.
                    break
            
            # 3. Execute or Navigate
            if isinstance(curr_node, Branch):
                if remaining_args:
                    # We ended at a branch but still have args that didn't match children.
                    # e.g. "system invalid_cmd"
                    print(f"Command not found: {remaining_args[0]}")
                    continue
                
                # Navigation: Enter the branch
                session.current_node = curr_node
                continue

            if isinstance(curr_node, CommandSpec):
                _execute_command(curr_node, remaining_args, session)
                continue
            
            print(f"Node '{curr_node.name}' is not executable.")

        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break


def _build_prompt_path(node):
    if node.name == "root":
        return ""
    
    names = []
    curr = node
    while curr and curr.name != "root":
        names.append(curr.name)
        curr = curr.parent
    
    return "/" + "/".join(reversed(names))


def _resolve_node(start_node, name):
    """Bubbles up from start_node to find a child with the given name."""
    curr = start_node
    while curr:
        if isinstance(curr, Branch):
            child = curr.get_child(name)
            if child:
                return child
        curr = curr.parent
    return None


def _execute_command(spec, args_list, session):
    """Builds a temporary parser for the command and executes it."""
    parser = argparse.ArgumentParser(
        prog=spec.name,
        description=spec.help
    )
    
    for arg in spec.arguments:
        parser.add_argument(*arg['args'], **arg['kwargs'])

    try:
        # Parse args
        args = parser.parse_args(args_list)
    except SystemExit:
        # argparse prints help and exits. We catch it to stay in the loop.
        return

    # Inject session
    setattr(args, "_session", session)
    setattr(args, "_interactive", True)

    # Execute
    if spec.handler:
        result = spec.handler(args)
        if result is False:
            session.should_exit = True


if __name__ == "__main__":
    run()
