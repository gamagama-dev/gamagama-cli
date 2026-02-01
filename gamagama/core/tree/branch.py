from dataclasses import dataclass
from typing import Iterator, Optional
from .node import Node


@dataclass(eq=False)
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

    def get_child(self, key: str) -> Optional[Node]:
        """Retrieves a child node by key, if supported."""
        return None

    def __iter__(self) -> Iterator[Node]:
        """Subclasses must yield children."""
        raise NotImplementedError
