from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class Character:
    """Represents a player character loaded from a JSON file."""

    name: str
    system: str = "generic"
    strings: Dict[str, str] = field(default_factory=dict)
    stats: Dict[str, int] = field(default_factory=dict)
    skills: Dict[str, int] = field(default_factory=dict)
    counts: Dict[str, Tuple[int, int]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "Character":
        """Create a Character from a dictionary (parsed JSON)."""
        counts = {}
        for key, value in data.get("counts", {}).items():
            counts[key] = (value[0], value[1])

        return cls(
            name=data["name"],
            system=data.get("system", "generic"),
            strings=data.get("strings", {}),
            stats=data.get("stats", {}),
            skills=data.get("skills", {}),
            counts=counts,
        )
