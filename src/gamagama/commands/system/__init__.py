from ..base import CommandBase
from gamagama.systems import SYSTEMS


class SystemCommand(CommandBase):
    """Manage the active game system."""

    name = "system"
    help = "Manage the active game system."
    description = "Allows viewing and changing the active game system for the current session."

    def setup(self, spec):
        spec.add_argument("action", choices=["show", "list", "set"], help="Action to perform")
        spec.add_argument("system_name", nargs="?", help="Name of the system to set (required for 'set')")

    def handle(self, args):
        session = getattr(args, "_session", None)
        if not session:
            print("Error: System command requires an active session.")
            return

        if args.action == "show":
            print(f"Current system: {session.system.name}")
        
        elif args.action == "list":
            print("Available systems:")
            for name in sorted(SYSTEMS.keys()):
                print(f" - {name}")

        elif args.action == "set":
            if not args.system_name:
                print("Error: Please specify a system name.")
                return
            
            sys_class = SYSTEMS.get(args.system_name)
            if not sys_class:
                print(f"Error: System '{args.system_name}' not found.")
                return
            
            session.system = sys_class()
            print(f"System changed to: {session.system.name}")
