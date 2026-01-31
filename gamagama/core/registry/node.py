from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable


@dataclass
class Node:
    name: str
    help: str
    parent: Optional['Node'] = None


@dataclass
class CommandNode(Node):
    """Represents a leaf command (e.g., 'roll')."""
    handler: Callable = None
    arguments: List[Dict[str, Any]] = field(default_factory=list)

    def add_argument(self, *args, **kwargs):
        """Stores argument defs to be applied to argparse later."""
        self.arguments.append({"args": args, "kwargs": kwargs})


@dataclass
class GroupNode(Node):
    """Represents a container (e.g., 'player')."""
    children: Dict[str, Node] = field(default_factory=dict)

    def add_child(self, node: Node):
        self.children[node.name] = node
        node.parent = self
