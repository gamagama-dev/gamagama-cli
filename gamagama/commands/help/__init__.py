def handle_help(subparsers):
    """Prints a formatted list of all registered commands and their help text."""
    print("Available commands:")

    # Get command actions from the internal list argparse maintains
    commands = [action for action in subparsers._choices_actions]

    if not commands:
        return

    # Calculate padding for alignment
    max_len = max(len(cmd.dest) for cmd in commands)

    for cmd in sorted(commands, key=lambda x: x.dest):
        print(f"  {cmd.dest:<{max_len + 2}}{cmd.help}")


def register(parser, subparsers):
    """Registers the 'help' command."""
    help_parser = subparsers.add_parser(
        "help", help="Shows a list of all available commands."
    )
    # The lambda captures the 'subparsers' object from this function's scope.
    help_parser.set_defaults(func=lambda args: handle_help(subparsers))
