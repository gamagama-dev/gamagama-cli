import readline
from gamagama.core.tree import Branch


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
            if isinstance(current, Branch):
                child = current.get_child(part)
                if child:
                    current = child
                    continue
            
            # Path doesn't exist in tree or cannot be traversed
            return None

        # We can only complete if we are currently at a Branch
        if not isinstance(current, Branch):
            return None

        # Find matches by iterating over the branch (polymorphic)
        options = [node.name for node in current if node.name and node.name.startswith(text)]

        if state < len(options):
            return options[state]
        return None
