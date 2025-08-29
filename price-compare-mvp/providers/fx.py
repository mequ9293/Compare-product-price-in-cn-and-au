# providers/fx.py
import time, requests

_CACHE = {"ts": 0, "rate": 0.21, "source": "default"}
_TTL = 60 * 60

def fetch_cny_to_aud() -> float:
    """兼容旧用法：只要数字"""
    return fetch_cny_to_aud_info()["rate"]

def fetch_cny_to_aud_info() -> dict:
    now = time.time()
    if _CACHE["rate"] and now - _CACHE["ts"] < _TTL:
        return {"rate": _CACHE["rate"], "ts": _CACHE["ts"], "source": _CACHE["source"]}

    rate = _CACHE["rate"]
    source = "default"
    try:
        r = requests.get("https://api.exchangerate.host/latest",
                         params={"base":"CNY","symbols":"AUD"}, timeout=8)
        r.raise_for_status()
        rate = float(r.json()["rates"]["AUD"])
        source = "exchangerate.host"
    except Exception:
        try:
            r = requests.get("https://api.frankfurter.app/latest",
                             params={"from":"CNY","to":"AUD"}, timeout=8)
            rate = float(r.json()["rates"]["AUD"])
            source = "frankfurter.app"
        except Exception:
            pass

    _CACHE.update({"rate": round(rate, 6), "ts": now, "source": source})
    return {"rate": _CACHE["rate"], "ts": _CACHE["ts"], "source": _CACHE["source"]}
