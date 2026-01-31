from typing import List, Any, Optional
from .node import Branch, Leaf, Node


class Tree:
    """A generic hierarchical structure."""

    def __init__(self, root_name: str = "root"):
        self.root = Branch(name=root_name)

    def insert(self, path: List[str], data: Any) -> Leaf:
        """
        Inserts data at the specified path, creating Branches as needed.
        Returns the created Leaf.
        """
        current = self.root

        # Navigate or create branches for the path prefix
        for part in path[:-1]:
            if part not in current.children:
                new_branch = Branch(name=part)
                current.add_child(new_branch)

            current = current.children[part]
            if not isinstance(current, Branch):
                raise ValueError(f"Cannot traverse '{part}': it is a Leaf, not a Branch.")

        # Create and attach the final Leaf
        leaf_name = path[-1]
        leaf = Leaf(name=leaf_name, data=data)
        current.add_child(leaf)
        return leaf

    def get(self, path: List[str]) -> Optional[Node]:
        """Retrieves a Node at the specified path, or None."""
        current = self.root
        for part in path:
            if isinstance(current, Branch) and part in current.children:
                current = current.children[part]
            else:
                return None
        return current
