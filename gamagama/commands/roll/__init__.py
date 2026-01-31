def handle_roll(args):
    """Handler for the 'roll' command."""
    print(f"--> Rolling dice with spec: {' '.join(args.dice_spec)}")


def register(subparsers):
    """Registers the 'roll' command and its arguments."""
    parser = subparsers.add_parser("roll", help="Roll dice based on a specification.")
    parser.add_argument(
        "dice_spec", nargs="+", help="The dice specification (e.g., 3d6)."
    )
    parser.set_defaults(func=handle_roll)
