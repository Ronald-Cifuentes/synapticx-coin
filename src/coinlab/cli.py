"""
CLI mínima: init-chain, create-wallet, mint-demo-notes, create-transfer, etc.
"""

from pathlib import Path
from typing import Optional

import typer

from .chain import Blockchain
from .config import Config
from .mempool import Mempool
from .miner import build_and_mine_block
from .notes import create_note, deserialize_note, serialize_note
from .store import Store
from .transactions import (
    create_transfer_transaction,
    create_transfer_with_output_notes,
    validate_transaction_basic,
)

app = typer.Typer(help="CoinLab MVP - Laboratorio de base monetaria privada")

DATA_DIR_OPTION = typer.Option(
    Path(".coinlab"),
    "--data-dir",
    "-d",
    help="Directorio de datos",
)


def _get_store(data_dir: Path) -> Store:
    return Store(data_dir)


def _load_chain(store: Store, config: Optional[Config] = None) -> Blockchain:
    """Carga cadena desde store. Usa config persistida si no se pasa una."""
    blocks = store.load_blocks()
    if not blocks:
        cfg = config or Config.default()
        return Blockchain(cfg)
    stored_config = store.load_config()
    cfg = config or stored_config or Config.default()
    ok, err = store.config_compatible_with_blocks(cfg, blocks)
    if not ok:
        raise RuntimeError(f"Config incoherente con bloques: {err}")
    chain = Blockchain(cfg)
    for block in blocks:
        ok, err = chain.add_block(block)
        if not ok:
            raise RuntimeError(f"Error cargando bloque: {err}")
    return chain


def _load_mempool(store: Store, chain: "Blockchain") -> Mempool:
    """Carga mempool validando cada tx contra chain.state (ruta segura)."""
    mempool = Mempool()
    for tx in store.load_mempool():
        mempool.add_transaction_validated(tx, chain.state)  # ignora txs inválidas
    return mempool


def _wallets_to_notes(store: Store) -> dict:
    """owner -> list of Note"""
    wallets = store.load_wallets()
    result = {}
    for owner, serialized in wallets.items():
        result[owner] = [deserialize_note(s) for s in serialized]
    return result


def _save_wallets(store: Store, owner_notes: dict) -> None:
    wallets = {owner: [serialize_note(n) for n in notes] for owner, notes in owner_notes.items()}
    store.save_wallets(wallets)


@app.command()
def init_chain(
    data_dir: Path = DATA_DIR_OPTION,
    difficulty: int = typer.Option(2, help="Dificultad PoW (ceros hex)"),
    force: bool = typer.Option(False, "--force", "-f", help="Sobrescribir cadena existente"),
):
    """Inicializa cadena con bloque genesis."""
    store = _get_store(data_dir)
    if store.load_blocks() and not force:
        typer.echo("Cadena ya existe. Para resetear y comenzar de cero: init-chain --force")
        raise typer.Exit(1)
    if force and store.load_blocks():
        store.save_blocks([])
        store.save_wallets({})
        store.save_mempool([])
        if store.config_file.exists():
            store.config_file.unlink()
    config = Config(difficulty=difficulty)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    store.save_config(config)
    store.save_blocks(chain.blocks)
    _save_wallets(store, {"faucet": [faucet_note]})
    typer.echo(f"Genesis creado. Block hash: {block.block_hash()[:16]}...")
    typer.echo(f"Faucet tiene 1 nota de {config.block_reward}")


@app.command()
def create_wallet(
    name: str = typer.Argument(..., help="Nombre del wallet"),
    data_dir: Path = DATA_DIR_OPTION,
):
    """Crea un wallet (solo registra nombre, sin notas)."""
    store = _get_store(data_dir)
    wallets = store.load_wallets()
    if name in wallets and wallets[name]:
        typer.echo(f"Wallet {name} ya existe con {len(wallets[name])} notas.")
    else:
        wallets[name] = []
        store.save_wallets(wallets)
        typer.echo(f"Wallet '{name}' creado.")


@app.command()
def mint_demo_notes(
    to: str = typer.Argument(..., help="Destinatario"),
    amount: int = typer.Argument(100, help="Monto"),
    data_dir: Path = DATA_DIR_OPTION,
):
    """Transfiere desde faucet a un wallet (crea tx y la añade al mempool)."""
    store = _get_store(data_dir)
    chain = _load_chain(store)
    owner_notes = _wallets_to_notes(store)
    faucet_notes = owner_notes.get("faucet", [])
    if not faucet_notes:
        has_chain = bool(store.load_blocks())
        if has_chain:
            typer.echo("Faucet sin notas (ya gastó todo). Ejecuta 'init-chain --force' para resetear.")
        else:
            typer.echo("Faucet sin notas. Ejecuta init-chain primero.")
        raise typer.Exit(1)
    note = faucet_notes[0]
    if note.amount < amount:
        typer.echo(f"Faucet tiene {note.amount}, se pide {amount}")
        raise typer.Exit(1)
    if note.amount == amount:
        input_notes = [note]
        output_amounts = [amount]
        output_owners = [to]
    else:
        input_notes = [note]
        output_amounts = [amount, note.amount - amount]
        output_owners = [to, "faucet"]
    tx, output_notes = create_transfer_with_output_notes(
        input_notes, output_amounts, output_owners, fee=0
    )
    mempool = _load_mempool(store, chain)
    ok, err = mempool.add_transaction_validated(tx, chain.state)
    if not ok:
        typer.echo(f"Error mempool: {err}")
        raise typer.Exit(1)
    store.save_mempool(mempool.all_transactions())
    faucet_notes.remove(note)
    for i, owner in enumerate(output_owners):
        if owner not in owner_notes:
            owner_notes[owner] = []
        owner_notes[owner].append(output_notes[i])
    _save_wallets(store, owner_notes)
    typer.echo(f"Tx creada: {tx.tx_id[:16]}... -> {to} {amount}")
    typer.echo("Ejecuta mine-block para incluir en cadena.")


@app.command()
def create_transfer(
    from_wallet: str = typer.Argument(..., help="Origen"),
    to_wallet: str = typer.Argument(..., help="Destino"),
    amount: int = typer.Argument(..., help="Monto"),
    fee: int = typer.Option(0, help="Fee"),
    data_dir: Path = DATA_DIR_OPTION,
):
    """Crea transferencia entre wallets."""
    store = _get_store(data_dir)
    chain = _load_chain(store)
    owner_notes = _wallets_to_notes(store)
    from_notes = owner_notes.get(from_wallet, [])
    total = sum(n.amount for n in from_notes)
    if total < amount + fee:
        typer.echo(f"{from_wallet} tiene {total}, se necesita {amount}+{fee}")
        raise typer.Exit(1)
    input_notes = []
    acc = 0
    for n in from_notes:
        input_notes.append(n)
        acc += n.amount
        if acc >= amount + fee:
            break
    change = acc - amount - fee
    output_amounts = [amount]
    output_owners = [to_wallet]
    if change > 0:
        output_amounts.append(change)
        output_owners.append(from_wallet)
    tx, output_notes = create_transfer_with_output_notes(
        input_notes, output_amounts, output_owners, fee=fee
    )
    mempool = _load_mempool(store, chain)
    ok, err = mempool.add_transaction_validated(tx, chain.state)
    if not ok:
        typer.echo(f"Error mempool: {err}")
        raise typer.Exit(1)
    store.save_mempool(mempool.all_transactions())
    for n in input_notes:
        owner_notes[from_wallet].remove(n)
    for i, owner in enumerate(output_owners):
        if owner not in owner_notes:
            owner_notes[owner] = []
        owner_notes[owner].append(output_notes[i])
    _save_wallets(store, owner_notes)
    typer.echo(f"Tx creada: {tx.tx_id[:16]}... {from_wallet} -> {to_wallet} {amount}")


@app.command()
def show_chain(
    data_dir: Path = DATA_DIR_OPTION,
):
    """Muestra la cadena."""
    store = _get_store(data_dir)
    chain = _load_chain(store)
    if not chain.blocks:
        typer.echo("Cadena vacía. Ejecuta init-chain.")
        return
    for i, block in enumerate(chain.blocks):
        h = block.block_hash()
        typer.echo(f"Block {i}: {h[:24]}... txs={len(block.transactions)} coinbase={block.coinbase_amount}")


@app.command()
def show_state(
    data_dir: Path = DATA_DIR_OPTION,
):
    """Muestra estado: commitments, nullifiers."""
    store = _get_store(data_dir)
    chain = _load_chain(store)
    typer.echo(f"Commitments: {len(chain.state.commitments)}")
    typer.echo(f"Nullifiers usados: {len(chain.state.nullifiers_used)}")
    for c in list(chain.state.commitments)[:5]:
        typer.echo(f"  {c[:32]}...")
    if len(chain.state.commitments) > 5:
        typer.echo("  ...")


@app.command()
def show_utxo_equivalent(
    data_dir: Path = DATA_DIR_OPTION,
):
    """Muestra notas por wallet (CACHE DE DEMO: wallets.json, no fuente canónica)."""
    store = _get_store(data_dir)
    owner_notes = _wallets_to_notes(store)
    for owner, notes in owner_notes.items():
        total = sum(n.amount for n in notes)
        typer.echo(f"{owner}: {len(notes)} notas, total={total}")


@app.command()
def mine_block(
    miner: str = typer.Option("miner", help="Dirección del minero"),
    data_dir: Path = DATA_DIR_OPTION,
):
    """Mina un bloque con txs del mempool."""
    store = _get_store(data_dir)
    chain = _load_chain(store)
    mempool = _load_mempool(store, chain)
    block = build_and_mine_block(chain, mempool, miner)
    store.save_blocks(chain.blocks)
    store.save_mempool(mempool.all_transactions())
    typer.echo(f"Bloque minado: {block.block_hash()[:24]}... reward={block.coinbase_amount}")


@app.command()
def validate_chain(
    data_dir: Path = DATA_DIR_OPTION,
):
    """Valida la cadena completa."""
    store = _get_store(data_dir)
    chain = _load_chain(store)
    ok, err = chain.validate_chain()
    if ok:
        typer.echo("Cadena válida.")
    else:
        typer.echo(f"Inválida: {err}")
        raise typer.Exit(1)


def _run_demo_in_memory() -> None:
    """Demo en memoria: dos wallets, mint, transfer, mine, double spend rechazado."""
    typer.echo("=== CoinLab Demo ===\n")
    config = Config(difficulty=2)
    chain = Blockchain(config)
    block, faucet_note = chain.create_genesis("faucet")
    typer.echo(f"1. Genesis: {block.block_hash()[:24]}...")
    alice_note = create_note("alice", 50, "BASE")
    bob_note = create_note("bob", 50, "BASE")
    tx1, out_notes = create_transfer_with_output_notes(
        [faucet_note], [50, 50], ["alice", "bob"], fee=0
    )
    mempool = Mempool()
    ok, _ = mempool.add_transaction_validated(tx1, chain.state)
    assert ok
    typer.echo("2. Tx creada: faucet -> alice(50), bob(50)")
    block2 = build_and_mine_block(chain, mempool, "miner")
    typer.echo(f"3. Bloque minado: {block2.block_hash()[:24]}...")
    typer.echo(f"   State: {len(chain.state.commitments)} commitments, {len(chain.state.nullifiers_used)} nullifiers")
    tx2, _ = create_transfer_with_output_notes(
        [out_notes[0]], [50], ["bob"], fee=0
    )
    ok, err = mempool.add_transaction_validated(tx2, chain.state)
    assert ok
    typer.echo("4. Tx: alice -> bob 50")
    tx_double, _ = create_transfer_with_output_notes(
        [out_notes[0]], [50], ["miner"], fee=0
    )
    ok, err = mempool.add_transaction_validated(tx_double, chain.state)
    typer.echo("5. Intento doble gasto (alice -> miner):")
    if ok:
        typer.echo("   ERROR: doble gasto aceptado (bug)")
    else:
        typer.echo(f"   Rechazado correctamente: {err}")
    block3 = build_and_mine_block(chain, mempool, "miner")
    typer.echo(f"6. Bloque final: {block3.block_hash()[:24]}...")
    ok, _ = chain.validate_chain()
    typer.echo(f"7. Cadena válida: {ok}")
    typer.echo("\n=== Demo OK ===")


@app.command()
def run_demo():
    """Ejecuta demo completa: genesis, transfer, mine, double spend."""
    _run_demo_in_memory()


if __name__ == "__main__":
    app()
