"""
Trabalho 4 — Locust: cada usuário virtual executa uma sequência de 10
invocações ao serviço de extração de links, cada uma com URL diferente.
"""
import os
from urllib.parse import quote

from locust import HttpUser, between, task

# 10 URLs distintas (páginas públicas estáveis / leves)
URLS = [
    "http://example.com/",
    "https://example.org/",
    "https://www.iana.org/domains/reserved",
    "https://httpbin.org/html",
    "https://www.w3.org/TR/html401/intro/intro.html",
    "https://info.cern.ch/",
    "https://www.rfc-editor.org/rfc/rfc2616",
    "https://books.toscrape.com/",
    "https://quotes.toscrape.com/",
    "https://webscraper.io/test-sites/e-commerce/static",
]

# Alvo: API direta (serviço de extração). Alternativa web: MODE=web
MODE = os.environ.get("LOCUST_MODE", "api").lower()
API_PREFIX = os.environ.get("API_PREFIX", "/api/")


def path_for(url: str) -> str:
    if MODE == "web":
        return f"/?url={quote(url, safe='')}"
    # Flask/Sinatra: /api/<path:url> — a URL alvo vai no path
    return f"{API_PREFIX.rstrip('/')}/{url}"


class LinkExtractorUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task
    def extrair_dez_urls(self):
        for i, url in enumerate(URLS, start=1):
            self.client.get(
                path_for(url),
                name=f"extract_{i:02d}",
                timeout=120,
            )
