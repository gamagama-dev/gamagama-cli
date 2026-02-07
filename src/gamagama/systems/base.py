from abc import ABC
from typing import Dict, List, Optional, Type

from .dice import DiceEngine


class GameSystem(ABC):
    """Abstract base class for game-specific logic."""

    name = "generic"
    schemas: Dict[str, Type] = {}  # Maps schema name to Pydantic model (if any)

    def __init__(self):
        self.dice = DiceEngine()

    @classmethod
    def list_schemas(cls) -> List[str]:
        """Return list of available schema names."""
        return list(cls.schemas.keys())

    @classmethod
    def get_schema(cls, name: str) -> Optional[dict]:
        """Return JSON Schema for the named schema, or None."""
        model = cls.schemas.get(name)
        if model is None:
            return None
        # Pydantic v2 uses model_json_schema()
        if hasattr(model, "model_json_schema"):
            return model.model_json_schema()
        # Pydantic v1 fallback
        if hasattr(model, "schema"):
            return model.schema()
        return None
