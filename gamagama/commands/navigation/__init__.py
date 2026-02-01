from ..base import CommandBase


class UpCommand(CommandBase):
    """Moves the interactive session up one level."""

    name = ".."
    help = "Moves the interactive session up one level."

    def setup(self, spec):
        pass

    def handle(self, args):
        session = getattr(args, "_session", None)
        if not session:
            print("Error: Navigation commands only work in interactive mode.")
            return

        if session.current_node.parent:
            session.current_node = session.current_node.parent


class RootCommand(CommandBase):
    """Moves the interactive session to the root."""

    name = "/"
    help = "Moves the interactive session to the root."

    def setup(self, spec):
        pass

    def handle(self, args):
        session = getattr(args, "_session", None)
        if not session:
            print("Error: Navigation commands only work in interactive mode.")
            return

        session.current_node = session.tree.root
