import readline


class Completer:
    """A completer for readline."""

    def __init__(self, commands):
        self.commands = commands

    def complete(self, text, state):
        """Returns the next possible completion for 'text'."""
        line = readline.get_line_buffer().split()
        # Only complete the first word
        if len(line) > 1 and line[0] in self.commands:
            return None

        options = [cmd for cmd in self.commands if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        return None
