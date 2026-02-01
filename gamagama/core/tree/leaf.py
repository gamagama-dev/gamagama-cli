from dataclasses import dataclass
from typing import Any
from .node import Node


@dataclass
class Leaf(Node):
    """A terminal node that holds data."""
    data: Any = None
