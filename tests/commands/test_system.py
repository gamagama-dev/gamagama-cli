import argparse
from gamagama.commands.system import SystemShowCommand, SystemListCommand, SystemSetCommand
from gamagama.core.session import Session
from gamagama.core.tree import Tree
from gamagama.systems import RolemasterSystem, GenericSystem


def _create_args():
    """Helper to create args with a valid session."""
    args = argparse.Namespace()
    tree = Tree()
    session = Session(tree)
    setattr(args, "_session", session)
    return args


def test_system_show(capsys):
    cmd = SystemShowCommand()
    args = _create_args()
    # Default is Generic
    cmd.handle(args)
    captured = capsys.readouterr()
    assert "Current system: generic" in captured.out


def test_system_list(capsys):
    cmd = SystemListCommand()
    args = _create_args()
    cmd.handle(args)
    captured = capsys.readouterr()
    assert "generic" in captured.out
    assert "rolemaster" in captured.out


def test_system_set_valid(capsys):
    cmd = SystemSetCommand()
    args = _create_args()
    args.system_name = "rolemaster"
    
    cmd.handle(args)
    
    captured = capsys.readouterr()
    assert "System changed to: rolemaster" in captured.out
    assert isinstance(args._session.system, RolemasterSystem)


def test_system_set_invalid(capsys):
    cmd = SystemSetCommand()
    args = _create_args()
    args.system_name = "invalid_game"
    
    cmd.handle(args)
    
    captured = capsys.readouterr()
    assert "System 'invalid_game' not found" in captured.out
    # Should remain Generic
    assert isinstance(args._session.system, GenericSystem)
