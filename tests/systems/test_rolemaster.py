import argparse
from unittest.mock import patch
from gamagama.commands.roll import RollCommand
from gamagama.core.session import Session
from gamagama.core.tree import Tree
from gamagama.systems import RolemasterSystem


def _create_args(dice_spec):
    """Helper to create args with a valid Rolemaster session."""
    args = argparse.Namespace(dice_spec=dice_spec)
    tree = Tree()
    session = Session(tree)
    session.system = RolemasterSystem()
    setattr(args, "_session", session)
    return args


def test_roll_rolemaster_normal(capsys):
    """Tests d%! in normal range (06-95)."""
    cmd = RollCommand()
    args = _create_args(["d%!"])
    
    with patch("random.randint", return_value=50):
        cmd.handle(args)
        
    captured = capsys.readouterr()
    assert captured.out == "d%!: 50 [50]\n"


def test_roll_rolemaster_explode_up(capsys):
    """Tests d%! exploding upwards (96-100)."""
    cmd = RollCommand()
    args = _create_args(["d%!"])
    
    # 96 (explode) -> 50 (stop) = 146
    with patch("random.randint", side_effect=[96, 50]):
        cmd.handle(args)
        
    captured = capsys.readouterr()
    assert captured.out == "d%!: 146 [146]\n"


def test_roll_rolemaster_explode_up_recursive(capsys):
    """Tests d%! exploding upwards recursively."""
    cmd = RollCommand()
    args = _create_args(["d%!"])
    
    # 99 (explode) -> 98 (explode) -> 10 (stop) = 207
    with patch("random.randint", side_effect=[99, 98, 10]):
        cmd.handle(args)
        
    captured = capsys.readouterr()
    assert captured.out == "d%!: 207 [207]\n"


def test_roll_rolemaster_explode_down(capsys):
    """Tests d%! exploding downwards (01-05)."""
    cmd = RollCommand()
    args = _create_args(["d%!"])
    
    # 04 (explode down) -> 50 (stop subtraction) = 4 - 50 = -46
    with patch("random.randint", side_effect=[4, 50]):
        cmd.handle(args)
        
    captured = capsys.readouterr()
    assert captured.out == "d%!: -46 [-46]\n"


def test_roll_rolemaster_explode_down_recursive(capsys):
    """Tests d%! exploding downwards recursively."""
    cmd = RollCommand()
    args = _create_args(["d%!"])
    
    # 02 (explode down) -> 99 (continue subtraction) -> 50 (stop subtraction)
    # Result: 2 - (99 + 50) = 2 - 149 = -147
    with patch("random.randint", side_effect=[2, 99, 50]):
        cmd.handle(args)
        
    captured = capsys.readouterr()
    assert captured.out == "d%!: -147 [-147]\n"
