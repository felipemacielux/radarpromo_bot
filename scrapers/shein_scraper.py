"""Scraper da Shein — pouco documentada.

Antes de finalizar a abordagem, provavelmente será necessário mapear
endpoints internos via DevTools/Network (pode ser mais eficiente que
scraping puro de DOM).

TODO: implementar extração real. Os seletores em config.yaml
(lojas.shein.seletores_css) são placeholders e precisam ser validados por
inspeção real da página antes de usar.
"""

from antidetect.driver_factory import criar_driver
from antidetect.proxy_manager import ProxyManager
from scrapers.base_scraper import BaseScraper


class SheinScraper(BaseScraper):
    LOJA = "shein"

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._proxy_manager = ProxyManager()

    def buscar_ofertas(self) -> list[dict]:
        # TODO: decidir entre scraping de DOM ou consumo direto de
        # endpoints internos mapeados via DevTools/Network, depois
        # implementar extração usando os seletores de config.yaml.
        return []
