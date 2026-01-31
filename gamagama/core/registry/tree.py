from .node import GroupNode, CommandNode, Node


class CommandTree:
    def __init__(self):
        self.root = GroupNode(name="root", help="Root")

    def register_at_path(self, path_parts: list, node: Node):
        """
        Registers a node at a specific path in the tree.
        path_parts: e.g. ['player', 'create']
        """
        current = self.root

        # Navigate/Create groups for all parts except the last one
        for part in path_parts[:-1]:
            if part not in current.children:
                # Create intermediate group
                new_group = GroupNode(name=part, help=f"Group {part}")
                current.add_child(new_group)

            current = current.children[part]
            if not isinstance(current, GroupNode):
                raise ValueError(f"Cannot register child under non-group node '{part}'")

        # Add the final node
        # Ensure the node name matches the path
        node.name = path_parts[-1]
        current.add_child(node)

    def get_node(self, path_parts: list) -> Node:
        current = self.root
        for part in path_parts:
            if isinstance(current, GroupNode) and part in current.children:
                current = current.children[part]
            else:
                return None
        return current
