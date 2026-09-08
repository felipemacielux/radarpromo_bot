"""Único ponto do pipeline que sabe se uma conta de afiliado está ativa.

Scrapers, filtro e dedup nunca devem importar este módulo nem saber se um
link é de afiliado — eles só trabalham com URLs brutas.

Contas de afiliado ainda estão em processo de solicitação: enquanto
AFILIADO_ATIVO[loja] for False, resolver_link faz passthrough puro.
"""

from affiliate.config import AFILIADO_ATIVO, AFILIADO_TAG


def resolver_link(url: str, loja: str) -> str:
    if not AFILIADO_ATIVO.get(loja, False):
        return url

    # TODO: implementar geração do link de afiliado por loja assim que as
    # contas forem aprovadas (Amazon PA-API, Shopee Affiliate, ML Afiliados).
    tag = AFILIADO_TAG.get(loja, "")
    if not tag:
        return url

    return url
