from ..base import CommandBase
from gamagama.core.domain import DomainBranch


def _find_domain(session, domain_name):
    """Find a domain branch by name, searching from root."""
    from gamagama.core.tree import Branch

    def search(node):
        if isinstance(node, DomainBranch) and node.name == domain_name:
            return node
        if isinstance(node, Branch):
            for child in node:
                result = search(child)
                if result:
                    return result
        return None

    return search(session.tree.root)


def _get_current_domain(session):
    """Get the current domain if we're in one."""
    if isinstance(session.current_node, DomainBranch):
        return session.current_node
    return None


def _resolve_domain(session, domain_name=None):
    """Resolve domain: use explicit name, current context, or None."""
    if domain_name:
        return _find_domain(session, domain_name)
    return _get_current_domain(session)


def _collect_all_actives(session):
    """Collect all top-level domain actives from the tree for root-level show."""
    from gamagama.core.tree import Branch

    actives = {}

    # Only look at direct children of root - these are the top-level domains
    for child in session.tree.root:
        if isinstance(child, DomainBranch):
            active = child.get_active(session)
            actives[child.name] = active if active else "(none)"
            # Also collect nested actives from this domain
            nested = child.get_nested_actives(session)
            for nested_name, nested_active in nested.items():
                actives[f"  {nested_name}"] = nested_active

    return actives


class ShowCommand(CommandBase):
    """Show item details or list of actives."""

    name = "show"
    help = "Show item details or active items."
    path = []

    def setup(self, spec):
        spec.add_argument("target", nargs="?", help="Domain or item name")
        spec.add_argument("name", nargs="?", help="Item name (if target is domain)")

    def handle(self, args):
        session = args._session
        target = getattr(args, "target", None)
        name = getattr(args, "name", None)

        # If target is a domain name, use it
        domain = None
        if target:
            domain = _find_domain(session, target)
            if domain:
                # target was a domain, name is the item
                pass
            else:
                # target might be an item name in current domain
                current = _get_current_domain(session)
                if current:
                    # Treat target as the item name
                    name = target
                    domain = current
                else:
                    print(f"Domain '{target}' not found.")
                    return

        if not domain:
            domain = _get_current_domain(session)

        if not domain:
            # At root - show all actives
            actives = _collect_all_actives(session)
            if actives:
                for domain_name, active in actives.items():
                    print(f"{domain_name}: {active}")
            else:
                print("No domains configured.")
            return

        # Check if this domain has nested domains
        if domain.has_nested_domains() and not name:
            # Show nested actives instead of item details
            # First, collect nested domain children
            nested_domains = []
            for child in domain:
                if isinstance(child, DomainBranch):
                    nested_domains.append(child)

            if nested_domains:
                for nested in nested_domains:
                    nested_active = nested.get_active(session)
                    print(f"{nested.name}: {nested_active if nested_active else '(none)'}")
            else:
                # No nested domain children found, show domain's own active
                active = domain.get_active(session)
                if active:
                    print(f"{domain.name}: {active}")
                else:
                    print(f"No active {domain.name}.")
            return

        # Show item details
        if "show" not in domain.supported_verbs:
            print(f"'show' is not available in this context.")
            return

        result = domain.show_item(session, name)
        if result:
            print(result)
        else:
            target_name = name if name else domain.get_active(session)
            if target_name:
                print(f"'{target_name}' not found.")
            else:
                print(f"No active {domain.name}.")


class ListCommand(CommandBase):
    """List items in a domain."""

    name = "list"
    help = "List items in a domain."
    path = []

    def setup(self, spec):
        spec.add_argument("domain", nargs="?", help="Domain to list items from")

    def handle(self, args):
        session = args._session
        domain_name = getattr(args, "domain", None)

        domain = _resolve_domain(session, domain_name)
        if not domain:
            if domain_name:
                print(f"Domain '{domain_name}' not found.")
            else:
                print("Not in a domain context. Specify a domain: list <domain>")
            return

        if "list" not in domain.supported_verbs:
            print(f"'list' is not available in this context.")
            return

        items = domain.list_items(session)
        active = domain.get_active(session)

        if not items:
            print(f"No {domain.name}s available.")
            return

        for item in items:
            marker = "* " if item == active else "  "
            print(f"{marker}{item}")


class SetCommand(CommandBase):
    """Set the active item in a domain."""

    name = "set"
    help = "Set the active item."
    path = []

    def setup(self, spec):
        spec.add_argument("target", help="Domain or item name")
        spec.add_argument("name", nargs="?", help="Item name (if target is domain)")

    def handle(self, args):
        session = args._session
        target = args.target
        name = getattr(args, "name", None)

        # If target is a domain name, use it
        domain = _find_domain(session, target)
        if domain:
            # target was a domain, name is required
            if not name:
                print(f"Usage: set {target} <name>")
                return
        else:
            # target might be an item name in current domain
            current = _get_current_domain(session)
            if current:
                name = target
                domain = current
            else:
                print(f"Domain '{target}' not found.")
                return

        if "set" not in domain.supported_verbs:
            print(f"'set' is not available in this context.")
            return

        if not domain.set_active(session, name):
            print(f"'{name}' not found in {domain.name}.")


class LoadCommand(CommandBase):
    """Load an item into a domain."""

    name = "load"
    help = "Load an item from storage."
    path = []

    def setup(self, spec):
        spec.add_argument("target", help="Domain or item name")
        spec.add_argument("name", nargs="?", help="Item name (if target is domain)")

    def handle(self, args):
        session = args._session
        target = args.target
        name = getattr(args, "name", None)

        # If target is a domain name, use it
        domain = _find_domain(session, target)
        if domain:
            if not name:
                print(f"Usage: load {target} <name>")
                return
        else:
            current = _get_current_domain(session)
            if current:
                name = target
                domain = current
            else:
                print(f"Domain '{target}' not found.")
                return

        if "load" not in domain.supported_verbs:
            print(f"'load' is not available in this context.")
            return

        domain.load_item(session, name)


class DropCommand(CommandBase):
    """Drop an item from a domain."""

    name = "drop"
    help = "Remove an item from the session."
    path = []

    def setup(self, spec):
        spec.add_argument("target", nargs="?", help="Domain or item name")
        spec.add_argument("name", nargs="?", help="Item name (if target is domain)")

    def handle(self, args):
        session = args._session
        target = getattr(args, "target", None)
        name = getattr(args, "name", None)

        domain = None
        if target:
            domain = _find_domain(session, target)
            if domain:
                # target was a domain
                pass
            else:
                # target might be an item name in current domain
                current = _get_current_domain(session)
                if current:
                    name = target
                    domain = current
                else:
                    print(f"Domain '{target}' not found.")
                    return

        if not domain:
            domain = _get_current_domain(session)

        if not domain:
            print("Not in a domain context. Specify a domain: drop <domain> [name]")
            return

        if "drop" not in domain.supported_verbs:
            print(f"'drop' is not available in this context.")
            return

        domain.drop_item(session, name)
