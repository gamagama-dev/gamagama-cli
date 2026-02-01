from ..base import CommandBase
from gamagama.core.tree import MapBranch
from gamagama.core.registry import CommandSpec


class HelpCommand(CommandBase):
    """Shows a list of all available commands or help for a specific command."""

    name = "help"
    help = "Shows help for a specific command."

    def __init__(self):
        self.tree = None  # Injected by loader

    def setup(self, spec):
        spec.add_argument(
            "command_name", nargs="*", help="The command path to get help for."
        )

    def handle(self, args):
        """Prints help for a specific command or a list of all commands."""
        path = args.command_name if args.command_name else []

        if not path:
            self._print_group_help(self.tree.root)
            return

        node = self.tree.get(path)

        if not node:
            print(f"Unknown command: '{' '.join(path)}'")
            return

        if isinstance(node, CommandSpec):
            spec = node
            print(f"Help for '{' '.join(path)}':")
            print(f"  {spec.help}")
        elif isinstance(node, MapBranch):
            self._print_group_help(node)
        else:
            # Should not happen in standard usage
            print(f"Node '{' '.join(path)}' is not a command or group.")

    def _print_group_help(self, branch):
        header = f"Available commands in '{branch.name}':" if branch.name != "root" else "Available commands:"
        print(header)

        if not branch.children:
            return

        commands = []
        for child in branch:
            if isinstance(child, CommandSpec):
                commands.append((child.name, child.help))
            elif isinstance(child, MapBranch):
                commands.append((child.name, f"Group {child.name}"))

        if not commands:
            return

        max_len = max(len(name) for name, _ in commands)

        for name, help_text in sorted(commands, key=lambda x: x[0]):
            print(f"  {name:<{max_len + 2}}{help_text}")
