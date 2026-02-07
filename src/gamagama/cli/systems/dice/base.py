from abc import ABC
import random


class DiceEngine(ABC):
    """Handles dice mechanics."""
    
    def roll(self, sides: int, explode: bool) -> int:
        """Standard rolling logic."""
        die_total = 0
        while True:
            roll = random.randint(1, sides)
            die_total += roll
            if not explode or roll != sides:
                break
        return die_total

    @property
    def help_text(self) -> str:
        """Returns system-specific help text for dice mechanics."""
        return ""
