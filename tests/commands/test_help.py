import argparse
from gamagama.commands.help import HelpCommand


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
