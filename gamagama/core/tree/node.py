from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False)
class Node:
    """Base class for all nodes in the tree."""
    name: str
    parent: Optional['Node'] = None
