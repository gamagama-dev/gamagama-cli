from ..base import CommandBase


class QuitCommand(CommandBase):
    """Exits the interactive session."""

    name = "quit"
    help = "Exits the interactive session."

    def setup(self, spec):
        pass

    def handle(self, args):
        """Signals the main loop to exit."""
        return False
