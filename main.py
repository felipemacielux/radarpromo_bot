"""Orquestrador do pipeline de coleta e catalogação.

[Scrapers] -> [filtro] -> [dedup/SQLite]

A resolução de link de afiliado (affiliate/link_resolver.py) não entra
aqui: fica reservada para o módulo de publicação, que ainda não existe
neste repositório.
"""

import logging
from pathlib import Path

import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from data.dedup import deve_republicar, salvar_ou_atualizar
from data.models import criar_tabelas, get_connection
from filtro import filtrar_ofertas
from scrapers.amazon_scraper import AmazonScraper
from scrapers.mercadolivre_scraper import MercadoLivreScraper
from scrapers.shein_scraper import SheinScraper
from scrapers.shopee_scraper import ShopeeScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("radarpromo")

SCRAPERS_POR_LOJA = {
    "mercadolivre": MercadoLivreScraper,
    "shopee": ShopeeScraper,
    "amazon": AmazonScraper,
    "shein": SheinScraper,
}

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


def carregar_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def rodar_pipeline_loja(loja: str, config: dict) -> None:
    scraper_cls = SCRAPERS_POR_LOJA[loja]
    scraper = scraper_cls(config["lojas"][loja])

    logger.info("Coletando ofertas: %s", loja)
    ofertas = scraper.buscar_ofertas()
    logger.info("%s: %d ofertas coletadas", loja, len(ofertas))

    aprovadas = filtrar_ofertas(ofertas, config)
    logger.info("%s: %d ofertas aprovadas no filtro", loja, len(aprovadas))

    dias_sem_repostar = config["filtro"]["dias_sem_repostar"]
    conn = get_connection()
    try:
        for oferta in aprovadas:
            if deve_republicar(conn, oferta["url"], dias_sem_repostar):
                salvar_ou_atualizar(conn, oferta)
    finally:
        conn.close()


def rodar_pipeline_completo() -> None:
    config = carregar_config()
    for loja, dados_loja in config["lojas"].items():
        if not dados_loja.get("ativo", False):
            continue
        rodar_pipeline_loja(loja, config)


def main() -> None:
    load_dotenv()
    criar_tabelas()

    scheduler = BlockingScheduler()
    scheduler.add_job(rodar_pipeline_completo, "interval", hours=6)

    logger.info("RadarPromo scraper iniciado. Rodando pipeline uma vez agora.")
    rodar_pipeline_completo()

    scheduler.start()


if __name__ == "__main__":
    main()
