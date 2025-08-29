import re, requests
from bs4 import BeautifulSoup
from typing import Dict, Any

PRICE_HINT = re.compile(r"(?:¥|\$|\bCNY\b|\bAUD\b)\s*\d[\d.,]*")

def fetch_price_from_url(url: str) -> Dict[str, Any]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)  # ↑ 超时长一点
        r.raise_for_status()
    except Exception as e:
        # 把错误带回去（如 ReadTimeout）
        return {
            "title": "请求失败",
            "price": "N/A",
            "currency": "",
            "source": url,
            "url": url,
            "error": f"{type(e).__name__}: {e}",
        }

    soup = BeautifulSoup(r.text, "html.parser")

    # 1) meta
    for key in ["product:price:amount", "og:price:amount"]:
        m = soup.find("meta", {"property": key}) or soup.find("meta", {"name": key})
        if m and m.get("content"):
            return {"title": soup.title.string.strip() if soup.title else url,
                    "price": m["content"], "currency": "AUTO",
                    "source": url, "url": url}

    # 2) schema.org
    item = soup.find(attrs={"itemprop": "price"}) or soup.find(attrs={"property": "price"})
    if item:
        val = item.get("content") or item.get_text(strip=True)
        return {"title": soup.title.string.strip() if soup.title else url,
                "price": val, "currency": "AUTO", "source": url, "url": url}

    # 3) 兜底
    candidates = soup.select('[class*="price"], [id*="price"], [class*="amount"], [id*="amount"]')
    texts = " ".join(el.get_text(" ", strip=True) for el in candidates) or soup.get_text(" ", strip=True)
    m = PRICE_HINT.search(texts)
    return {"title": soup.title.string.strip() if soup.title else url,
            "price": (m.group(0) if m else "N/A"),
            "currency": "AUTO", "source": url, "url": url}
