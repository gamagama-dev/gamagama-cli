import importlib
import inspect
import pkgutil

from .base import CommandBase


def discover_and_register_commands(parser, subparsers):
    """Discovers and registers all commands in this package."""
    for _, name, _ in pkgutil.iter_modules(__path__, f"{__name__}."):
        module = importlib.import_module(name)
        for _, member in inspect.getmembers(module):
            if (
                inspect.isclass(member)
                and issubclass(member, CommandBase)
                and member is not CommandBase
            ):
                command_instance = member(parser, subparsers)
                command_instance.register()
