import argparse
import pytest
from gamagama.cli.commands import discover_commands
from gamagama.cli.core.registry import CommandTree, ArgparseBuilder


@pytest.fixture
def parser_and_tree():
    """Returns a parser with all commands registered and the command tree."""
    parser = argparse.ArgumentParser(prog="gg-cli")
    tree = CommandTree()
    discover_commands(tree)

    builder = ArgparseBuilder(tree)
    builder.build(parser)

    return parser, tree
