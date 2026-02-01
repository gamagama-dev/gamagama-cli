import importlib
import inspect
import pkgutil

from .base import CommandBase
from gamagama.core.registry import CommandSpec


def discover_commands(tree):
    """Discovers and registers all commands in this package into the tree."""
    for _, name, _ in pkgutil.iter_modules(__path__, f"{__name__}."):
        module = importlib.import_module(name)
        for _, member in inspect.getmembers(module):
            if (
                inspect.isclass(member)
                and issubclass(member, CommandBase)
                and member is not CommandBase
            ):
                command_instance = member()

                # Inject tree if the command needs it (like HelpCommand)
                if hasattr(command_instance, "tree"):
                    command_instance.tree = tree

                # CommandSpec is now a Node, so we initialize it with a name
                spec = CommandSpec(name=command_instance.name, handler=command_instance.handle, help=command_instance.help)
                command_instance.setup(spec)

                # Register at top level for now.
                tree.register_command([command_instance.name], spec)
