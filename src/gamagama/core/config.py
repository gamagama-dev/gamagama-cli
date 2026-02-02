import os
import tomllib
from pathlib import Path
from typing import Any, Dict


def load_config() -> Dict[str, Any]:
    """
    Loads configuration from standard locations.
    Priority:
    1. ~/.config/gg/config.toml
    2. ~/.gg.toml
    """
    home = Path.home()
    
    candidates = [
        home / ".config" / "gg" / "config.toml",
        home / ".gg.toml",
    ]

    for path in candidates:
        if path.exists() and path.is_file():
            try:
                with open(path, "rb") as f:
                    return tomllib.load(f)
            except Exception as e:
                print(f"Warning: Failed to load config file at {path}: {e}")
    
    return {}
