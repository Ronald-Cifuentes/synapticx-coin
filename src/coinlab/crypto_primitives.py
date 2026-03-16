"""
Primitivos criptográficos MVP de laboratorio.

ADVERTENCIA: Esto NO es criptografía de producción.
- Solo modela la semántica de commitments y nullifiers.
- No hay privacidad criptográfica real.
- Usamos SHA-256 como hash determinístico; en producción se usarían
  construcciones específicas (Pedersen, Poseidon, etc.).
"""

import hashlib
from typing import Optional


def hash_bytes(data: bytes) -> bytes:
    """Hash SHA-256 de bytes. Determinístico para el lab."""
    return hashlib.sha256(data).digest()


def hash_hex(data: str) -> str:
    """Hash SHA-256 de string, retorna hex."""
    return hashlib.sha256(data.encode()).hexdigest()


def commitment_for_note(
    owner_key: str,
    amount: int,
    nonce: str,
    asset_id: str = "BASE",
) -> str:
    """
    Genera un commitment para una nota.
    MVP: H(owner|amount|nonce|asset). En producción sería Pedersen/Poseidon.
    """
    payload = f"{owner_key}|{amount}|{nonce}|{asset_id}"
    return hash_hex(payload)


def nullifier_for_note(note_secret: str, commitment: str) -> str:
    """
    Genera nullifier para evitar doble gasto.
    MVP: H(secret|commitment). En producción sería derivación segura.
    """
    payload = f"{note_secret}|{commitment}"
    return hash_hex(payload)
