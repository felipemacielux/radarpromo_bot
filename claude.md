# CLAUDE.md — RadarPromo (Bot de Coleta e Catalogação de Ofertas)

Este arquivo dá contexto persistente ao Claude Code para trabalhar neste projeto. Leia antes de qualquer implementação.

## Visão geral do projeto

RadarPromo é um agregador brasileiro de promoções (Amazon, Shopee, Shein, Mercado Livre, Aliexpress) com WhatsApp como canal principal de distribuição. TikTok, Instagram e uma landing page estática funcionam como canais de captação, levando pessoas até o grupo/canal do WhatsApp. Modelo de negócio: links de afiliado nas ofertas publicadas.

**Restrições fortes do projeto:**
- Custo recorrente próximo de zero (só o domínio, ~R$40-50/ano)
- Sem backend/API na landing page (estática, atualizada via `git push`)
- Mínimo de intervenção manual diária
- Servidor físico já disponível (Ubuntu), sem custo de VPS

## Este módulo específico: coleta e catalogação de ofertas

Este repositório/pasta cobre o **módulo de scraping/catalogação**, que é a base de todo o resto do pipeline (filtro, geração de imagem, publicação). É o primeiro elo da corrente:

```
[Coleta/Catalogação] → [Filtro] → [Gerador de Imagem] → [Envio WhatsApp] → [Landing Page]
```

## Decisão arquitetural chave: scraping vs. API de afiliados

**Scraping (Selenium) = motor de descoberta.** Encontra ofertas, preços, descontos, avaliações.

**APIs oficiais de afiliados (Amazon PA-API, Shopee Affiliate, ML Afiliados) = geração do link monetizável**, usadas SOMENTE para trocar a URL bruta pelo link de afiliado, nunca para descoberta.

Essas duas responsabilidades NÃO devem se misturar no código. O módulo `affiliate/link_resolver.py` é o único ponto que sabe se uma conta de afiliado está ativa ou não. O resto do pipeline (scrapers, filtro, dedup) nunca deve saber disso — ele só trabalha com URLs "brutas" e deixa o resolver decidir se troca por link de afiliado ou não.

**Status atual das contas de afiliado: ainda em processo de solicitação.** Até serem aprovadas, `link_resolver.py` deve simplesmente retornar a URL original sem modificação (passthrough), sem quebrar o pipeline.

## Prioridade de desenvolvimento: robustez anti-detecção desde o início

O usuário definiu explicitamente que quer robustez contra bloqueio/CAPTCHA desde o começo, não velocidade a qualquer custo. Isso significa:

- Usar `undetected-chromedriver`, NÃO Selenium/ChromeDriver puro
- Rodar com Xvfb (display virtual), evitar `headless=True` puro
- Delays aleatórios entre ações (nunca intervalos fixos)
- Rotação de proxies (pool configurável via `.env`, nunca hardcoded)
- User-Agent fixo durante uma sessão de scraping, rotacionado apenas entre execuções
- Rate limit configurável POR LOJA (Amazon é mais rígida que Mercado Livre)
- Se aparecer CAPTCHA: pausar aquela loja com backoff, NUNCA tentar resolver automaticamente

## Nível de dificuldade/prioridade por loja

1. **Mercado Livre** — mais tolerante, ponto de partida recomendado para validar todo o pipeline
2. **Shopee** — JS pesado, precisa Selenium completo (não dá pra usar só requests+BeautifulSoup)
3. **Amazon** — a mais rígida. Priorizar migrar para PA-API assim que aprovado; scraping só como fallback conservador e temporário
4. **Shein** — pouco documentado, provavelmente exige mapear endpoints internos via DevTools/Network antes de decidir a abordagem

## Estrutura de pastas esperada

```
bot/
 ├── scrapers/
 │    ├── base_scraper.py          # classe abstrata: buscar_ofertas() -> list[dict]
 │    ├── mercadolivre_scraper.py
 │    ├── shopee_scraper.py
 │    ├── amazon_scraper.py
 │    └── shein_scraper.py
 ├── antidetect/
 │    ├── driver_factory.py        # cria driver undetected-chromedriver configurado
 │    ├── proxy_manager.py         # rotação de proxies
 │    └── behavior.py              # delays humanizados, scroll gradual
 ├── affiliate/
 │    ├── link_resolver.py         # URL bruta -> link de afiliado (ou passthrough)
 │    └── config.py                # chaves/tags de afiliado por loja (via .env)
 ├── data/
 │    ├── models.py                # schema SQLite
 │    └── dedup.py                 # evita reposto + histórico de preço
 ├── filtro.py                     # desconto mínimo, avaliação mínima, comparação com histórico
 ├── main.py                       # orquestra via APScheduler
 └── config.yaml                   # limites de rate, horários, seletores CSS por loja
```

## Schema SQLite esperado (tabela `produtos`)

- `id`
- `loja` (mercadolivre | shopee | amazon | aliexpress | shein)
- `titulo`
- `url` (URL bruta, sem afiliado)
- `preco_atual`
- `preco_original`
- `desconto_pct`
- `avaliacao`
- `primeira_vez_visto`
- `ultima_vez_visto`

Usado tanto para dedup (não republicar a mesma oferta em menos de X dias) quanto para histórico de preço (comparar se o "desconto" atual é real ou inflação artificial de preço "de tabela").

## Ambiente de execução

- Servidor físico Ubuntu, Docker Compose (containers separados: scraper/scheduler e Chrome+Selenium+Xvfb)
- Sem exposição de portas de entrada — só saída para internet
- Restart automático via `restart: unless-stopped` + systemd
- Backup diário do SQLite (`sqlite3 .backup`)
- Proxies e chaves de afiliado via `.env` / Docker secrets, nunca hardcoded no código

## Convenções de código

- Python 3.11+
- Cada scraper herda de `base_scraper.py` e implementa `buscar_ofertas() -> list[dict]` com estrutura de dados consistente entre lojas
- Configurações de rate limit, seletores CSS e horários ficam em `config.yaml`, não hardcoded
- Nenhum módulo de scraping deve conhecer lógica de afiliados — isso fica isolado em `affiliate/`

## O que NÃO fazer

- Não resolver CAPTCHA automaticamente
- Não misturar lógica de afiliado dentro dos scrapers
- Não hardcodar proxies, chaves de API ou tags de afiliado no código
- Não usar headless puro sem Xvfb
- Não disparar requests em intervalos fixos/previsíveis

## Pontos em aberto (decidir no momento em que for preciso)

- Seletores CSS reais de cada loja (exigem inspeção das páginas atuais, podem mudar com frequência)
- Provedor de proxy específico a usar (orçamento limitado)
- Regras exatas de filtro (desconto mínimo, avaliação mínima) — já há sugestões no plano de crescimento (`Plano_de_Crescimento`), mas podem ser ajustadas

## Regra de ouro

- Sempre que for preciso, me pergunte antes de decidir sozinho.