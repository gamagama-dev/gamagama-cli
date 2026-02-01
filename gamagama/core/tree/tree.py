from typing import List, Any, Optional, Iterator
from .node import Node
from .branch import Branch
from .map_branch import MapBranch
from .leaf import Leaf


class Tree:
    """A generic hierarchical structure."""

    def __init__(self, root_name: str = "root"):
        # The default Tree implementation uses a MapBranch (named nodes)
        self.root = MapBranch(name=root_name)

    def insert(self, path: List[str], data: Any) -> Leaf:
        """
        Inserts data at the specified path, creating MapBranches as needed.
        Returns the created Leaf.
        """
        current = self.root

        # Navigate or create branches for the path prefix
        for part in path[:-1]:
            if isinstance(current, MapBranch):
                if part not in current.children:
                    new_branch = MapBranch(name=part)
                    current.add_child(new_branch)
                current = current.children[part]
            else:
                # If we encounter a SeqBranch or Leaf while traversing a path, we can't proceed by name
                raise ValueError(f"Cannot traverse '{part}': current node is not a MapBranch.")

            if not isinstance(current, Branch):
                raise ValueError(f"Cannot traverse '{part}': it is a Leaf, not a Branch.")

        # Create and attach the final Leaf
        leaf_name = path[-1]
        
        # Check for existence if we are in a MapBranch
        if isinstance(current, MapBranch) and leaf_name in current.children:
             raise ValueError(f"Node '{leaf_name}' already exists.")

        leaf = Leaf(name=leaf_name, data=data)
        current.add_child(leaf)
        return leaf

    def get(self, path: List[str]) -> Optional[Node]:
        """Retrieves a Node at the specified path, or None."""
        current = self.root
        for part in path:
            if isinstance(current, MapBranch) and part in current.children:
                current = current.children[part]
            else:
                return None
        return current

    def walk(self, start_node: Node = None) -> Iterator[Node]:
        """
        Yields nodes in the subtree starting at start_node (default: root).
        Traversal is Depth-First Pre-Order, respecting insertion order.
        """
        node = start_node or self.root
        yield node

        if isinstance(node, Branch):
            for child in node:
                yield from self.walk(child)
