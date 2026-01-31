import importlib
import pkgutil


def discover_and_register_commands(subparsers):
    """Discovers and registers all commands in this package."""
    for _, name, _ in pkgutil.iter_modules(__path__, f"{__name__}."):
        module = importlib.import_module(name)
        if hasattr(module, "register"):
            module.register(subparsers)
