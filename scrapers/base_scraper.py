"""Classe abstrata para todos os scrapers de loja.

Cada implementação retorna uma lista de dicts com a estrutura:
    {
        "loja": str,             # mercadolivre | shopee | amazon | aliexpress | shein
        "titulo": str,
        "url": str,              # URL bruta, sem afiliado
        "preco_atual": float,
        "preco_original": float,
        "desconto_pct": float,
        "avaliacao": float,
    }

Scrapers nunca devem importar nada de `affiliate/` — essa camada só lida
com descoberta, não com monetização.
"""

from abc import ABC, abstractmethod


class BaseScraper(ABC):
    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def buscar_ofertas(self) -> list[dict]:
        raise NotImplementedError
