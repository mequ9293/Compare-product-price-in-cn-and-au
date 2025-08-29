# providers/serpapi_au.py
import os, time, requests
from typing import List, Dict, Any

# 简单 TTL 缓存：key -> (expire_ts, data)
_CACHE: Dict[str, tuple] = {}
_TTL = 60 * 60   # 1 小时

def _k(q: str) -> str:
    # 归一化关键词作为缓存键
    return "au::" + " ".join(q.lower().split())

def search_serpapi_au(q: str, limit: int = 12) -> List[Dict[str, Any]]:
    key = os.getenv("SERPAPI_KEY")
    if not key:
        return []

    ck = _k(q)
    now = time.time()
    hit = _CACHE.get(ck)
    if hit and hit[0] > now:
        return hit[1][:limit]

    params = {
        "engine": "google_shopping",
        "q": q,
        "gl": "au",   # 澳大利亚
        "hl": "en",
        "location": "Sydney, New South Wales, Australia",
        "api_key": key,
    }
    r = requests.get("https://serpapi.com/search.json", params=params, timeout=15)
    r.raise_for_status()
    items = r.json().get("shopping_results", []) or []

    out: List[Dict[str, Any]] = []
    for s in items[:limit]:
        out.append({
            "title": s.get("title"),
            "price": s.get("extracted_price"),   # 数值型；可能为 None
            "currency": "AUD",
            "source": s.get("source") or "Google Shopping",
            "url": s.get("product_link") or s.get("link"),
            "thumb": s.get("thumbnail"),
            "shipping": s.get("delivery"),
            "last_checked": "live",
        })

    _CACHE[ck] = (now + _TTL, out)
    return out
