"""Delays humanizados e scroll gradual — nunca intervalos fixos/previsíveis."""

import random
import time


def delay_humanizado(min_s: float, max_s: float) -> None:
    time.sleep(random.uniform(min_s, max_s))


def scroll_gradual(driver, passos: int = 8, pausa_min: float = 0.3, pausa_max: float = 1.2) -> None:
    altura_total = driver.execute_script("return document.body.scrollHeight")
    passo_altura = altura_total / passos

    for i in range(1, passos + 1):
        driver.execute_script(f"window.scrollTo(0, {passo_altura * i});")
        delay_humanizado(pausa_min, pausa_max)
