from ..tree import MapBranch
from .node import CommandSpec


class ArgparseBuilder:
    def __init__(self, tree):
        self.tree = tree

    def build(self, root_parser):
        """Builds the argparse tree using the CommandTree."""
        # Map: Node -> ArgumentParser
        # We start knowing the root node maps to the root_parser passed in.
        node_parsers = {self.tree.root: root_parser}

        # Map: Node -> SubparsersAction (The object returned by add_subparsers)
        # We need this because we add parsers to the 'action', not the parser itself.
        node_actions = {}

        # walk() guarantees parents are visited before children (Pre-Order)
        for node in self.tree.walk():
            if node is self.tree.root:
                continue

            parent_node = node.parent
            parent_parser = node_parsers[parent_node]

            # Ensure parent has a subparsers action
            if parent_node not in node_actions:
                dest_name = f"cmd_{parent_node.name}" if parent_node.name != "root" else "command_name"
                node_actions[parent_node] = parent_parser.add_subparsers(dest=dest_name)

            parent_action = node_actions[parent_node]

            if isinstance(node, MapBranch):
                # Create parser for the group
                grp_parser = parent_action.add_parser(node.name, help=f"Group {node.name}")
                node_parsers[node] = grp_parser

            elif isinstance(node, CommandSpec):
                spec = node
                cmd_parser = parent_action.add_parser(node.name, help=spec.help)
                for arg in spec.arguments:
                    cmd_parser.add_argument(*arg['args'], **arg['kwargs'])
                cmd_parser.set_defaults(func=spec.handler)
