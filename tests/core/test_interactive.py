from unittest.mock import patch
from gamagama.core.main import run_interactive_mode
from gamagama.core.registry import CommandTree
from gamagama.commands import discover_commands
from gamagama.systems import GenericSystem


def test_show_at_root(capsys):
    """
    Test that 'show' at root displays all domain actives.
    """
    tree = CommandTree()
    discover_commands(tree)

    inputs = ["show", "quit"]

    with patch("builtins.input", side_effect=inputs):
        run_interactive_mode(tree, GenericSystem)

    captured = capsys.readouterr()

    # Should show domain actives
    assert "system: generic" in captured.out
    assert "player: (none)" in captured.out


def test_domain_navigation(capsys):
    """
    Test that typing just 'system' navigates to the domain.
    """
    tree = CommandTree()
    discover_commands(tree)

    inputs = ["system", "quit"]

    with patch("builtins.input", side_effect=inputs):
        run_interactive_mode(tree, GenericSystem)

    captured = capsys.readouterr()

    # No errors should occur
    assert "Command not found" not in captured.out
    assert "is not executable" not in captured.out


def test_domain_navigation_with_name(capsys):
    """
    Test 'player gandalf' tries to navigate and set active.
    """
    tree = CommandTree()
    discover_commands(tree)

    inputs = ["player gandalf", "quit"]

    with patch("builtins.input", side_effect=inputs):
        run_interactive_mode(tree, GenericSystem)

    captured = capsys.readouterr()

    # Should fail silently (player not loaded) but navigate to player domain
    # No "Command not found" error
    assert "Command not found" not in captured.out


def test_list_command(capsys):
    """
    Test 'list system' shows available systems.
    """
    tree = CommandTree()
    discover_commands(tree)

    inputs = ["list system", "quit"]

    with patch("builtins.input", side_effect=inputs):
        run_interactive_mode(tree, GenericSystem)

    captured = capsys.readouterr()

    assert "generic" in captured.out
    assert "rolemaster" in captured.out


def test_set_command(capsys):
    """
    Test 'set system rolemaster' changes the active system.
    """
    tree = CommandTree()
    discover_commands(tree)

    inputs = ["set system rolemaster", "show", "quit"]

    with patch("builtins.input", side_effect=inputs):
        run_interactive_mode(tree, GenericSystem)

    captured = capsys.readouterr()

    assert "System changed to: rolemaster" in captured.out
    assert "system: rolemaster" in captured.out
