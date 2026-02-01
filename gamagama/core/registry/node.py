from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from ..tree.node import Node
from ..tree.map_branch import MapBranch


# We alias Node here just to keep imports clean in other files if they use registry.node
# But GroupNode now inherits from MapBranch to get the dictionary behavior.

@dataclass
class CommandNode(Node):
    """Represents a leaf command (e.g., 'roll')."""
    handler: Callable = None
    arguments: List[Dict[str, Any]] = field(default_factory=list)

    def add_argument(self, *args, **kwargs):
        """Stores argument defs to be applied to argparse later."""
        self.arguments.append({"args": args, "kwargs": kwargs})


@dataclass
class GroupNode(MapBranch):
    """Represents a container (e.g., 'player')."""
    # MapBranch already defines 'children' and 'add_child'
    pass
