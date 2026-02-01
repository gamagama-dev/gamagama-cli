import argparse
import readline
import shlex
import sys

from .. import commands
from .parsers import NoHelpArgumentParser
from .completer import Completer
from .registry import CommandTree, ArgparseBuilder


def run():
    """Main entry point for the gamagama CLI."""
    parser = argparse.ArgumentParser(
        prog="gg", description="A Game Master Game Manager for tabletop RPGs."
    )

    # Build the command tree
    tree = CommandTree()
    commands.discover_commands(tree)

    # Build argparse structure from tree
    builder = ArgparseBuilder(tree)
    builder.build(parser)

    # If command-line arguments are given, run in CLI mode and exit.
    cli_args = sys.argv[1:]
    if cli_args:
        args = parser.parse_args(cli_args)
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()  # Show help if no command was given
        return

    # Otherwise, start interactive mode.
    # TODO: Update Completer to use tree. For now, extract names from tree root.
    command_names = list(tree.root.children.keys())
    completer = Completer(command_names)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")

    print("Welcome to gamagama!")
    print("Type 'quit' to exit.")

    while True:
        try:
            line = input("gg> ")
            if not line.strip():
                continue

            command_parts = shlex.split(line)
            try:
                # Pass a namespace object to indicate interactive mode to handlers.
                ns = argparse.Namespace()
                setattr(ns, "_interactive", True)
                args = parser.parse_args(command_parts, namespace=ns)
                if hasattr(args, "func"):
                    if args.func(args) is False:
                        break
                else:
                    # User entered a command name without required arguments
                    parser.print_help()
            except SystemExit:
                # Argparse calls sys.exit() on --help. Catch it to keep the loop running.
                pass

        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break


if __name__ == "__main__":
    run()
