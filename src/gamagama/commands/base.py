from abc import ABC, abstractmethod
from typing import List
from gamagama.core.registry import CommandSpec


class CommandBase(ABC):
    """Base class for all commands."""

    name: str = ""
    help: str = ""
    path: List[str] = []

    @abstractmethod
    def setup(self, spec: CommandSpec):
        """Configures the command arguments on the spec."""
        pass

    @abstractmethod
    def handle(self, args):
        """The handler function that executes the command's logic."""
        pass
