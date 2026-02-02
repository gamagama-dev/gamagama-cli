from unittest.mock import patch
from gamagama.core.main import run_interactive_mode
from gamagama.core.registry import CommandTree
from gamagama.commands import discover_commands
from gamagama.systems import GenericSystem


def test_greedy_resolution_execution(capsys):
    """
    Test that typing 'system show' from root executes the command 
    instead of just navigating to the 'system' branch.
    """
    tree = CommandTree()
    discover_commands(tree)

    # Mock inputs:
    # 1. "system show" (Should execute show)
    # 2. "quit" (Exit loop)
    inputs = ["system show", "quit"]
    
    with patch("builtins.input", side_effect=inputs):
        run_interactive_mode(tree, GenericSystem)

    captured = capsys.readouterr()
    
    # Verify that the output of SystemShowCommand appeared
    assert "Current system: generic" in captured.out
    # Verify we didn't get a "Command not found" error
    assert "Command not found" not in captured.out


def test_greedy_resolution_navigation(capsys):
    """
    Test that typing just 'system' navigates to the branch.
    """
    tree = CommandTree()
    discover_commands(tree)

    # Mock inputs:
    # 1. "system" (Should navigate)
    # 2. "quit"
    inputs = ["system", "quit"]
    
    with patch("builtins.input", side_effect=inputs):
        run_interactive_mode(tree, GenericSystem)

    captured = capsys.readouterr()
    
    # The prompt should have changed to gg/system> before quitting.
    # Since we mock input, we can't easily see the prompt change in stdout 
    # (it's passed to input()), but we can verify no errors occurred.
    assert "Command not found" not in captured.out
    assert "is not executable" not in captured.out


def test_greedy_resolution_partial_fail(capsys):
    """
    Test 'system invalid' - should fail and stay at root.
    """
    tree = CommandTree()
    discover_commands(tree)

    inputs = ["system invalid", "quit"]
    
    with patch("builtins.input", side_effect=inputs):
        run_interactive_mode(tree, GenericSystem)

    captured = capsys.readouterr()
    assert "Command not found: invalid" in captured.out
