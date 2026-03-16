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


def owner_secret_hash(secret: str) -> str:
    """Hash del secret para verificar autorización de gasto."""
    return hash_hex(secret)


def commitment_for_output(
    owner_secret_hash: str,
    amount: int,
    asset_id: str,
    nonce: str,
) -> str:
    """
    Genera commitment verificable para un output.
    Fórmula: H(owner_secret_hash|amount|asset_id|nonce).
    Permite verificar que commitment deriva criptográficamente de metadata.
    """
    payload = f"{owner_secret_hash}|{amount}|{asset_id}|{nonce}"
    return hash_hex(payload)


def commitment_for_note(
    owner_key: str,
    amount: int,
    nonce: str,
    asset_id: str = "BASE",
) -> str:
    """
    DEPRECADO: usa commitment_for_output con owner_secret_hash.
    Mantenido para transición. Note.commitment() usa owner_secret_hash(secret).
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
