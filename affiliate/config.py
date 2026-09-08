"""Flags e chaves de afiliado por loja, lidas de variáveis de ambiente.

Nenhuma chave ou tag é hardcoded aqui — tudo vem do .env / Docker secrets.
"""

import os


def _bool_env(nome: str) -> bool:
    return os.getenv(nome, "false").strip().lower() == "true"


AFILIADO_ATIVO = {
    "mercadolivre": _bool_env("ML_AFFILIATE_ATIVO"),
    "shopee": _bool_env("SHOPEE_AFFILIATE_ATIVO"),
    "amazon": _bool_env("AMAZON_AFFILIATE_ATIVO"),
    "aliexpress": _bool_env("ALIEXPRESS_AFFILIATE_ATIVO"),
    "shein": _bool_env("SHEIN_AFFILIATE_ATIVO"),
}

AFILIADO_TAG = {
    "mercadolivre": os.getenv("ML_AFFILIATE_TAG", ""),
    "shopee": os.getenv("SHOPEE_AFFILIATE_TAG", ""),
    "amazon": os.getenv("AMAZON_AFFILIATE_TAG", ""),
    "aliexpress": os.getenv("ALIEXPRESS_AFFILIATE_TAG", ""),
    "shein": os.getenv("SHEIN_AFFILIATE_TAG", ""),
}
