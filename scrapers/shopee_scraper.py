"""Scraper da Shopee — JS pesado, exige Selenium completo (não dá pra usar
requests+BeautifulSoup).

TODO: implementar extração real. Os seletores em config.yaml
(lojas.shopee.seletores_css) são placeholders e precisam ser validados por
inspeção real da página (DevTools) antes de usar.
"""

from antidetect.driver_factory import criar_driver
from antidetect.proxy_manager import ProxyManager
from scrapers.base_scraper import BaseScraper


class ShopeeScraper(BaseScraper):
    LOJA = "shopee"

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._proxy_manager = ProxyManager()

    def buscar_ofertas(self) -> list[dict]:
        # TODO: abrir driver via criar_driver(), navegar, aplicar
        # antidetect.behavior (delay_humanizado / scroll_gradual) e
        # extrair produtos usando os seletores de config.yaml.
        return []
