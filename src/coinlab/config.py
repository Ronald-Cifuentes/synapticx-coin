"""Configuración del laboratorio MVP."""

import json
from dataclasses import dataclass
from typing import Any, Dict

from .crypto_primitives import hash_hex


def chain_params_hash(config: "Config") -> str:
    """
    Hash determinístico de parámetros constitucionales.
    Ancla la config al ledger; alterar config.json sin coincidir con genesis invalida la carga.
    """
    d = config.to_dict()
    canonical = json.dumps(d, sort_keys=True)
    return hash_hex(canonical)


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
