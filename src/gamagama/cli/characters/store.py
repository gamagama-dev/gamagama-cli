import json
from pathlib import Path
from typing import Optional

from .base import Character


class CharacterStore:
    """Loads character JSON files from a directory on disk."""

    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            base_dir = Path.home() / ".config" / "gg-cli" / "characters"
        self.base_dir = base_dir

    def load(self, name: str) -> Optional[Character]:
        """Load a character by name from a JSON file.

        Returns None and prints an error if the file is not found.
        """
        file_path = self.base_dir / f"{name}.json"
        if not file_path.exists():
            print(f"Character file not found: {file_path}")
            return None

        with open(file_path, "r") as f:
            data = json.load(f)

        return Character.from_dict(data)
