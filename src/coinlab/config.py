"""Configuración del laboratorio MVP."""

from dataclasses import dataclass


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
