from ..base import CommandBase
from gamagama.core.tree import MapBranch, Leaf
from gamagama.core.registry import CommandSpec


class HelpCommand(CommandBase):
    """Shows a list of all available commands or help for a specific command."""

    name = "help"
    help = "Shows help for a specific command."

    def __init__(self):
        self.tree = None  # Injected by loader

    def setup(self, spec):
        spec.add_argument(
            "command_name", nargs="?", help="The command to get help for."
        )

    def handle(self, args):
        """Prints help for a specific command or a list of all commands."""
        if args.command_name:
            # Find the node in the tree
            node = self.tree.get([args.command_name])

            if node and isinstance(node, Leaf) and isinstance(node.data, CommandSpec):
                spec = node.data
                print(f"Help for '{args.command_name}':")
                print(f"  {spec.help}")
            else:
                print(f"Unknown command: '{args.command_name}'")
            return

        print("Available commands:")
        if not self.tree.root.children:
            return

        commands = []
        for child in self.tree.root:
            if isinstance(child, Leaf) and isinstance(child.data, CommandSpec):
                commands.append((child.name, child.data.help))
            elif isinstance(child, MapBranch):
                commands.append((child.name, f"Group {child.name}"))

        if not commands:
            return

        max_len = max(len(name) for name, _ in commands)

        for name, help_text in sorted(commands, key=lambda x: x[0]):
            print(f"  {name:<{max_len + 2}}{help_text}")
