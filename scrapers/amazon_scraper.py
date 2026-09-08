"""Scraper da Amazon — a loja mais rígida contra bots.

Prioridade: migrar para PA-API assim que a conta de afiliado for aprovada.
Este scraper deve ser tratado como fallback conservador e temporário.

TODO: implementar extração real. Os seletores em config.yaml
(lojas.amazon.seletores_css) são placeholders e precisam ser validados por
inspeção real da página (DevTools) antes de usar.
"""

from antidetect.driver_factory import criar_driver
from antidetect.proxy_manager import ProxyManager
from scrapers.base_scraper import BaseScraper


class AmazonScraper(BaseScraper):
    LOJA = "amazon"

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._proxy_manager = ProxyManager()

    def buscar_ofertas(self) -> list[dict]:
        # TODO: abrir driver via criar_driver(), navegar com rate limit
        # mais conservador que as demais lojas, aplicar antidetect.behavior
        # e extrair produtos usando os seletores de config.yaml. Se
        # aparecer CAPTCHA, pausar esta loja com backoff — nunca resolver
        # automaticamente.
        return []
