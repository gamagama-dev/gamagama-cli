from dataclasses import dataclass, field
from typing import Dict, Iterator, Optional
from .node import Node
from .branch import Branch


@dataclass(eq=False)
class MapBranch(Branch):
    """A node with named children (Dict). Enforces unique names."""
    children: Dict[str, Node] = field(default_factory=dict)

    def _add_child_impl(self, node: Node):
        if node.name in self.children:
            raise ValueError(f"Node '{node.name}' already exists.")
        self.children[node.name] = node

    def get_child(self, key: str) -> Optional[Node]:
        return self.children.get(key)

    def __iter__(self) -> Iterator[Node]:
        return iter(self.children.values())
