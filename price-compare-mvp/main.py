from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Dict, Any
import uvicorn

# Demo providers (stubbed). Replace with real API or scraper modules when ready.
from providers.au_demo import search_au
from providers.cn_demo import search_cn

app = FastAPI(title="Price Compare MVP", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# from providers.fx import fetch_cny_to_aud
from providers.fx import fetch_cny_to_aud_info  # 改成这个

@app.get("/fx")
def fx():
    info = fetch_cny_to_aud_info()
    return {"cny_aud": info["rate"], "ts": info["ts"], "source": info["source"]}



from dotenv import load_dotenv
from providers.serpapi_au import search_serpapi_au
# 原有：from providers.au_demo import search_au  ← 可以删掉或保留
#from providers.cn_demo import search_cn          # 先继续用演示的中国列，之后再接淘宝
from providers.serpapi_cn_sites import search_serpapi_cn

load_dotenv()  # 读取 .env

@app.get("/search")
def search(q: str):
    # AU 用 SerpApi
    try:
        au = search_serpapi_au(q)
    except Exception as e:
        au = [{
            "title": "AU 查询失败", "price": None, "currency": "AUD",
            "source": "SerpApi", "url": "", "shipping": str(e), "last_checked": "err"
        }]

    # CN 过渡用serpapi
    try:
        cn = search_serpapi_cn(q)
    except Exception as e:
        cn = [{"title":"CN 查询失败（SerpApi）", "price":None, "currency":"CNY", "source":"SerpApi", "url":"", "shipping":str(e), "last_checked":"err"}]
    return {"query": q, "au": au, "cn": cn}


from providers.url_link import fetch_price_from_url

@app.get("/fetch")
def api_fetch(url: str):
    try:
        data = fetch_price_from_url(url)
        return {"ok": True, "data": data}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}
    
# Serve static files (frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
