from abc import ABC, abstractmethod
import random


class GameSystem(ABC):
    """Abstract base class for game-specific logic."""
    
    name = "generic"

    def roll_die(self, sides: int, explode: bool) -> int:
        """
        Rolls a single die. 
        Override this to implement system-specific mechanics (like Open-Ended rolls).
        """
        # Default generic behavior
        die_total = 0
        while True:
            roll = random.randint(1, sides)
            die_total += roll
            if not explode or roll != sides:
                break
        return die_total
