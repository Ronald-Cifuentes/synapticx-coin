"""Configuración del laboratorio MVP."""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Config:
    """Configuración inmutable del lab."""

    # PoW
    difficulty: int = 2  # número de ceros al inicio del hash (hex)
    block_reward: int = 100

    # Asset
    default_asset_id: str = "BASE"

    @classmethod
    def default(cls) -> "Config":
        return cls()

    def to_dict(self) -> Dict[str, Any]:
        """Serializa para persistencia."""
        return {
            "difficulty": self.difficulty,
            "block_reward": self.block_reward,
            "default_asset_id": self.default_asset_id,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Config":
        """Deserializa desde persistencia."""
        return cls(
            difficulty=d.get("difficulty", 2),
            block_reward=d.get("block_reward", 100),
            default_asset_id=d.get("default_asset_id", "BASE"),
        )
