from dataclasses import dataclass
from typing import Any, TYPE_CHECKING
from .node import Node

if TYPE_CHECKING:
    from .visitor import NodeVisitor


@dataclass(eq=False)
class Leaf(Node):
    """A terminal node that holds data."""
    data: Any = None

    def accept(self, visitor: 'NodeVisitor') -> Any:
        return visitor.visit_leaf(self)
