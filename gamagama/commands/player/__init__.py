from ..base import CommandBase


class PlayerAddCommand(CommandBase):
    name = "add"
    help = "Adds a new player."
    path = ["player"]

    def setup(self, spec):
        spec.add_argument("name", help="Name of the player to add")

    def handle(self, args):
        print(f"Adding player: {args.name}")


class PlayerRemoveCommand(CommandBase):
    name = "remove"
    help = "Removes an existing player."
    path = ["player"]

    def setup(self, spec):
        spec.add_argument("name", help="Name of the player to remove")

    def handle(self, args):
        print(f"Removing player: {args.name}")


class PlayerListCommand(CommandBase):
    name = "list"
    help = "Lists all players."
    path = ["player"]

    def setup(self, spec):
        pass

    def handle(self, args):
        print("Listing players... (TODO)")
