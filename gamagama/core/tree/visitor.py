from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node
    from .map_branch import MapBranch
    from .seq_branch import SeqBranch
    from .leaf import Leaf


class NodeVisitor:
    """
    Abstract base class for Visitors.
    """

    def visit(self, node: 'Node') -> Any:
        """Entry point for visiting a node."""
        return node.accept(self)

    def visit_map_branch(self, node: 'MapBranch') -> Any:
        """Handle a MapBranch."""
        return self.visit_node(node)

    def visit_seq_branch(self, node: 'SeqBranch') -> Any:
        """Handle a SeqBranch."""
        return self.visit_node(node)

    def visit_leaf(self, node: 'Leaf') -> Any:
        """Handle a Leaf."""
        return self.visit_node(node)

    def visit_node(self, node: 'Node') -> Any:
        """Fallback for unknown node types."""
        return None
