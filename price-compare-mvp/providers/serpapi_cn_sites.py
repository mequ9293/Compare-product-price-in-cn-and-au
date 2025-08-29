# providers/serpapi_cn_sites.py —— CN via SerpApi（购物→网页 双兜底）
import os, time, re, requests, urllib.parse
from typing import List, Dict, Any, Tuple

_CACHE: Dict[str, Tuple[float, list]] = {}
_TTL = 60 * 60

ALLOW = [
    "jd.com","jd.hk","tmall.com","tmall.hk","taobao.com",
    "pinduoduo.com","yangkeduo.com","suning.com","vip.com",
    "kaola.com","gome.com.cn","1688.com"
]

SYN = {
    "nescafe": "雀巢 金牌 咖啡",
    "starbucks": "星巴克 咖啡豆",
    "lip balm": "润唇膏",
    "lipstick": "口红",
    "prada": "普拉达",
    "coffee": "咖啡",
    "toothbrush": "电动牙刷",
    "ipad": "iPad 平板",
    "iphone": "iPhone 手机",
}

def _ckey(q: str) -> str: return "cn::" + " ".join(q.lower().split())

def _price_from_text(t: str):
    if not t: return None
    s = t.replace(",", "")
    m = re.search(r"(?:￥|¥)\s*([0-9]+(?:\.[0-9]{1,2})?)", s)
    if not m:
        m = re.search(r"([0-9]+(?:\.[0-9]{1,2})?)\s*(?:元|CNY)", s, re.I)
    try: return float(m.group(1)) if m else None
    except: return None

def _fetch(params: dict):
    r = requests.get("https://serpapi.com/search.json", params=params, timeout=15)
    r.raise_for_status()
    j = r.json()
    err = j.get("error")
    if err and "hasn't returned any results" not in err:
        # key 失效/超额等算错误；“没结果”不抛
        raise RuntimeError(err)
    return j

def _candidates(q: str):
    qs = [q]
    low = q.lower()
    for k, zh in SYN.items():
        if k in low:
            qs.append(zh); break
    if re.fullmatch(r"[ -~]+", q):  # 全英文再加“中文”提示版
        qs.append(q + " 中文")
    # 去重保序
    seen=set(); out=[]
    for s in qs:
        if s not in seen: out.append(s); seen.add(s)
    return out

def _accept(url: str) -> bool:
    if not url: return False
    return any(d in url for d in ALLOW)

def search_serpapi_cn(q: str, limit: int = 12):
    key = os.getenv("SERPAPI_KEY")
    if not key: return []

    ck = _ckey(q); now = time.time()
    hit = _CACHE.get(ck)
    if hit and hit[0] > now: return hit[1][:limit]

    results = []

    for kw in _candidates(q):
        # 先：购物搜索（多区域/引擎）
        for use_site in [True, False]:
            base_q = f"{kw} (site:jd.com OR site:tmall.com OR site:taobao.com)" if use_site else kw
            base = {"q": base_q, "api_key": key, "num": "20", "hl":"zh-CN"}

            combos = [
                {"engine":"google","tbm":"shop","gl":"hk"},
                {"engine":"google_shopping","location":"Hong Kong"},
                {"engine":"google","tbm":"shop","gl":"sg"},
                {"engine":"google_shopping","location":"Singapore"},
                {"engine":"google","tbm":"shop"},
            ]
            items=[]
            for opt in combos:
                j = _fetch({**base, **opt})
                items = j.get("shopping_results") or []
                if items: break

            for s in items:
                url = s.get("product_link") or s.get("link") or ""
                if not _accept(url): 
                    if use_site:  # 有 site 了还不在白名单，跳
                        continue
                results.append({
                    "title": s.get("title"),
                    "price": s.get("extracted_price") or _price_from_text(s.get("price") or ""),
                    "currency": "CNY",
                    "source": s.get("source") or "Google Shopping",
                    "url": url,
                    "thumb": s.get("thumbnail"),
                    "shipping": s.get("delivery"),
                    "last_checked": "live",
                })
            if results: break
        if results: break

        # 再：普通网页搜索（从 snippet/title 里抽价格）
        if not results:
            site_filter = "(site:jd.com OR site:tmall.com OR site:taobao.com OR site:pinduoduo.com OR site:yangkeduo.com)"
            base = {"engine":"google","q": f"{kw} {site_filter}", "api_key": key, "num":"20", "hl":"zh-CN"}
            j = _fetch(base)
            for r in j.get("organic_results", []):
                url = r.get("link") or ""
                if not _accept(url): continue
                title = r.get("title") or ""
                snippet = r.get("snippet") or ""
                price = _price_from_text(title) or _price_from_text(snippet)
                results.append({
                    "title": title,
                    "price": price,
                    "currency": "CNY",
                    "source": "Google Web",
                    "url": url,
                    "thumb": None,
                    "shipping": "",
                    "last_checked": "live",
                })
            if results: break

    _CACHE[ck] = (now + _TTL, results)
    return results[:limit]
