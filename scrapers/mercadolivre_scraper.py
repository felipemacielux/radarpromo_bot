"""Scraper do Mercado Livre — loja mais tolerante, ponto de partida do pipeline.

Seletores CSS vêm de config.yaml (lojas.mercadolivre.seletores_css). Foram
validados por inspeção real da página em 2026-09-08; revalidar se o scraper
passar a retornar listas vazias (sinal de que o Mercado Livre mudou o markup).
"""

import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from antidetect.behavior import delay_humanizado, scroll_gradual
from antidetect.driver_factory import criar_driver
from antidetect.proxy_manager import ProxyManager
from antidetect.user_agents import UserAgentManager
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger("radarpromo.scrapers.mercadolivre")

URL_OFERTAS_PADRAO = "https://www.mercadolivre.com.br/ofertas"


def _texto_para_preco(texto: str) -> float | None:
    if not texto:
        return None
    limpo = texto.strip().replace(".", "").replace(",", ".")
    try:
        return float(limpo)
    except ValueError:
        return None


def _texto_para_avaliacao(texto: str) -> float | None:
    if not texto:
        return None
    try:
        return float(texto.strip().replace(",", "."))
    except ValueError:
        return None


class MercadoLivreScraper(BaseScraper):
    LOJA = "mercadolivre"

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._proxy_manager = ProxyManager()
        self._user_agent_manager = UserAgentManager()

    def buscar_ofertas(self) -> list[dict]:
        seletores = self.config["seletores_css"]
        rate_limit = self.config["rate_limit_segundos"]
        url = self.config.get("url_ofertas", URL_OFERTAS_PADRAO)

        driver = criar_driver(
            proxy=self._proxy_manager.get_proxy(),
            user_agent=self._user_agent_manager.get_user_agent_aleatorio(),
        )
        ofertas: list[dict] = []
        try:
            driver.get(url)
            delay_humanizado(rate_limit["min"], rate_limit["max"])
            scroll_gradual(driver)

            cards = driver.find_elements(By.CSS_SELECTOR, seletores["lista_produtos"])
            for card in cards:
                oferta = self._extrair_oferta(card, seletores)
                if oferta is not None:
                    ofertas.append(oferta)
        except Exception:
            logger.exception("Falha ao coletar ofertas do Mercado Livre")
            return []
        finally:
            driver.quit()

        return ofertas

    def _extrair_oferta(self, card, seletores: dict) -> dict | None:
        try:
            titulo_el = card.find_element(By.CSS_SELECTOR, seletores["titulo"])
            titulo = titulo_el.text.strip()
            link_el = card.find_element(By.CSS_SELECTOR, seletores["link"])
            link = link_el.get_attribute("href")
        except NoSuchElementException:
            return None

        if not titulo or not link:
            return None

        preco_atual = self._preco_opcional(card, seletores["preco_atual"])
        preco_original = self._preco_opcional(card, seletores["preco_original"])
        avaliacao = self._avaliacao_opcional(card, seletores["avaliacao"])

        if preco_atual is None:
            return None

        desconto_pct = 0.0
        if preco_original and preco_original > preco_atual:
            desconto_pct = round((1 - preco_atual / preco_original) * 100, 2)
        else:
            preco_original = preco_atual

        return {
            "loja": self.LOJA,
            "titulo": titulo,
            "url": link,
            "preco_atual": preco_atual,
            "preco_original": preco_original,
            "desconto_pct": desconto_pct,
            "avaliacao": avaliacao,
        }

    @staticmethod
    def _preco_opcional(card, seletor: str) -> float | None:
        try:
            elemento = card.find_element(By.CSS_SELECTOR, seletor)
        except NoSuchElementException:
            return None
        return _texto_para_preco(elemento.text)

    @staticmethod
    def _avaliacao_opcional(card, seletor: str) -> float | None:
        try:
            elemento = card.find_element(By.CSS_SELECTOR, seletor)
        except NoSuchElementException:
            return None
        return _texto_para_avaliacao(elemento.text)
