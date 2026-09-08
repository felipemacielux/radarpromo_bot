"""Dedup por URL e histórico de preço (evita repostar, detecta desconto falso)."""

import sqlite3
from datetime import datetime, timedelta


def produto_existe(conn: sqlite3.Connection, url: str) -> bool:
    cur = conn.execute("SELECT 1 FROM produtos WHERE url = ?", (url,))
    return cur.fetchone() is not None


def deve_republicar(conn: sqlite3.Connection, url: str, dias: int) -> bool:
    """True se o produto nunca foi visto ou não é republicado há `dias` dias."""
    cur = conn.execute(
        "SELECT ultima_vez_visto FROM produtos WHERE url = ?", (url,)
    )
    row = cur.fetchone()
    if row is None:
        return True

    ultima_vez = datetime.fromisoformat(row["ultima_vez_visto"])
    return datetime.now() - ultima_vez >= timedelta(days=dias)


def salvar_ou_atualizar(conn: sqlite3.Connection, produto: dict) -> None:
    agora = datetime.now().isoformat()

    if produto_existe(conn, produto["url"]):
        conn.execute(
            """
            UPDATE produtos
            SET preco_atual = ?,
                preco_original = ?,
                desconto_pct = ?,
                avaliacao = ?,
                ultima_vez_visto = ?
            WHERE url = ?
            """,
            (
                produto.get("preco_atual"),
                produto.get("preco_original"),
                produto.get("desconto_pct"),
                produto.get("avaliacao"),
                agora,
                produto["url"],
            ),
        )
    else:
        conn.execute(
            """
            INSERT INTO produtos (
                loja, titulo, url, preco_atual, preco_original,
                desconto_pct, avaliacao, primeira_vez_visto, ultima_vez_visto
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                produto["loja"],
                produto["titulo"],
                produto["url"],
                produto.get("preco_atual"),
                produto.get("preco_original"),
                produto.get("desconto_pct"),
                produto.get("avaliacao"),
                agora,
                agora,
            ),
        )

    conn.commit()
