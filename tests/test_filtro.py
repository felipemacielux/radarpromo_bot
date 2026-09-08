from filtro import filtrar_ofertas

CONFIG = {"filtro": {"desconto_minimo_pct": 20, "avaliacao_minima": 4.0, "dias_sem_repostar": 7}}


def _oferta(**overrides):
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


def test_aprova_oferta_dentro_dos_criterios():
    aprovadas = filtrar_ofertas([_oferta()], CONFIG)
    assert len(aprovadas) == 1


def test_reprova_desconto_abaixo_do_minimo():
    aprovadas = filtrar_ofertas([_oferta(desconto_pct=10.0)], CONFIG)
    assert aprovadas == []


def test_reprova_avaliacao_abaixo_do_minimo():
    aprovadas = filtrar_ofertas([_oferta(avaliacao=3.5)], CONFIG)
    assert aprovadas == []


def test_trata_campos_ausentes_como_zero_sem_quebrar():
    oferta = _oferta()
    del oferta["desconto_pct"]
    del oferta["avaliacao"]
    aprovadas = filtrar_ofertas([oferta], CONFIG)
    assert aprovadas == []


def test_trata_campos_none_como_zero_sem_quebrar():
    aprovadas = filtrar_ofertas([_oferta(desconto_pct=None, avaliacao=None)], CONFIG)
    assert aprovadas == []
