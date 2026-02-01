from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class Node:
    """Base class for all nodes in the tree."""
    name: str
    parent: Optional['Node'] = None


@dataclass
class Branch(Node):
    """A node that can contain other nodes."""
    children: Dict[str, Node] = field(default_factory=dict)

    def add_child(self, node: Node):
        if node.parent is not None:
            raise ValueError(f"Node '{node.name}' already has a parent: '{node.parent.name}'.")
        self.children[node.name] = node
        node.parent = self


@dataclass
class Leaf(Node):
    """A terminal node that holds data."""
    data: Any = None
