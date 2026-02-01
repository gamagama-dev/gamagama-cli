from gamagama.commands.quit import QuitCommand


def test_quit_command_handler():
    """Tests the return value of the QuitCommand handler."""
    cmd = QuitCommand()
    assert cmd.handle(None) is False
