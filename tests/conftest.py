import argparse
import pytest
from gamagama.commands import discover_and_register_commands


@pytest.fixture
def parser_and_subparsers():
    """Returns a parser with all commands registered and its subparsers action."""
    parser = argparse.ArgumentParser(prog="gg")
    subparsers = parser.add_subparsers(title="Commands")
    discover_and_register_commands(parser, subparsers)
    return parser, subparsers
