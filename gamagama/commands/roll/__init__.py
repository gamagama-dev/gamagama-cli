import argparse
import random
import re

from ..base import CommandBase


class RollCommand(CommandBase):
    """Rolls dice based on one or more specifications.

    SYNTAX:
      A dice specification consists of one or more dice expressions.

    EXPRESSIONS:
      NdX[MODS][+/-M]    Rolls N X-sided dice.
      N(dX[MODS][+/-M])  Rolls a dX die N times, applying modifiers to each roll.

    COMPONENTS:
      N      The number of dice to roll (default: 1).
      d      A literal 'd' separator.
      X      The number of sides on the die (e.g., 6, 20, 100 or %).
      +/-M   A modifier added to the total (for NdX) or to each
             individual die roll (for N(dX)).

    MODS (Optional):
      !      Exploding Die: On a max roll, re-roll and add. (e.g. 6 on a d6).
      *      Open-Ended Die (d100 only): Add on 96-100, subtract on 1-5.

    EXAMPLES:
      gg roll 3d6         # Rolls three 6-sided dice and sums the result.
      gg roll d20!+5      # Rolls one exploding d20 and adds 5.
      gg roll d100*       # Rolls a standard RM open-ended d100.
      gg roll 3(d6+1)     # Rolls a d6, adds 1, repeats 3 times, and sums.
      gg roll 1d100*+15 2d6 # Performs two separate rolls.
    """

    def register(self):
        """Registers the 'roll' command and its arguments."""
        roll_parser = self.subparsers.add_parser(
            "roll",
            help="Rolls dice based on one or more specifications.",
            description=self.__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        roll_parser.add_argument(
            "dice_spec",
            nargs="+",
            help="One or more dice specifications (e.g., '3d6', '1d20+5').",
        )
        roll_parser.set_defaults(func=self.handle)

    def handle(self, args):
        """Handler for the 'roll' command."""
        for spec in args.dice_spec:
            print(self._roll_dice(spec))

    def _roll_dice(self, spec):
        """Parses a single dice spec (e.g., '3d6') and returns the roll result."""
        match = re.match(r"^(\d*)d(\d+|%)$", spec, re.IGNORECASE)
        if not match:
            return f"{spec}: Invalid dice specification."

        num_dice_str, sides_str = match.groups()

        num_dice = int(num_dice_str) if num_dice_str else 1
        sides = 100 if sides_str == "%" else int(sides_str)

        if sides == 0:
            return f"{spec}: Cannot roll a 0-sided die."

        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        total = sum(rolls)

        return f"{spec}: {total} {rolls}"
