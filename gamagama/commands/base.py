from abc import ABC, abstractmethod
import argparse


class NoHelpArgumentParser(argparse.ArgumentParser):
    """An ArgumentParser that defaults to not adding a --help argument."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("add_help", False)
        super().__init__(*args, **kwargs)


class CommandBase(ABC):
    """Base class for all commands."""

    def __init__(self, parser, subparsers):
        self.parser = parser
        self.subparsers = subparsers

    @abstractmethod
    def register(self):
        """Registers the command with its arguments to the subparser."""
        pass

    @abstractmethod
    def handle(self, args):
        """The handler function that executes the command's logic."""
        pass
