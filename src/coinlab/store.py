"""
Persistencia mínima: JSON en directorio de datos.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .blocks import Block, BlockHeader
from .chain import Blockchain, GENESIS_PREV
from .config import Config, chain_params_hash
from .notes import Note, deserialize_note, serialize_note
from .transactions import (
    PrivateTransaction,
    TransactionInput,
    TransactionOutput,
)
from .types import CommitmentHash, TxId


def _serialize_tx(tx: PrivateTransaction) -> Dict[str, Any]:
    return {
        "tx_id": tx.tx_id,
        "inputs": [
            {
                "commitment": i.commitment,
                "nullifier": i.nullifier,
                "amount": i.amount,
                "asset_id": i.asset_id,
                "secret": i.secret,
            }
            for i in tx.inputs
        ],
        "outputs": [
            {
                "commitment": o.commitment,
                "amount": o.amount,
                "asset_id": o.asset_id,
                "owner_secret_hash": getattr(o, "owner_secret_hash", "") or "",
                "nonce": getattr(o, "nonce", "") or "",
            }
            for o in tx.outputs
        ],
        "fee": tx.fee,
    }


def deserialize_tx(d: Dict[str, Any]) -> PrivateTransaction:
    """Deserializa tx desde dict (para conformance invalid-cases)."""
    return _deserialize_tx(d)


def _deserialize_tx(d: Dict[str, Any]) -> PrivateTransaction:
    return PrivateTransaction(
        tx_id=TxId(d["tx_id"]),
        inputs=[
            TransactionInput(
                commitment=CommitmentHash(i["commitment"]),
                nullifier=i["nullifier"],
                amount=i["amount"],
                asset_id=i["asset_id"],
                secret=i.get("secret", ""),
            )
            for i in d["inputs"]
        ],
        outputs=[
            TransactionOutput(
                commitment=CommitmentHash(o["commitment"]),
                amount=o["amount"],
                asset_id=o["asset_id"],
                owner_secret_hash=o.get("owner_secret_hash", "") or "",
                nonce=o.get("nonce", "") or "",
            )
            for o in d["outputs"]
        ],
        fee=d["fee"],
    )


def _serialize_block(block: Block) -> Dict[str, Any]:
    return {
        "header": {
            "prev_hash": block.header.prev_hash,
            "merkle_root": block.header.merkle_root,
            "timestamp": block.header.timestamp,
            "nonce": block.header.nonce,
            "difficulty": block.header.difficulty,
        },
        "transactions": [_serialize_tx(tx) for tx in block.transactions],
        "coinbase_commitment": block.coinbase_commitment,
        "coinbase_amount": block.coinbase_amount,
        "coinbase_owner_secret_hash": getattr(block, "coinbase_owner_secret_hash", "") or "",
        "coinbase_nonce": getattr(block, "coinbase_nonce", "") or "",
        "chain_params_hash": getattr(block, "chain_params_hash", None) or None,
    }


def _deserialize_block(d: Dict[str, Any]) -> Block:
    block = Block(
        header=BlockHeader(
            prev_hash=d["header"]["prev_hash"],
            merkle_root=d["header"]["merkle_root"],
            timestamp=d["header"]["timestamp"],
            nonce=d["header"]["nonce"],
            difficulty=d["header"]["difficulty"],
        ),
        transactions=[_deserialize_tx(tx) for tx in d["transactions"]],
        coinbase_commitment=d["coinbase_commitment"],
        coinbase_amount=d["coinbase_amount"],
        coinbase_owner_secret_hash=d.get("coinbase_owner_secret_hash", "") or "",
        coinbase_nonce=d.get("coinbase_nonce", "") or "",
        chain_params_hash=d.get("chain_params_hash") or None,
    )
    return block


class Store:
    """Almacenamiento en directorio."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.blocks_file = self.data_dir / "blocks.json"
        self.wallets_file = self.data_dir / "wallets.json"
        self.mempool_file = self.data_dir / "mempool.json"
        self.config_file = self.data_dir / "config.json"

    def save_config(self, config: Config) -> None:
        """Persiste config. Usar con init-chain o al crear cadena."""
        self.config_file.write_text(json.dumps(config.to_dict(), indent=2))

    def load_config(self) -> Optional[Config]:
        """Carga config persistida. None si no existe."""
        if not self.config_file.exists():
            return None
        data = json.loads(self.config_file.read_text())
        return Config.from_dict(data)

    def save_blocks(self, blocks: List[Block]) -> None:
        data = [_serialize_block(b) for b in blocks]
        self.blocks_file.write_text(json.dumps(data, indent=2))

    def load_blocks(self) -> List[Block]:
        if not self.blocks_file.exists():
            return []
        data = json.loads(self.blocks_file.read_text())
        return [_deserialize_block(d) for d in data]

    def save_wallets(self, wallets: Dict[str, List[str]]) -> None:
        """wallets: owner -> list of serialized notes"""
        self.wallets_file.write_text(json.dumps(wallets, indent=2))

    def load_wallets(self) -> Dict[str, List[str]]:
        if not self.wallets_file.exists():
            return {}
        return json.loads(self.wallets_file.read_text())

    def save_mempool(self, tx_list: List[PrivateTransaction]) -> None:
        data = [_serialize_tx(tx) for tx in tx_list]
        self.mempool_file.write_text(json.dumps(data, indent=2))

    def load_mempool(self) -> List[PrivateTransaction]:
        if not self.mempool_file.exists():
            return []
        data = json.loads(self.mempool_file.read_text())
        return [_deserialize_tx(d) for d in data]

    def config_for_chain(self, blocks: List[Block]) -> Config:
        """
        Carga config y verifica contra genesis.chain_params_hash.
        Falla si config.json fue alterada o formato legacy (sin hash en genesis).
        La fuente de verdad constitucional está en el ledger (genesis), no en config.json.
        """
        if not blocks:
            raise ValueError("config_for_chain requiere bloques")
        genesis = blocks[0]
        cph = getattr(genesis, "chain_params_hash", None)
        if not cph:
            raise RuntimeError(
                "Formato legacy: genesis no tiene chain_params_hash. "
                "Ejecute init-chain --force para resetear."
            )
        cfg = self.load_config()
        if cfg is None:
            raise RuntimeError(
                "Config no persistida. Ejecute init-chain --force para resetear."
            )
        computed = chain_params_hash(cfg)
        if computed != cph:
            raise RuntimeError(
                "Config alterada: hash no coincide con genesis. "
                "La cadena fue creada con config distinta. Ejecute init-chain --force para resetear."
            )
        return cfg

    def config_compatible_with_blocks(
        self, config: Config, blocks: List[Block]
    ) -> Tuple[bool, Optional[str]]:
        """
        Verifica que config sea coherente con bloques persistidos.
        Requiere genesis.chain_params_hash cuando hay bloques.
        Retorna (ok, error_message).
        """
        if not blocks:
            return True, None
        genesis = blocks[0]
        cph = getattr(genesis, "chain_params_hash", None)
        if not cph:
            return False, (
                "Formato legacy: genesis no tiene chain_params_hash. "
                "Ejecute init-chain --force para resetear."
            )
        if chain_params_hash(config) != cph:
            return False, "Config incoherente: hash no coincide con genesis"
        exp_diff = config.difficulty
        for i, block in enumerate(blocks):
            if block.header.difficulty != exp_diff:
                return False, (
                    f"Config incoherente con bloque {i}: "
                    f"header.difficulty={block.header.difficulty}, config.difficulty={exp_diff}"
                )
            if block.coinbase_amount != config.block_reward:
                return False, (
                    f"Config incoherente con bloque {i}: "
                    f"coinbase_amount={block.coinbase_amount}, config.block_reward={config.block_reward}"
                )
        return True, None
