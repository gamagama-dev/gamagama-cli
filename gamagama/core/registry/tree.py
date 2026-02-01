from typing import List
from ..tree import Tree
from .node import CommandSpec


class CommandTree(Tree):
    """A Tree specialized for storing CommandSpecs."""

    def register_command(self, path: List[str], spec: CommandSpec):
        """Registers a command specification at the given path."""
        self.insert(path, spec)
