from ..base import CommandBase


class RollCommand(CommandBase):
    """Rolls dice based on a specification."""

    def register(self):
        """Registers the 'roll' command and its arguments."""
        roll_parser = self.subparsers.add_parser(
            "roll", help="Roll dice based on a specification."
        )
        roll_parser.add_argument(
            "dice_spec", nargs="+", help="The dice specification (e.g., 3d6)."
        )
        roll_parser.set_defaults(func=self.handle)

    def handle(self, args):
        """Handler for the 'roll' command."""
        print(f"--> Rolling dice with spec: {' '.join(args.dice_spec)}")
