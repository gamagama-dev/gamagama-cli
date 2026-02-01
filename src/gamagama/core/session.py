from dataclasses import dataclass, field
from gamagama.core.registry import CommandTree
from gamagama.core.tree import Node


@dataclass
class Session:
    """Holds the state of an interactive session."""
    tree: CommandTree
    current_node: Node = field(init=False)
    should_exit: bool = False

    def __post_init__(self):
        self.current_node = self.tree.root
