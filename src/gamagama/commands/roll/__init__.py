import random
import re

from ..base import CommandBase


class RollCommand(CommandBase):
    """Rolls dice based on one or more specifications."""

    name = "roll"
    help = "Rolls dice based on one or more specifications."
    description = """
Rolls dice based on one or more specifications.

Syntax: [count]d[sides][!][modifier]

Examples:
  3d6      - Roll 3 six-sided dice
  d20      - Roll 1 twenty-sided die
  3d6!     - Roll 3d6, rerolling max values (exploding)
  1d20+5   - Roll 1d20 and add 5
  2d8-2    - Roll 2d8 and subtract 2
  d%       - Roll a percentile die (1-100)
  d%!      - Rolemaster Open-Ended (Explodes up on 96-100, down on 1-5)
"""

    def setup(self, spec):
        spec.add_argument(
            "dice_spec",
            nargs="+",
            help="One or more dice specifications (e.g., '3d6', '1d20+5').",
        )

    def handle(self, args):
        """Handler for the 'roll' command."""
        for spec in args.dice_spec:
            print(self._roll_dice(spec))

    def _roll_dice(self, spec):
        """Parses a single dice spec (e.g., '3d6!+5') and returns the roll result."""
        match = re.match(r"^(\d*)d(\d+|%)(!?)([+-]\d+)?$", spec, re.IGNORECASE)
        if not match:
            return f"{spec}: Invalid dice specification."

        num_dice_str, sides_str, explode_str, modifier_str = match.groups()

        num_dice = int(num_dice_str) if num_dice_str else 1
        sides = 100 if sides_str == "%" else int(sides_str)
        should_explode = bool(explode_str)
        modifier = int(modifier_str) if modifier_str else 0

        if sides == 0:
            return f"{spec}: Cannot roll a 0-sided die."

        if sides == 1 and should_explode:
            return f"{spec}: Cannot explode a 1-sided die (infinite loop)."

        rolls = []
        for _ in range(num_dice):
            if sides == 100 and should_explode:
                rolls.append(self._roll_rolemaster_die())
            else:
                rolls.append(self._roll_standard_die(sides, should_explode))

        total = sum(rolls) + modifier

        return f"{spec}: {total} {rolls}"

    def _roll_standard_die(self, sides, should_explode):
        """Standard die roll with optional max-value explosion."""
        die_total = 0
        while True:
            roll = random.randint(1, sides)
            die_total += roll
            if not should_explode or roll != sides:
                break
        return die_total

    def _roll_rolemaster_die(self):
        """
        Rolemaster Open-Ended Logic:
        - 96-100: Roll again and add (recursive).
        - 01-05: Roll again and subtract (the subtraction itself explodes up).
        """
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
            # We generate the value to subtract. This value behaves like a 
            # high open-ended roll (if it's >= 96, it keeps growing).
            subtract_total = 0
            last_sub_roll = 100  # Force entry into loop
            
            while last_sub_roll >= 96:
                last_sub_roll = random.randint(1, 100)
                subtract_total += last_sub_roll
            
            return first_roll - subtract_total

        else:
            return first_roll
