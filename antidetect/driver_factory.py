"""Cria instâncias de undetected-chromedriver configuradas para o RadarPromo.

Assume que o processo já está rodando sob Xvfb (variável DISPLAY setada
pelo container/systemd) — nunca força headless=True puro, conforme
CLAUDE.md.
"""

import undetected_chromedriver as uc


def criar_driver(proxy: str | None = None, user_agent: str | None = None) -> uc.Chrome:
    options = uc.ChromeOptions()

    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    if user_agent:
        options.add_argument(f"--user-agent={user_agent}")

    options.add_argument("--disable-blink-features=AutomationControlled")

    return uc.Chrome(options=options)
