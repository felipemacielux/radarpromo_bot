from affiliate import config as affiliate_config
from affiliate.link_resolver import resolver_link

URL = "https://exemplo.com/produto"


def test_passthrough_quando_afiliado_inativo(monkeypatch):
    monkeypatch.setitem(affiliate_config.AFILIADO_ATIVO, "mercadolivre", False)
    assert resolver_link(URL, "mercadolivre") == URL


def test_passthrough_quando_loja_nao_mapeada():
    assert resolver_link(URL, "loja_desconhecida") == URL


def test_passthrough_quando_ativo_mas_sem_tag(monkeypatch):
    monkeypatch.setitem(affiliate_config.AFILIADO_ATIVO, "mercadolivre", True)
    monkeypatch.setitem(affiliate_config.AFILIADO_TAG, "mercadolivre", "")
    assert resolver_link(URL, "mercadolivre") == URL
