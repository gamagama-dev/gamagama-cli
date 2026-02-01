from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable
from ..tree.node import Node


@dataclass(eq=False)
class CommandSpec(Node):
    """Payload for a command leaf, defining its handler and arguments."""
    handler: Callable = None
    arguments: List[Dict[str, Any]] = field(default_factory=list)
    help: str = ""

    def add_argument(self, *args, **kwargs):
        """Stores argument defs to be applied to argparse later."""
        self.arguments.append({"args": args, "kwargs": kwargs})
