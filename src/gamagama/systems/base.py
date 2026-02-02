from abc import ABC
from .dice import DiceEngine


class GameSystem(ABC):
    """Abstract base class for game-specific logic."""
    
    name = "generic"

    def __init__(self):
        self.dice = DiceEngine()
