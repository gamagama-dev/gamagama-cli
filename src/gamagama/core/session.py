from dataclasses import dataclass, field
from typing import Dict, Optional

from gamagama.characters import Character, CharacterStore
from gamagama.core.registry import CommandTree
from gamagama.core.tree import Node
from gamagama.systems import GameSystem, RolemasterSystem, GenericSystem


@dataclass
class Session:
    """Holds the state of an interactive session."""
    tree: CommandTree
    current_node: Node = field(init=False)
    should_exit: bool = False
    system: GameSystem = field(default_factory=GenericSystem)
    store: CharacterStore = field(default_factory=CharacterStore)
    players: Dict[str, Character] = field(default_factory=dict)
    active_player: Optional[str] = None
    active_schema: Optional[str] = None

    def __post_init__(self):
        self.current_node = self.tree.root
