import argparse

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
      o      RM-style Open-Ended (d100 only):
               96-100: re-roll and add d100oh.
               01-05: re-roll and subtract d100ol.
      oh     Open-Ended High only (d100 only): 96-100.
      ol     Open-Ended Low only (d100 only): 01-05.

    EXAMPLES:
      gg roll 3d6         # Rolls three 6-sided dice and sums the result.
      gg roll d20!+5      # Rolls one exploding d20 and adds 5.
      gg roll d100o       # Rolls a standard RM open-ended d100.
      gg roll 3(d6+1)     # Rolls a d6, adds 1, repeats 3 times, and sums.
      gg roll 1d100o+15 2d6 # Performs two separate rolls.
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
        print(f"--> Rolling dice with spec: {' '.join(args.dice_spec)}")
