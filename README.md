# RadarPromo — Coleta e Catalogação de Ofertas

Módulo de scraping/catalogação do RadarPromo: descobre ofertas (Mercado
Livre, Shopee, Amazon, Shein), filtra por desconto/avaliação e persiste em
SQLite para dedup e histórico de preço. Ver `claude.md` para o contexto
completo do projeto e as decisões arquiteturais.

## Requisitos

- Python 3.11+
- Google Chrome instalado (usado via `undetected-chromedriver`)
- Linux: Xvfb, se for rodar sem monitor (nunca usar `headless=True` puro)

## Setup local

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Preencha o `.env` com o pool de proxies (`PROXY_LIST`) e, quando as contas
forem aprovadas, as tags de afiliado por loja. Enquanto
`*_AFFILIATE_ATIVO=false`, `affiliate/link_resolver.py` devolve a URL
original sem modificação — o pipeline funciona normalmente sem afiliado
configurado.

## Rodando os testes

```bash
pytest -q
```

Os testes cobrem apenas lógica pura (`filtro.py`, `data/dedup.py`,
`affiliate/link_resolver.py`, parsing do scraper do ML) — não abrem
navegador nem fazem requisições de rede.

## Rodando o scraper localmente

```bash
python main.py
```

Isso cria as tabelas do SQLite (`data/radarpromo.db`), roda o pipeline uma
vez e depois agenda execuções a cada 6 horas via APScheduler. Só a loja
Mercado Livre está com `ativo: true` em `config.yaml` no momento — as
demais (`shopee`, `amazon`, `shein`) ainda são placeholders.

Isso abre uma janela real do Chrome (via `undetected-chromedriver`). Em
ambientes com política de grupo restritiva (comum em máquinas corporativas
Windows) o lançamento do processo pode ser bloqueado pelo SO — nesse caso,
rodar em outra máquina/ambiente ou dentro do container Docker.

## Rodando com Docker

```bash
docker compose up -d --build
```

O `Dockerfile` já inclui Chromium + Xvfb no mesmo container do scraper
(sem depender de Selenium Grid remoto, preservando o patch anti-detecção
do `undetected-chromedriver`). O `docker-compose.yml` não expõe nenhuma
porta de entrada — só tráfego de saída — e usa `restart: unless-stopped`.
O SQLite fica persistido no volume `./data:/app/data`.

## Deploy no servidor (Ubuntu)

- `deploy/radarpromo.service`: unit systemd que sobe/derruba o
  `docker compose` no boot (`cp` para `/etc/systemd/system/`,
  `systemctl enable --now radarpromo`).
- `deploy/backup_sqlite.sh`: backup diário do SQLite via `sqlite3 .backup`,
  pensado para rodar por cron no host (não dentro do container), mantendo
  os últimos 14 backups.

## Estrutura

```
scrapers/     # um módulo por loja, herda de base_scraper.py
antidetect/   # driver factory, proxies, delays humanizados, rotação de UA
affiliate/    # único ponto que resolve URL bruta -> link de afiliado
data/         # schema SQLite + dedup/histórico de preço
filtro.py     # regras de desconto mínimo / avaliação mínima
main.py       # orquestração via APScheduler
tests/        # testes de lógica pura, sem browser/rede
deploy/       # systemd unit + script de backup para o servidor Ubuntu
```
