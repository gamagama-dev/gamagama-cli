from ..base import CommandBase
from gamagama.core.tree import NodeVisitor, MapBranch
from gamagama.core.registry import CommandSpec


class HelpDescriptionVisitor(NodeVisitor):
    """Visitor to extract a one-line description for a node."""

    def visit_CommandSpec(self, node):
        return node.help

    def visit_MapBranch(self, node):
        return f"{node.name.capitalize()} subcommands"


class HelpPrinterVisitor(NodeVisitor):
    """Visitor to print the full help output for a node."""

    def __init__(self, path):
        self.path = path
        self.path_str = " ".join(path)

    def visit_CommandSpec(self, node):
        print(f"Help for '{self.path_str}':")
        print(f"  {node.help}")

    def visit_MapBranch(self, node):
        header = f"Available commands in '{node.name}':" if node.name != "root" else "Available commands:"
        print(header)
        self._print_tree(node, indent=2)

    def _print_tree(self, branch, indent):
        children = list(branch)
        if not children:
            return

        # Calculate padding for this specific level
        max_len = max(len(c.name) for c in children)
        desc_visitor = HelpDescriptionVisitor()

        for child in sorted(children, key=lambda x: x.name):
            description = desc_visitor.visit(child)
            prefix = " " * indent
            
            # Print the current node (Command or Branch)
            print(f"{prefix}{child.name:<{max_len + 2}}{description}")

            # If it's a branch, recurse immediately to show its children
            if isinstance(child, MapBranch):
                self._print_tree(child, indent + 2)

    def generic_visit(self, node):
        print(f"Node '{self.path_str}' is not a command or group.")


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

        node = self.tree.get(path)

        if not node:
            print(f"Unknown command: '{' '.join(path)}'")
            return

        visitor = HelpPrinterVisitor(path)
        visitor.visit(node)
