import argparse
from gamagama.commands.roll import RollCommand


def test_roll_command_handler(capsys):
    """Tests the output of the RollCommand handler."""
    cmd = RollCommand()
    # Use a deterministic roll (1d1 always rolls 1)
    args = argparse.Namespace(dice_spec=["1d1"])
    cmd.handle(args)
    captured = capsys.readouterr()
    assert captured.out == "1d1: 1 [1]\n"
