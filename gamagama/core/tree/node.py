from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    """Base class for all nodes in the tree."""
    name: str
    parent: Optional['Node'] = None
