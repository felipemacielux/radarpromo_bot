import sqlite3
from datetime import datetime, timedelta

import pytest

from data.dedup import deve_republicar, produto_existe, salvar_ou_atualizar
from data.models import criar_tabelas


@pytest.fixture
def conn():
    conexao = sqlite3.connect(":memory:")
    conexao.row_factory = sqlite3.Row
    criar_tabelas(conexao)
    yield conexao
    conexao.close()


def _produto(**overrides):
    base = {
        "loja": "mercadolivre",
        "titulo": "Produto teste",
        "url": "https://exemplo.com/produto",
        "preco_atual": 80.0,
        "preco_original": 100.0,
        "desconto_pct": 20.0,
        "avaliacao": 4.5,
    }
    base.update(overrides)
    return base


def test_produto_novo_nao_existe(conn):
    assert produto_existe(conn, "https://exemplo.com/produto") is False


def test_deve_republicar_produto_nunca_visto(conn):
    assert deve_republicar(conn, "https://exemplo.com/produto", dias=7) is True


def test_salvar_e_recuperar_produto(conn):
    salvar_ou_atualizar(conn, _produto())
    assert produto_existe(conn, "https://exemplo.com/produto") is True


def test_nao_deve_republicar_logo_apos_salvar(conn):
    salvar_ou_atualizar(conn, _produto())
    assert deve_republicar(conn, "https://exemplo.com/produto", dias=7) is False


def test_deve_republicar_apos_prazo_expirado(conn):
    salvar_ou_atualizar(conn, _produto())
    antiga = (datetime.now() - timedelta(days=10)).isoformat()
    conn.execute(
        "UPDATE produtos SET ultima_vez_visto = ? WHERE url = ?",
        (antiga, "https://exemplo.com/produto"),
    )
    conn.commit()
    assert deve_republicar(conn, "https://exemplo.com/produto", dias=7) is True


def test_atualizar_produto_existente_nao_duplica(conn):
    salvar_ou_atualizar(conn, _produto())
    salvar_ou_atualizar(conn, _produto(preco_atual=70.0))

    cur = conn.execute("SELECT COUNT(*) AS total FROM produtos")
    assert cur.fetchone()["total"] == 1

    cur = conn.execute("SELECT preco_atual FROM produtos WHERE url = ?", ("https://exemplo.com/produto",))
    assert cur.fetchone()["preco_atual"] == 70.0
