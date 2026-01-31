from .node import GroupNode, CommandNode


class ArgparseBuilder:
    def __init__(self, tree):
        self.tree = tree

    def build(self, root_parser):
        """Recursively adds subparsers to the root_parser."""
        self._build_group(self.tree.root, root_parser)

    def _build_group(self, group_node, parser):
        if not group_node.children:
            return

        # We use a unique dest for each level of nesting to avoid collisions
        # and to allow inspecting the full command path in args if needed.
        # Top level matches existing expectation of 'command_name'.
        dest_name = f"cmd_{group_node.name}" if group_node.name != "root" else "command_name"

        subparsers = parser.add_subparsers(dest=dest_name)

        for child in group_node.children.values():
            if isinstance(child, GroupNode):
                grp_parser = subparsers.add_parser(child.name, help=child.help)
                self._build_group(child, grp_parser)
            elif isinstance(child, CommandNode):
                cmd_parser = subparsers.add_parser(child.name, help=child.help)
                for arg in child.arguments:
                    cmd_parser.add_argument(*arg['args'], **arg['kwargs'])
                cmd_parser.set_defaults(func=child.handler)
