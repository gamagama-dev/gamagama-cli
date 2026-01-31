import argparse
import pytest
from gamagama.commands import discover_and_register_commands
from gamagama.commands.help import HelpCommand
from gamagama.commands.quit import QuitCommand
from gamagama.commands.roll import RollCommand


@pytest.fixture
def parser_and_subparsers():
    """Returns a parser with all commands registered and its subparsers action."""
    parser = argparse.ArgumentParser(prog="gg")
    subparsers = parser.add_subparsers(title="Commands")
    discover_and_register_commands(parser, subparsers)
    return parser, subparsers


def test_roll_command_handler(capsys):
    """Tests the output of the RollCommand handler."""
    cmd = RollCommand(None, None)
    args = argparse.Namespace(dice_spec=["3d6", "+", "1"])
    cmd.handle(args)
    captured = capsys.readouterr()
    assert captured.out == "--> Rolling dice with spec: 3d6 + 1\n"


def test_quit_command_handler():
    """Tests the return value of the QuitCommand handler."""
    cmd = QuitCommand(None, None)
    assert cmd.handle(None) is False


def test_help_command_list_output(parser_and_subparsers, capsys):
    """Tests the general help command output."""
    parser, subparsers = parser_and_subparsers
    cmd = HelpCommand(parser, subparsers)
    args = argparse.Namespace(command_name=None)
    cmd.handle(args)
    captured = capsys.readouterr()
    output = captured.out
    assert "Available commands:" in output
    assert "help" in output
    assert "quit" in output
    assert "roll" in output


def test_help_command_specific_output(parser_and_subparsers, capsys):
    """Tests the help output for a specific command in CLI mode."""
    parser, subparsers = parser_and_subparsers
    cmd = HelpCommand(parser, subparsers)
    args = argparse.Namespace(command_name="roll", _interactive=False)
    cmd.handle(args)
    captured = capsys.readouterr()
    assert "usage: gg roll" in captured.out
    assert "dice_spec" in captured.out


def test_help_command_specific_interactive_output(parser_and_subparsers, capsys):
    """Tests the help output for a specific command in interactive mode."""
    parser, subparsers = parser_and_subparsers
    cmd = HelpCommand(parser, subparsers)
    args = argparse.Namespace(command_name="roll", _interactive=True)
    cmd.handle(args)
    captured = capsys.readouterr()
    assert "usage: roll" in captured.out
    assert "gg" not in captured.out
    assert "dice_spec" in captured.out
