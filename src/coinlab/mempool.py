"""
Mempool: pool de transacciones pendientes.
Rechaza tx con inputs inexistentes y conflictos por nullifier.
"""

from typing import Dict, List, Optional, Set

from .transactions import PrivateTransaction


class Mempool:
    """Pool de transacciones pendientes."""

    def __init__(self) -> None:
        self._txs: Dict[str, PrivateTransaction] = {}
        self._nullifiers_pending: Set[str] = set()

    def add_transaction(
        self,
        tx: PrivateTransaction,
        used_nullifiers: Optional[Set[str]] = None,
        available_commitments: Optional[Set[str]] = None,
    ) -> tuple[bool, Optional[str]]:
        """
        Añade tx si: inputs existen, no hay conflicto de nullifier.
        available_commitments: si None, no se valida existencia de inputs.
        """
        if available_commitments is not None:
            from .state import tx_inputs_exist_in_state

            ok, err = tx_inputs_exist_in_state(tx, available_commitments)
            if not ok:
                return False, err
        nfs = set(tx.nullifiers())
        # Conflicto con cadena
        if used_nullifiers:
            for nf in nfs:
                if nf in used_nullifiers:
                    return False, f"Nullifier ya gastado en cadena: {nf[:16]}..."
        # Conflicto con mempool
        for nf in nfs:
            if nf in self._nullifiers_pending:
                return False, f"Nullifier en tx competidora: {nf[:16]}..."
        self._txs[tx.tx_id] = tx
        self._nullifiers_pending.update(nfs)
        return True, None

    def remove_transaction(self, tx_id: str) -> None:
        """Elimina tx del mempool (ej. ya incluida en bloque)."""
        if tx_id in self._txs:
            tx = self._txs[tx_id]
            for nf in tx.nullifiers():
                self._nullifiers_pending.discard(nf)
            del self._txs[tx_id]

    def select_for_block(self, limit: Optional[int] = None) -> List[PrivateTransaction]:
        """Selecciona txs para incluir en bloque (orden arbitrario)."""
        txs = list(self._txs.values())
        if limit:
            txs = txs[:limit]
        return txs

    def get_pending_nullifiers(self) -> Set[str]:
        return self._nullifiers_pending.copy()

    def __len__(self) -> int:
        return len(self._txs)

    def all_transactions(self) -> List[PrivateTransaction]:
        return list(self._txs.values())
