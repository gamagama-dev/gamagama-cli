from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node


class NodeVisitor:
    """
    A generic Visitor class that uses reflection to dispatch methods.
    
    It looks for a method named 'visit_ClassName' (e.g., 'visit_MapBranch').
    If not found, it calls 'generic_visit'.
    """

    def visit(self, node: 'Node') -> Any:
        """Visit a node."""
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: 'Node') -> Any:
        """Called if no explicit visitor function exists for a node."""
        # Default behavior: do nothing or raise error depending on preference.
        # Here we return None to be safe.
        return None
