from dataclasses import dataclass, field
from typing import List, Iterator, Optional, Any, TYPE_CHECKING
from .node import Node
from .branch import Branch

if TYPE_CHECKING:
    from .visitor import NodeVisitor


@dataclass(eq=False)
class SeqBranch(Branch):
    """A node with ordered children (List). Allows duplicates."""
    children: List[Node] = field(default_factory=list)

    def _add_child_impl(self, node: Node):
        self.children.append(node)

    def get_child(self, key: str) -> Optional[Node]:
        return None

    def __iter__(self) -> Iterator[Node]:
        return iter(self.children)

    def accept(self, visitor: 'NodeVisitor') -> Any:
        return visitor.visit_seq_branch(self)
