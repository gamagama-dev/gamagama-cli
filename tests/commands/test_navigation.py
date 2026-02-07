import argparse
import pytest
from gamagama.cli.commands.navigation import UpCommand, RootCommand
from gamagama.cli.core.session import Session
from gamagama.cli.core.tree import MapBranch

def test_up_command(parser_and_tree):
    _, tree = parser_and_tree
    
    # Setup: Create a child branch 'player' if it doesn't exist, or use it
    player_node = tree.get(["player"])
    if not player_node:
        player_node = MapBranch(name="player")
        tree.root.add_child(player_node)

    session = Session(tree)
    session.current_node = player_node
    
    # Execute '..'
    cmd = UpCommand()
    args = argparse.Namespace(_session=session)
    cmd.handle(args)
    
    assert session.current_node == tree.root

def test_up_command_at_root(parser_and_tree):
    _, tree = parser_and_tree
    session = Session(tree) # Starts at root
    
    cmd = UpCommand()
    args = argparse.Namespace(_session=session)
    cmd.handle(args)
    
    assert session.current_node == tree.root

def test_root_command(parser_and_tree):
    _, tree = parser_and_tree
    
    # Setup: Create deep nesting root -> player -> inventory
    player_node = tree.get(["player"])
    if not player_node:
        player_node = MapBranch(name="player")
        tree.root.add_child(player_node)
        
    inv_node = MapBranch(name="inventory")
    player_node.add_child(inv_node)
    
    session = Session(tree)
    session.current_node = inv_node
    
    # Execute '/'
    cmd = RootCommand()
    args = argparse.Namespace(_session=session)
    cmd.handle(args)
    
    assert session.current_node == tree.root

def test_navigation_no_session(capsys):
    """Test that navigation commands fail gracefully without a session."""
    cmd = UpCommand()
    args = argparse.Namespace(_session=None)
    cmd.handle(args)
    
    captured = capsys.readouterr()
    assert "Error: Navigation commands only work in interactive mode." in captured.out
