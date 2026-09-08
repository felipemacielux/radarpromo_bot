from scrapers.mercadolivre_scraper import _texto_para_avaliacao, _texto_para_preco


def test_texto_para_preco_sem_milhar():
    assert _texto_para_preco("872") == 872.0


def test_texto_para_preco_com_milhar():
    assert _texto_para_preco("1.499") == 1499.0


def test_texto_para_preco_invalido_retorna_none():
    assert _texto_para_preco("indisponível") is None


def test_texto_para_preco_vazio_retorna_none():
    assert _texto_para_preco("") is None


def test_texto_para_avaliacao_valido():
    assert _texto_para_avaliacao("4.9") == 4.9


def test_texto_para_avaliacao_vazia_retorna_none():
    assert _texto_para_avaliacao("") is None
