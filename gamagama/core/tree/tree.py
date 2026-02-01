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

    def insert(self, path: List[str], data: Any) -> Node:
        """
        Inserts data at the specified path, creating MapBranches as needed.
        If 'data' is already a Node, it is attached directly.
        Otherwise, it is wrapped in a Leaf.
        Returns the inserted Node.
        """
        current = self.root

        # Navigate or create branches for the path prefix
        for part in path[:-1]:
            if isinstance(current, MapBranch):
                child = current.get_child(part)
                if not child:
                    new_branch = MapBranch(name=part)
                    current.add_child(new_branch)
                    current = new_branch
                else:
                    current = child
            else:
                # If we encounter a SeqBranch or Leaf while traversing a path, we can't proceed by name
                raise ValueError(f"Cannot traverse '{part}': current node is not a MapBranch.")

            if not isinstance(current, Branch):
                raise ValueError(f"Cannot traverse '{part}': it is a Leaf, not a Branch.")

        # Create and attach the final Node
        leaf_name = path[-1]

        # Ensure the final container is a MapBranch
        if not isinstance(current, MapBranch):
             raise ValueError(f"Cannot insert '{leaf_name}': current node is not a MapBranch.")

        # Check for existence if we are in a MapBranch
        if current.get_child(leaf_name):
             raise ValueError(f"Node '{leaf_name}' already exists.")

        if isinstance(data, Node):
            node = data
            node.name = leaf_name
        else:
            node = Leaf(name=leaf_name, data=data)

        current.add_child(node)
        return node

    def get(self, path: List[str]) -> Optional[Node]:
        """Retrieves a Node at the specified path, or None."""
        current = self.root
        for part in path:
            if isinstance(current, Branch):
                current = current.get_child(part)
                if current is None:
                    return None
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
