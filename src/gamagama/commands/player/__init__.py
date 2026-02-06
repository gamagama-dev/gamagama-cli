from ..base import CommandBase


class PlayerLoadCommand(CommandBase):
    name = "load"
    help = "Load a character from disk."
    path = ["player"]

    def setup(self, spec):
        spec.add_argument("name", help="Name of the character to load")

    def handle(self, args):
        session = args._session
        name = args.name

        if name in session.players:
            print(f"Character '{name}' is already loaded.")
            return

        character = session.store.load(name)
        if character is not None:
            session.players[name] = character
            print(f"Loaded character: {character.name}")


class PlayerDropCommand(CommandBase):
    name = "drop"
    help = "Remove a loaded character from the session."
    path = ["player"]

    def setup(self, spec):
        spec.add_argument("name", help="Name of the character to drop")

    def handle(self, args):
        session = args._session
        name = args.name

        if name not in session.players:
            print(f"Character '{name}' is not loaded.")
            return

        del session.players[name]
        print(f"Dropped character: {name}")


class PlayerListCommand(CommandBase):
    name = "list"
    help = "List all loaded characters."
    path = ["player"]

    def setup(self, spec):
        pass

    def handle(self, args):
        session = args._session

        if not session.players:
            print("No characters loaded.")
            return

        print("Loaded characters:")
        for name in session.players:
            print(f"  {name}")


class PlayerShowCommand(CommandBase):
    name = "show"
    help = "Display a loaded character's attributes."
    path = ["player"]

    def setup(self, spec):
        spec.add_argument("name", help="Name of the character to show")

    def handle(self, args):
        session = args._session
        name = args.name

        if name not in session.players:
            print(f"Character '{name}' is not loaded.")
            return

        char = session.players[name]
        print(f"Name: {char.name}")
        print(f"System: {char.system}")

        if char.strings:
            print("Strings:")
            for key, value in char.strings.items():
                print(f"  {key}: {value}")

        if char.stats:
            print("Stats:")
            for key, value in char.stats.items():
                print(f"  {key}: {value}")

        if char.skills:
            print("Skills:")
            for key, value in char.skills.items():
                print(f"  {key}: {value}")

        if char.counts:
            print("Counts:")
            for key, (current, max_val) in char.counts.items():
                print(f"  {key}: {current}/{max_val}")
