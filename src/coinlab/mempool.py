"""
Mempool: pool de transacciones pendientes.
Ruta segura por defecto: add_transaction_validated(tx, chain_state).
"""

from typing import Dict, List, Optional, Set, TYPE_CHECKING

from .transactions import PrivateTransaction, validate_transaction_basic, verify_tx_id

if TYPE_CHECKING:
    from .state import ChainState


class Mempool:
    """Pool de transacciones pendientes."""

    def __init__(self) -> None:
        self._txs: Dict[str, PrivateTransaction] = {}
        self._nullifiers_pending: Set[str] = set()

    def add_transaction_validated(
        self,
        tx: PrivateTransaction,
        chain_state: "ChainState",
    ) -> tuple[bool, Optional[str]]:
        """
        Ruta SEGURA: valida tx contra estado canónico.
        Verifica tx_id == H(payload), estructura, autorización, amount/asset desde estado.
        Mismo contrato mínimo que validate_block para rechazar temprano.
        """
        ok, err = verify_tx_id(tx)
        if not ok:
            return False, err
        ok, err = validate_transaction_basic(tx)
        if not ok:
            return False, err
        ok, err = chain_state.can_apply_transaction(tx)
        if not ok:
            return False, err
        return self._add_transaction_internal(
            tx,
            used_nullifiers=chain_state.nullifiers_used,
        )

    def _add_transaction_internal(
        self,
        tx: PrivateTransaction,
        used_nullifiers: Optional[Set[str]] = None,
        available_commitments: Optional[Set[str]] = None,
    ) -> tuple[bool, Optional[str]]:
        """Interno: verifica conflictos de nullifier."""
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
