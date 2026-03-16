#!/usr/bin/env python3
"""
Simulación: dos transacciones compitiendo por la misma nota.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from coinlab.chain import Blockchain
from coinlab.config import Config
from coinlab.mempool import Mempool
from coinlab.miner import build_and_mine_block
from coinlab.notes import create_note
from coinlab.transactions import create_transfer_with_output_notes


def main():
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    mempool = Mempool()
    mempool.add_transaction(
        tx1,
        available_commitments=chain.state.commitments,
    )
    build_and_mine_block(chain, mempool, "miner")

    alice_note = out_notes[0]
    tx_legit, _ = create_transfer_with_output_notes(
        [alice_note], [50], ["bob"], fee=0
    )
    tx_attack, _ = create_transfer_with_output_notes(
        [alice_note], [50], ["eve"], fee=0
    )

    mempool = Mempool()
    ok1, _ = mempool.add_transaction(
        tx_legit,
        available_commitments=chain.state.commitments,
    )
    ok2, err2 = mempool.add_transaction(
        tx_attack,
        available_commitments=chain.state.commitments,
    )
    assert ok1
    assert not ok2, "Doble gasto debería ser rechazado"
    print("Doble gasto rechazado correctamente")
    print(f"Error esperado: {err2}")

    # Caso adicional: tx con input inexistente
    from coinlab.transactions import (
        PrivateTransaction,
        TransactionInput,
        TransactionOutput,
    )
    from coinlab.crypto_primitives import hash_hex
    from coinlab.types import CommitmentHash, TxId

    fake_tx = PrivateTransaction(
        tx_id=TxId("fake_tx"),
        inputs=[
            TransactionInput(
                commitment=CommitmentHash(hash_hex("input_inventado")),
                nullifier=hash_hex("nf_fake"),
                amount=50,
                asset_id="BASE",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out_fake")),
                amount=50,
                asset_id="BASE",
            )
        ],
        fee=0,
    )
    ok_fake, err_fake = mempool.add_transaction(
        fake_tx,
        available_commitments=chain.state.commitments,
    )
    assert not ok_fake, "Input inexistente debería ser rechazado"
    print("Input inexistente rechazado correctamente")


if __name__ == "__main__":
    main()
