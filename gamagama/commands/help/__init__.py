from ..base import CommandBase


class HelpCommand(CommandBase):
    """Shows a list of all available commands or help for a specific command."""

    def register(self):
        """Registers the 'help' command."""
        help_parser = self.subparsers.add_parser(
            "help", help="Shows help for a specific command."
        )
        help_parser.add_argument(
            "command_name", nargs="?", help="The command to get help for."
        )
        help_parser.set_defaults(func=self.handle)

    def handle(self, args):
        """Prints help for a specific command or a list of all commands."""
        if args.command_name:
            if args.command_name in self.subparsers.choices:
                subparser = self.subparsers.choices[args.command_name]
                if getattr(args, "_interactive", False):
                    help_text = subparser.format_help()
                    # To avoid modifying the shared parser state, we get the help text
                    # as a string and replace the usage line's program name.
                    usage_line = f"usage: {subparser.prog}"
                    interactive_usage_line = f"usage: {args.command_name}"
                    print(help_text.replace(usage_line, interactive_usage_line, 1))
                else:
                    subparser.print_help()
            else:
                print(f"Unknown command: '{args.command_name}'")
            return

        print("Available commands:")
        commands = [action for action in self.subparsers._choices_actions]
        if not commands:
            return

        max_len = max(len(cmd.dest) for cmd in commands)

        for cmd in sorted(commands, key=lambda x: x.dest):
            print(f"  {cmd.dest:<{max_len + 2}}{cmd.help}")
