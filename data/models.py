"""Schema SQLite da tabela `produtos` — dedup e histórico de preço."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "radarpromo.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    loja TEXT NOT NULL CHECK (loja IN (
        'mercadolivre', 'shopee', 'amazon', 'aliexpress', 'shein'
    )),
    titulo TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    preco_atual REAL,
    preco_original REAL,
    desconto_pct REAL,
    avaliacao REAL,
    primeira_vez_visto TEXT NOT NULL,
    ultima_vez_visto TEXT NOT NULL
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas(conn: sqlite3.Connection | None = None) -> None:
    fechar = conn is None
    conn = conn or get_connection()
    conn.execute(_SCHEMA)
    conn.commit()
    if fechar:
        conn.close()
