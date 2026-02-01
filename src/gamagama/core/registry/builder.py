import argparse
from ..tree import MapBranch, NodeVisitor
from .node import CommandSpec


class ArgparseBuilder(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.node_parsers = {}
        self.node_actions = {}

    def build(self, root_parser):
        """Builds the argparse tree using the CommandTree."""
        # Map: Node -> ArgumentParser
        self.node_parsers = {self.tree.root: root_parser}
        self.node_actions = {}

        # walk() guarantees parents are visited before children (Pre-Order)
        for node in self.tree.walk():
            if node is self.tree.root:
                continue
            # Dispatch using reflection (visit_MapBranch, visit_CommandSpec, etc.)
            self.visit(node)

    def _get_parent_action(self, node):
        """Helper to get or create the subparsers action for the parent node."""
        parent_node = node.parent
        parent_parser = self.node_parsers[parent_node]

        if parent_node not in self.node_actions:
            dest_name = f"cmd_{parent_node.name}" if parent_node.name != "root" else "command_name"
            # Set metavar to control help output (e.g. show 'command' instead of {list,of,cmds})
            metavar_text = "command" if parent_node.name == "root" else "subcommand"

            self.node_actions[parent_node] = parent_parser.add_subparsers(
                dest=dest_name,
                required=False,
                metavar=metavar_text
            )
        
        return self.node_actions[parent_node]

    def visit_MapBranch(self, node: MapBranch):
        parent_action = self._get_parent_action(node)
        grp_parser = parent_action.add_parser(node.name, help=f"Group {node.name}")
        self.node_parsers[node] = grp_parser

    def visit_CommandSpec(self, node: CommandSpec):
        parent_action = self._get_parent_action(node)
        cmd_parser = parent_action.add_parser(
            node.name,
            help=node.help,
            description=node.description,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        for arg in node.arguments:
            cmd_parser.add_argument(*arg['args'], **arg['kwargs'])
        cmd_parser.set_defaults(func=node.handler)
