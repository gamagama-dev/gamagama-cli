import argparse
import readline
import shlex
import sys

from . import commands
from .commands.base import NoHelpArgumentParser


class Completer:
    """A completer for readline."""

    def __init__(self, commands):
        self.commands = commands

    def complete(self, text, state):
        """Returns the next possible completion for 'text'."""
        line = readline.get_line_buffer().split()
        # Only complete the first word
        if len(line) > 1 and line[0] in self.commands:
            return None

        options = [cmd for cmd in self.commands if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        return None


def run():
    """Main entry point for the gamagama CLI."""
    parser = argparse.ArgumentParser(
        prog="gg", description="A Game Master Game Manager for tabletop RPGs."
    )
    subparsers = parser.add_subparsers(
        title="Commands", dest="command_name", parser_class=NoHelpArgumentParser
    )

    commands.discover_and_register_commands(parser, subparsers)

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
    command_names = list(subparsers.choices.keys())
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
                    if args.command_name:
                        subparsers.choices[args.command_name].print_help()
                    else:
                        parser.print_help()
            except SystemExit:
                # Argparse calls sys.exit() on --help. Catch it to keep the loop running.
                pass

        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break


if __name__ == "__main__":
    run()
