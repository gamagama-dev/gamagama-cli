from ..base import CommandBase


class HelpCommand(CommandBase):
    """Shows a list of all available commands."""

    def register(self):
        """Registers the 'help' command."""
        help_parser = self.subparsers.add_parser(
            "help", help="Shows a list of all available commands."
        )
        help_parser.set_defaults(func=self.handle)

    def handle(self, args):
        """Prints a formatted list of all registered commands and their help text."""
        print("Available commands:")

        commands = [action for action in self.subparsers._choices_actions]
        if not commands:
            return

        max_len = max(len(cmd.dest) for cmd in commands)

        for cmd in sorted(commands, key=lambda x: x.dest):
            print(f"  {cmd.dest:<{max_len + 2}}{cmd.help}")
