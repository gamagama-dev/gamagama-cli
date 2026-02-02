import random
from .base import GameSystem


class RolemasterSystem(GameSystem):
    name = "rolemaster"

    def roll_die(self, sides: int, explode: bool) -> int:
        # Only d100 explodes specially in RM. 
        # Other dice (like 1d10 initiative) behave normally or standard explode.
        if sides == 100 and explode:
            return self._roll_open_ended()
        
        return super().roll_die(sides, explode)

    def _roll_open_ended(self) -> int:
        first_roll = random.randint(1, 100)

        if first_roll >= 96:
            # Explode Up
            current_total = first_roll
            last_roll = first_roll
            while last_roll >= 96:
                last_roll = random.randint(1, 100)
                current_total += last_roll
            return current_total

        elif first_roll <= 5:
            # Explode Down
            subtract_total = 0
            last_sub_roll = 100
            while last_sub_roll >= 96:
                last_sub_roll = random.randint(1, 100)
                subtract_total += last_sub_roll
            
            return first_roll - subtract_total

        else:
            return first_roll
