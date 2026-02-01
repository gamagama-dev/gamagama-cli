from ..tree import MapBranch, Leaf
from .node import CommandSpec


class ArgparseBuilder:
    def __init__(self, tree):
        self.tree = tree

    def build(self, root_parser):
        """Recursively adds subparsers to the root_parser."""
        self._build_group(self.tree.root, root_parser)

    def _build_group(self, branch, parser):
        # branch is expected to be a MapBranch
        if not isinstance(branch, MapBranch) or not branch.children:
            return

        # We use a unique dest for each level of nesting to avoid collisions
        # and to allow inspecting the full command path in args if needed.
        # Top level matches existing expectation of 'command_name'.
        dest_name = f"cmd_{branch.name}" if branch.name != "root" else "command_name"

        subparsers = parser.add_subparsers(dest=dest_name)

        for child in branch:
            if isinstance(child, MapBranch):
                # MapBranch doesn't store help text, so we generate a default.
                grp_parser = subparsers.add_parser(child.name, help=f"Group {child.name}")
                self._build_group(child, grp_parser)
            elif isinstance(child, Leaf):
                spec = child.data
                if isinstance(spec, CommandSpec):
                    cmd_parser = subparsers.add_parser(child.name, help=spec.help)
                    for arg in spec.arguments:
                        cmd_parser.add_argument(*arg['args'], **arg['kwargs'])
                    cmd_parser.set_defaults(func=spec.handler)
