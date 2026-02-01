from dataclasses import dataclass
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .visitor import NodeVisitor


@dataclass(eq=False)
class Node:
    """Base class for all nodes in the tree."""
    name: str
    parent: Optional['Node'] = None

    def accept(self, visitor: 'NodeVisitor') -> Any:
        """Dispatches the visitor to the appropriate method."""
        return visitor.visit_node(self)
