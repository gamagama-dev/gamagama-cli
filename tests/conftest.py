import argparse
import pytest
from gamagama.commands import discover_commands
from gamagama.core.registry import CommandTree, ArgparseBuilder


@pytest.fixture
def parser_and_tree():
    """Returns a parser with all commands registered and the command tree."""
    parser = argparse.ArgumentParser(prog="gg")
    tree = CommandTree()
    discover_commands(tree)

    builder = ArgparseBuilder(tree)
    builder.build(parser)

    return parser, tree
