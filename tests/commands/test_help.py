import argparse
from gamagama.commands.help import HelpCommand
from gamagama.core.session import Session
from gamagama.core.tree import MapBranch


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
    # Verify we are NOT showing the detailed description in the list view
    assert "Syntax:" not in output


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
    # Verify detailed description is shown
    assert "Syntax: [count]d[sides][!][modifier]" in captured.out


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
    # Verify detailed description is shown
    assert "Syntax: [count]d[sides][!][modifier]" in captured.out


def test_help_bubbling_lookup(parser_and_tree, capsys):
    """Tests that help finds global commands when called from a subcommand context."""
    _, tree = parser_and_tree
    
    # Setup: Create a child branch 'player'
    player_node = tree.get(["player"])
    if not player_node:
        player_node = MapBranch(name="player")
        tree.root.add_child(player_node)

    session = Session(tree)
    session.current_node = player_node

    cmd = HelpCommand()
    cmd.tree = tree
    
    # User types 'help roll' while inside 'player'
    args = argparse.Namespace(command_name=["roll"], _session=session)
    cmd.handle(args)
    
    captured = capsys.readouterr()
    assert "Help for 'roll':" in captured.out
    # Verify detailed description is shown
    assert "Syntax: [count]d[sides][!][modifier]" in captured.out
