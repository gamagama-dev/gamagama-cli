import readline
from gamagama.cli.core.tree import Branch


class Completer:
    """A completer for readline."""

    def __init__(self, tree, session=None):
        self.tree = tree
        self.session = session

    def complete(self, text, state):
        """Returns the next possible completion for 'text'."""
        line = readline.get_line_buffer().lstrip()
        parts = line.split()

        # Determine the path to the current branch.
        if line.endswith(" "):
            path = parts
            text = ""
        else:
            path = parts[:-1]

        start_node = self.session.current_node if self.session else self.tree.root
        
        options = []

        if not path:
            # Bubbling completion for the first word
            options = self._get_bubbling_options(start_node, text)
        else:
            # Strict traversal for subsequent words
            target_branch = self._resolve_path(start_node, path)
            if target_branch and isinstance(target_branch, Branch):
                options = [node.name + " " for node in target_branch if node.name and node.name.startswith(text)]

        if state < len(options):
            return options[state]
        return None

    def _get_bubbling_options(self, start_node, text):
        options = set()
        curr = start_node
        while curr:
            if isinstance(curr, Branch):
                for node in curr:
                    if node.name and node.name.startswith(text):
                        options.add(node.name + " ")
            curr = curr.parent
        return sorted(list(options))

    def _resolve_path(self, start_node, path):
        # First element bubbles
        first = path[0]
        curr = start_node
        found_node = None
        
        while curr:
            if isinstance(curr, Branch):
                child = curr.get_child(first)
                if child:
                    found_node = child
                    break
            curr = curr.parent
        
        if not found_node:
            return None
            
        # Rest elements are strict children
        current = found_node
        for part in path[1:]:
            if isinstance(current, Branch):
                child = current.get_child(part)
                if child:
                    current = child
                else:
                    return None
            else:
                return None
        return current
