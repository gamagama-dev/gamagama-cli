import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from gamagama.core.domain import DomainBranch


@dataclass(eq=False)
class SchemaDomain(DomainBranch):
    """Domain for managing schemas within a game system."""

    name: str = "schema"
    supported_verbs: Set[str] = field(
        default_factory=lambda: {"show", "list", "set"}
    )

    def list_items(self, session) -> List[str]:
        """Return list of available schema names for the current system."""
        return session.system.list_schemas()

    def get_active(self, session) -> Optional[str]:
        """Return the active schema name."""
        return session.active_schema

    def set_active(self, session, name: str) -> bool:
        """Set the active schema. Returns True if schema exists."""
        available = session.system.list_schemas()
        if name not in available:
            print(f"Error: Schema '{name}' not found in system '{session.system.name}'.")
            return False
        session.active_schema = name
        return True

    def show_item(self, session, name: Optional[str]) -> Optional[str]:
        """Return JSON schema definition."""
        target = name if name else session.active_schema
        if not target:
            return None

        schema = session.system.get_schema(target)
        if schema is None:
            return None

        return json.dumps(schema, indent=2)

    def has_nested_domains(self) -> bool:
        """Schema has no nested domains."""
        return False

    def get_nested_actives(self, session) -> Dict[str, str]:
        """No nested domains."""
        return {}
