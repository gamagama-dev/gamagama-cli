import argparse
from unittest.mock import patch
from gamagama.commands.roll import RollCommand


def test_roll_command_handler(capsys):
    """Tests the output of the RollCommand handler."""
    cmd = RollCommand()
    # Use a deterministic roll (1d1 always rolls 1)
    args = argparse.Namespace(dice_spec=["1d1"])
    cmd.handle(args)
    captured = capsys.readouterr()
    assert captured.out == "1d1: 1 [1]\n"


def test_roll_exploding(capsys):
    """Tests that dice explode (reroll) on max value."""
    cmd = RollCommand()
    args = argparse.Namespace(dice_spec=["1d6!"])

    # Mock random.randint to return:
    # 1. 6 (Max value -> Explode)
    # 2. 6 (Max value -> Explode again)
    # 3. 2 (Non-max -> Stop)
    with patch("random.randint", side_effect=[6, 6, 2]):
        cmd.handle(args)

    captured = capsys.readouterr()
    # Total should be 6 + 6 + 2 = 14
    # The list of rolls contains the total for that single die
    assert captured.out == "1d6!: 14 [14]\n"


def test_roll_exploding_multiple_dice(capsys):
    """Tests exploding logic with multiple dice."""
    cmd = RollCommand()
    args = argparse.Namespace(dice_spec=["2d4!"])

    # Mock random.randint:
    # Die 1: 4 (Explode) -> 1 (Stop) = Total 5
    # Die 2: 2 (Stop)                = Total 2
    with patch("random.randint", side_effect=[4, 1, 2]):
        cmd.handle(args)

    captured = capsys.readouterr()
    # Total: 5 + 2 = 7
    # Rolls: [5, 2]
    assert captured.out == "2d4!: 7 [5, 2]\n"


def test_roll_exploding_infinite_loop_prevention(capsys):
    """Tests that 1d1! is prevented to avoid infinite loops."""
    cmd = RollCommand()
    args = argparse.Namespace(dice_spec=["1d1!"])
    
    cmd.handle(args)
    
    captured = capsys.readouterr()
    assert "Cannot explode a 1-sided die" in captured.out
