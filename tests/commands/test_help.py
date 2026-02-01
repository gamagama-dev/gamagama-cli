import argparse
from gamagama.commands.help import HelpCommand


def test_help_command_list_output(parser_and_tree, capsys):
    """Tests the general help command output."""
    parser, tree = parser_and_tree
    cmd = HelpCommand()
    cmd.tree = tree
    args = argparse.Namespace(command_name=None)
    cmd.handle(args)
    captured = capsys.readouterr()
    output = captured.out
    assert "Available commands:" in output
    assert "help" in output
    assert "quit" in output
    assert "roll" in output


def test_help_command_specific_output(parser_and_tree, capsys):
    """Tests the help output for a specific command in CLI mode."""
    parser, tree = parser_and_tree
    cmd = HelpCommand()
    cmd.tree = tree
    args = argparse.Namespace(command_name=["roll"], _interactive=False)
    cmd.handle(args)
    captured = capsys.readouterr()
    assert "Help for 'roll':" in captured.out
    assert "Rolls dice based on one or more specifications." in captured.out


def test_help_command_specific_interactive_output(parser_and_tree, capsys):
    """Tests the help output for a specific command in interactive mode."""
    parser, tree = parser_and_tree
    cmd = HelpCommand()
    cmd.tree = tree
    args = argparse.Namespace(command_name=["roll"], _interactive=True)
    cmd.handle(args)
    captured = capsys.readouterr()
    assert "Help for 'roll':" in captured.out
    assert "Rolls dice based on one or more specifications." in captured.out
