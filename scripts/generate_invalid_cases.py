#!/usr/bin/env python3
"""Genera invalid-cases JSON para conformance."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from coinlab.crypto_primitives import hash_hex, owner_secret_hash
from coinlab.transactions import (
    PrivateTransaction,
    TransactionInput,
    TransactionOutput,
    tx_id_from_payload,
)
from coinlab.types import CommitmentHash, TxId


def _serialize_tx(tx: PrivateTransaction) -> dict:
    return {
        "tx_id": tx.tx_id,
        "inputs": [
            {
                "commitment": str(i.commitment),
                "nullifier": i.nullifier,
                "amount": i.amount,
                "asset_id": i.asset_id,
                "secret": i.secret,
            }
            for i in tx.inputs
        ],
        "outputs": [
            {
                "commitment": str(o.commitment),
                "amount": o.amount,
                "asset_id": o.asset_id,
                "owner_secret_hash": o.owner_secret_hash,
            }
            for o in tx.outputs
        ],
        "fee": tx.fee,
    }


def main():
    out_dir = Path(__file__).resolve().parents[1] / "conformance" / "invalid-cases"
    out_dir.mkdir(parents=True, exist_ok=True)

    # input_inexistente: tx con commitment que no está en estado
    tx = PrivateTransaction(
        tx_id=TxId(""),
        inputs=[
            TransactionInput(
                commitment=CommitmentHash(hash_hex("input_inexistente")),
                nullifier=hash_hex("nf_fake"),
                amount=50,
                asset_id="BASE",
                secret="fake",
            )
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(hash_hex("out")),
                amount=50,
                asset_id="BASE",
                owner_secret_hash=owner_secret_hash(""),
            )
        ],
        fee=0,
    )
    tx.tx_id = tx_id_from_payload(tx)

    payload = {
        "description": "Tx con input commitment inexistente. Mempool debe rechazar.",
        "tx": _serialize_tx(tx),
    }
    (out_dir / "input_inexistente.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False)
    )
    print(f"Generado {out_dir / 'input_inexistente.json'}")


if __name__ == "__main__":
    main()
