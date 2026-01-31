from ..base import CommandBase


class QuitCommand(CommandBase):
    """Exits the interactive session."""

    def register(self):
        """Registers the 'quit' command."""
        quit_parser = self.subparsers.add_parser(
            "quit", help="Exits the interactive session."
        )
        quit_parser.set_defaults(func=self.handle)

    def handle(self, args):
        """Signals the main loop to exit."""
        return False
