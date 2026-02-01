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


def run():
    """Main entry point for the gamagama CLI."""
    # Build the command tree
    tree = CommandTree()
    commands.discover_commands(tree)

    # If command-line arguments are given, run in CLI mode and exit.
    if len(sys.argv) > 1:
        run_cli_mode(tree)
    else:
        run_interactive_mode(tree)


def run_cli_mode(tree):
    """Runs the application in stateless CLI mode using argparse."""
    parser = argparse.ArgumentParser(
        prog="gg",
        description="A Game Master Game Manager for tabletop RPGs.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Build argparse structure from tree
    builder = ArgparseBuilder(tree)
    builder.build(parser)

    cli_args = sys.argv[1:]
    args = parser.parse_args(cli_args)
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def run_interactive_mode(tree):
    """Runs the application in stateful interactive mode."""
    session = Session(tree)
    
    # TODO: Update Completer to be session-aware
    completer = Completer(tree)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")

    print("Welcome to gamagama!")
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
            cmd_name = parts[0]
            cmd_args = parts[1:]

            # Resolve command
            node = _resolve_node(session.current_node, cmd_name)

            if not node:
                print(f"Command not found: {cmd_name}")
                continue

            if isinstance(node, Branch):
                # Navigation: Enter the branch
                session.current_node = node
                continue

            if isinstance(node, CommandSpec):
                _execute_command(node, cmd_args, session)
                continue
            
            print(f"Node '{node.name}' is not executable.")

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
