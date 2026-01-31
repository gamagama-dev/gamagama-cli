def register(parser, subparsers):
    """Registers the 'help' command."""
    help_parser = subparsers.add_parser(
        "help", help="Shows a list of all available commands."
    )
    help_parser.set_defaults(func=lambda args: parser.print_help())
