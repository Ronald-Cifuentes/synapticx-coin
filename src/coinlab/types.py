"""Tipos base del lab."""

from typing import NewType

# Identificadores opacos para el modelo
NoteId = NewType("NoteId", str)
CommitmentHash = NewType("CommitmentHash", str)
NullifierHash = NewType("NullifierHash", str)
BlockHash = NewType("BlockHash", str)
TxId = NewType("TxId", str)
