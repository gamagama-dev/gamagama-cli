import importlib
import inspect
import pkgutil

from .base import CommandBase
from gamagama.core.registry import CommandSpec
from gamagama.core.domain import DomainBranch


def discover_commands(tree):
    """Discovers and registers all commands and domains in this package into the tree."""
    # Track registered domains to avoid duplicates
    registered_domains = set()

    for _, name, is_pkg in pkgutil.iter_modules(__path__, f"{__name__}."):
        module = importlib.import_module(name)

        for _, member in inspect.getmembers(module):
            # Handle DomainBranch classes
            if (
                inspect.isclass(member)
                and issubclass(member, DomainBranch)
                and member is not DomainBranch
            ):
                domain_name = getattr(member, "name", None)
                if domain_name and domain_name not in registered_domains:
                    domain_instance = member()
                    tree.insert([domain_name], domain_instance)
                    registered_domains.add(domain_name)

                    # Check for nested domains in submodules
                    if is_pkg:
                        _discover_nested_domains(name, domain_instance, tree, registered_domains)

            # Handle CommandBase classes (traditional commands)
            elif (
                inspect.isclass(member)
                and issubclass(member, CommandBase)
                and member is not CommandBase
            ):
                command_instance = member()

                # Inject tree if the command needs it (like HelpCommand)
                if hasattr(command_instance, "tree"):
                    command_instance.tree = tree

                # CommandSpec is now a Node, so we initialize it with a name
                spec = CommandSpec(
                    name=command_instance.name,
                    handler=command_instance.handle,
                    help=command_instance.help,
                    description=command_instance.description or command_instance.help
                )
                command_instance.setup(spec)

                # Register using the command's defined path
                full_path = command_instance.path + [command_instance.name]
                tree.register_command(full_path, spec)


def _discover_nested_domains(parent_module_name, parent_domain, tree, registered_domains):
    """Discover nested domains in submodules and attach them to the parent."""
    parent_module = importlib.import_module(parent_module_name)

    if not hasattr(parent_module, "__path__"):
        return

    for _, name, _ in pkgutil.iter_modules(parent_module.__path__, f"{parent_module_name}."):
        module = importlib.import_module(name)

        for _, member in inspect.getmembers(module):
            if (
                inspect.isclass(member)
                and issubclass(member, DomainBranch)
                and member is not DomainBranch
            ):
                domain_name = getattr(member, "name", None)
                if domain_name and domain_name not in registered_domains:
                    domain_instance = member()
                    parent_domain.add_child(domain_instance)
                    registered_domains.add(domain_name)
