import os
import tomllib
from pathlib import Path
from typing import Any, Dict, Iterable


def load_config() -> Dict[str, Any]:
    """
    Loads configuration from standard locations.
    Priority:
    1. ~/.config/gg-cli/config.toml
    2. ~/.gg-cli.toml
    """
    home = Path.home()
    
    candidates = [
        home / ".config" / "gg-cli" / "config.toml",
        home / ".gg-cli.toml",
    ]

    for path in candidates:
        if path.exists() and path.is_file():
            try:
                with open(path, "rb") as f:
                    return tomllib.load(f)
            except Exception as e:
                print(f"Warning: Failed to load config file at {path}: {e}")
    
    return {}


def validate_config(config: Dict[str, Any], valid_systems: Iterable[str]) -> None:
    """
    Validates the configuration against allowed values.
    Modifies the config dictionary in-place by removing invalid entries.
    """
    if "core" in config:
        sys_val = config["core"].get("system")
        if sys_val and sys_val not in valid_systems:
            print(f"Warning: Invalid system '{sys_val}' in config file. Ignoring.")
            del config["core"]["system"]
