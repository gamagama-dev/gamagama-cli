from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, Set, runtime_checkable

from .tree import MapBranch


@runtime_checkable
class Domain(Protocol):
    """Protocol defining the interface for domain branches."""

    supported_verbs: Set[str]

    def list_items(self, session) -> List[str]:
        """Return list of available item names in this domain."""
        ...

    def get_active(self, session) -> Optional[str]:
        """Return the currently active item name, or None."""
        ...

    def set_active(self, session, name: str) -> bool:
        """Set the active item. Returns True on success, False on failure."""
        ...

    def show_item(self, session, name: Optional[str]) -> Optional[str]:
        """Return details for the item (or active if name is None). Returns None if not found."""
        ...

    def has_nested_domains(self) -> bool:
        """Return True if this domain has child domains with their own actives."""
        ...

    def get_nested_actives(self, session) -> Dict[str, str]:
        """Return dict of child domain names to their active item names."""
        ...


@dataclass(eq=False)
class DomainBranch(MapBranch):
    """A MapBranch that implements the Domain protocol for verb-first commands."""

    supported_verbs: Set[str] = field(default_factory=set)

    def list_items(self, session) -> List[str]:
        """Override in subclass to return available items."""
        return []

    def get_active(self, session) -> Optional[str]:
        """Override in subclass to return current active item."""
        return None

    def set_active(self, session, name: str) -> bool:
        """Override in subclass to set the active item."""
        return False

    def show_item(self, session, name: Optional[str]) -> Optional[str]:
        """Override in subclass to return item details."""
        return None

    def has_nested_domains(self) -> bool:
        """Override in subclass if domain has nested domains."""
        return False

    def get_nested_actives(self, session) -> Dict[str, str]:
        """Override in subclass to return nested domain actives."""
        return {}

    def load_item(self, session, name: str) -> bool:
        """Override in subclass if load is supported."""
        return False

    def drop_item(self, session, name: Optional[str]) -> bool:
        """Override in subclass if drop is supported."""
        return False
