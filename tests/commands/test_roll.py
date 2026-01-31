import argparse
from gamagama.commands.roll import RollCommand


def test_roll_command_handler(capsys):
    """Tests the output of the RollCommand handler."""
    cmd = RollCommand(None, None)
    args = argparse.Namespace(dice_spec=["3d6", "+", "1"])
    cmd.handle(args)
    captured = capsys.readouterr()
    assert captured.out == "--> Rolling dice with spec: 3d6 + 1\n"
