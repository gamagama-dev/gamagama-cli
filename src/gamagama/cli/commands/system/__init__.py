from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from gamagama.cli.core.domain import DomainBranch
from gamagama.cli.systems import SYSTEMS


@dataclass(eq=False)
class SystemDomain(DomainBranch):
    """Domain for managing the active game system."""

    name: str = "system"
    supported_verbs: Set[str] = field(
        default_factory=lambda: {"show", "list", "set"}
    )

    def list_items(self, session) -> List[str]:
        """Return list of available system names."""
        return sorted(SYSTEMS.keys())

    def get_active(self, session) -> Optional[str]:
        """Return the active system name."""
        return session.system.name

    def set_active(self, session, name: str) -> bool:
        """Set the active system. Returns True on success."""
        sys_class = SYSTEMS.get(name)
        if not sys_class:
            print(f"Error: System '{name}' not found.")
            return False
        session.system = sys_class()
        # Clear schema active when system changes
        session.active_schema = None
        print(f"System changed to: {session.system.name}")
        return True

    def show_item(self, session, name: Optional[str]) -> Optional[str]:
        """Return system details."""
        target = name if name else session.system.name
        if target not in SYSTEMS:
            return None
        return f"System: {target}"

    def has_nested_domains(self) -> bool:
        """System has schema as a nested domain."""
        return True

    def get_nested_actives(self, session) -> Dict[str, str]:
        """Return nested domain actives (schema)."""
        result = {}
        if session.active_schema:
            result["schema"] = session.active_schema
        return result
