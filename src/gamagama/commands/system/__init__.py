from ..base import CommandBase
from gamagama.systems import SYSTEMS


class SystemShowCommand(CommandBase):
    name = "show"
    help = "Shows the current game system."
    path = ["system"]

    def setup(self, spec):
        pass

    def handle(self, args):
        session = getattr(args, "_session", None)
        if not session:
            print("Error: System command requires an active session.")
            return
        print(f"Current system: {session.system.name}")


class SystemListCommand(CommandBase):
    name = "list"
    help = "Lists available game systems."
    path = ["system"]

    def setup(self, spec):
        pass

    def handle(self, args):
        print("Available systems:")
        for name in sorted(SYSTEMS.keys()):
            print(f" - {name}")


class SystemSetCommand(CommandBase):
    name = "set"
    help = "Sets the active game system."
    path = ["system"]

    def setup(self, spec):
        spec.add_argument("system_name", help="Name of the system to set")

    def handle(self, args):
        session = getattr(args, "_session", None)
        if not session:
            print("Error: System command requires an active session.")
            return

        sys_class = SYSTEMS.get(args.system_name)
        if not sys_class:
            print(f"Error: System '{args.system_name}' not found.")
            return
        
        session.system = sys_class()
        print(f"System changed to: {session.system.name}")
