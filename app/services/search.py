"""NovaSeek search engine layer.

Primary engine: local SearXNG (self-hosted metasearch, no API limits, no keys).
Fallback: DuckDuckGo HTML endpoint, so the API keeps answering even if the
SearXNG container is still warming up. Results are cached in-memory (TTLCache)
so repeated identical queries are served in microseconds.
"""
import asyncio
import hashlib
import logging

import httpx
from bs4 import BeautifulSoup
from cachetools import TTLCache

from ..config import settings

log = logging.getLogger("novaseek.search")

_cache: TTLCache = TTLCache(maxsize=4096, ttl=settings.CACHE_TTL_SECONDS)
_client: httpx.AsyncClient | None = None

_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 NovaSeek/1.0")


def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=settings.SEARCH_TIMEOUT,
            headers={"User-Agent": _UA},
            follow_redirects=True,
        )
    return _client


def _cache_key(q: str, lang: str, site: str, count: int) -> str:
    raw = f"{q}|{lang}|{site}|{count}"
    return hashlib.sha256(raw.encode()).hexdigest()


async def _searxng_search(q: str, lang: str, count: int) -> list[dict]:
    client = get_client()
    resp = await client.get(
        f"{settings.SEARXNG_URL}/search",
        params={
            "q": q,
            "format": "json",
            "language": lang,
            "safesearch": 0,
            "categories": "general",
        },
    )
    resp.raise_for_status()
    data = resp.json()
    results = []
    for r in data.get("results", [])[:count]:
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", ""),
            "engine": r.get("engine", "searxng"),
            "published": r.get("publishedDate"),
        })
    if not results:
        raise RuntimeError("empty_searxng_result")
    return results


async def _ddg_fallback(q: str, count: int) -> list[dict]:
    client = get_client()
    resp = await client.get(
        "https://html.duckduckgo.com/html/",
        params={"q": q},
        headers={"User-Agent": _UA},
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for node in soup.select(".result")[:count]:
        a = node.select_one(".result__a")
        sn = node.select_one(".result__snippet")
        if not a:
            continue
        results.append({
            "title": a.get_text(strip=True),
            "url": a.get("href", ""),
            "snippet": sn.get_text(strip=True) if sn else "",
            "engine": "duckduckgo",
            "published": None,
        })
    return results


async def search(query: str, lang: str = "auto", site: str | None = None,
                 count: int = 10) -> dict:
    query = (query or "").strip()
    if not query:
        raise ValueError("empty_query")
    count = max(1, min(count, 50))
    effective_q = f"site:{site} {query}" if site else query
    key = _cache_key(effective_q, lang, count)
    if key in _cache:
        return {**_cache[key], "cached": True}

    errors = []
    results: list[dict] = []
    engine_used = "searxng"
    try:
        results = await _searxng_search(effective_q, lang, count)
    except Exception as exc:  # noqa: BLE001
        log.warning("SearXNG failed (%s), falling back to DuckDuckGo", exc)
        errors.append(str(exc))
        engine_used = "duckduckgo"
        try:
            results = await _ddg_fallback(effective_q, count)
        except Exception as exc2:  # noqa: BLE001
            errors.append(str(exc2))
            raise RuntimeError("all_engines_failed: " + "; ".join(errors))

    payload = {
        "query": query,
        "site": site,
        "lang": lang,
        "engine": engine_used,
        "count": len(results),
        "results": results,
        "cached": False,
    }
    _cache[key] = payload
    return payload


async def warmup():
    """Background warmup so the first real request is fast."""
    try:
        await asyncio.sleep(2)
        await search("novaseek warmup", count=1)
        log.info("Search engine warmup OK")
    except Exception as exc:  # noqa: BLE001
        log.warning("Warmup failed (will retry lazily): %s", exc)
