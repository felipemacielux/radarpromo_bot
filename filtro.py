"""Filtro de ofertas: desconto mínimo, avaliação mínima, comparação com histórico."""


def filtrar_ofertas(ofertas: list[dict], config: dict) -> list[dict]:
    desconto_minimo = config["filtro"]["desconto_minimo_pct"]
    avaliacao_minima = config["filtro"]["avaliacao_minima"]

    aprovadas = []
    for oferta in ofertas:
        desconto = oferta.get("desconto_pct") or 0
        avaliacao = oferta.get("avaliacao") or 0

        if desconto < desconto_minimo:
            continue
        if avaliacao < avaliacao_minima:
            continue

        aprovadas.append(oferta)

    return aprovadas
