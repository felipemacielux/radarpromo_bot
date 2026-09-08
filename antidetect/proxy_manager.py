"""Rotação de proxies lidos de variável de ambiente (nunca hardcoded)."""

import os
import random


class ProxyManager:
    def __init__(self) -> None:
        raw = os.getenv("PROXY_LIST", "")
        self._proxies = [p.strip() for p in raw.split(",") if p.strip()]
        self._indice = 0

    def get_proxy(self) -> str | None:
        """Retorna o próximo proxy do pool (round-robin), ou None se vazio."""
        if not self._proxies:
            return None

        proxy = self._proxies[self._indice % len(self._proxies)]
        self._indice += 1
        return proxy

    def get_proxy_aleatorio(self) -> str | None:
        if not self._proxies:
            return None
        return random.choice(self._proxies)
