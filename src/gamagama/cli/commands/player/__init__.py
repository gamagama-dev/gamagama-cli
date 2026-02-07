from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from gamagama.cli.core.domain import DomainBranch


@dataclass(eq=False)
class PlayerDomain(DomainBranch):
    """Domain for managing player characters."""

    name: str = "player"
    supported_verbs: Set[str] = field(
        default_factory=lambda: {"show", "list", "set", "load", "drop"}
    )

    def list_items(self, session) -> List[str]:
        """Return list of loaded player names."""
        return list(session.players.keys())

    def get_active(self, session) -> Optional[str]:
        """Return the active player name."""
        return session.active_player

    def set_active(self, session, name: str) -> bool:
        """Set the active player. Returns True if player exists."""
        if name not in session.players:
            return False
        session.active_player = name
        return True

    def show_item(self, session, name: Optional[str]) -> Optional[str]:
        """Return player details as a string."""
        target = name if name else session.active_player
        if not target or target not in session.players:
            return None

        char = session.players[target]
        lines = [
            f"Name: {char.name}",
            f"System: {char.system}",
        ]

        if char.strings:
            lines.append("Strings:")
            for key, value in char.strings.items():
                lines.append(f"  {key}: {value}")

        if char.stats:
            lines.append("Stats:")
            for key, value in char.stats.items():
                lines.append(f"  {key}: {value}")

        if char.skills:
            lines.append("Skills:")
            for key, value in char.skills.items():
                lines.append(f"  {key}: {value}")

        if char.counts:
            lines.append("Counts:")
            for key, (current, max_val) in char.counts.items():
                lines.append(f"  {key}: {current}/{max_val}")

        return "\n".join(lines)

    def has_nested_domains(self) -> bool:
        """Player has no nested domains."""
        return False

    def get_nested_actives(self, session) -> Dict[str, str]:
        """No nested domains."""
        return {}

    def load_item(self, session, name: str) -> bool:
        """Load a player from disk."""
        if name in session.players:
            print(f"Character '{name}' is already loaded.")
            return False

        character = session.store.load(name)
        if character is not None:
            session.players[name] = character
            print(f"Loaded character: {character.name}")
            return True
        return False

    def drop_item(self, session, name: Optional[str]) -> bool:
        """Drop a player from the session."""
        target = name if name else session.active_player
        if not target:
            print("No player specified and no active player set.")
            return False

        if target not in session.players:
            print(f"Character '{target}' is not loaded.")
            return False

        del session.players[target]
        print(f"Dropped character: {target}")

        # Clear active if we dropped the active player
        if session.active_player == target:
            session.active_player = None
            print("Active player cleared.")

        return True
