from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Iterator


@dataclass
class Node:
    """Base class for all nodes in the tree."""
    name: str
    parent: Optional['Node'] = None


@dataclass
class Branch(Node):
    """Abstract base for nodes that contain children."""

    def add_child(self, node: Node):
        """Adds a child node, enforcing single-parent rules."""
        if node.parent is not None:
            raise ValueError(f"Node '{node.name}' already has a parent: '{node.parent.name}'.")
        self._add_child_impl(node)
        node.parent = self

    def _add_child_impl(self, node: Node):
        """Subclasses implement specific storage logic."""
        raise NotImplementedError

    def __iter__(self) -> Iterator[Node]:
        """Subclasses must yield children."""
        raise NotImplementedError


@dataclass
class MapBranch(Branch):
    """A node with named children (Dict). Enforces unique names."""
    children: Dict[str, Node] = field(default_factory=dict)

    def _add_child_impl(self, node: Node):
        if node.name in self.children:
            raise ValueError(f"Node '{node.name}' already exists.")
        self.children[node.name] = node

    def __iter__(self) -> Iterator[Node]:
        return iter(self.children.values())


@dataclass
class SeqBranch(Branch):
    """A node with ordered children (List). Allows duplicates."""
    children: List[Node] = field(default_factory=list)

    def _add_child_impl(self, node: Node):
        self.children.append(node)

    def __iter__(self) -> Iterator[Node]:
        return iter(self.children)


@dataclass
class Leaf(Node):
    """A terminal node that holds data."""
    data: Any = None
