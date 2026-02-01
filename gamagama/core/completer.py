import readline
from gamagama.core.tree import MapBranch


class Completer:
    """A completer for readline."""

    def __init__(self, tree):
        self.tree = tree

    def complete(self, text, state):
        """Returns the next possible completion for 'text'."""
        line = readline.get_line_buffer().lstrip()
        parts = line.split()

        # Determine the path to the current branch.
        # If the line ends with a space, we are looking for a new child of the last word.
        # If not, we are completing the last word, so the path is everything before it.
        if line.endswith(" "):
            path = parts
        else:
            path = parts[:-1]

        # Traverse the tree
        current = self.tree.root
        for part in path:
            if isinstance(current, MapBranch) and part in current.children:
                current = current.children[part]
            else:
                # Path doesn't exist in tree, no completions
                return None

        # We can only complete if we are currently at a Branch (Group)
        if not isinstance(current, MapBranch):
            return None

        # Find matches
        options = [name for name in current.children.keys() if name.startswith(text)]

        if state < len(options):
            return options[state]
        return None
