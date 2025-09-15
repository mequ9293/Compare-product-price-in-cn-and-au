# Price Compare MVP (AU vs CN)
# 海外价差一键比较 · MVP

A super-light “search once, compare instantly” project: enter a keyword or paste a product link; the left shows Australia prices, the right shows China prices. The right panel also converts CNY to AUD using a real-time FX rate (you can edit it).

一个超轻量的「一搜就比价」小项目：输入关键词或直接粘贴商品链接，左边出 **澳洲价**，右边出 **中国价**，右侧还会按**实时汇率**（可手动改）估算成 AUD。

---

## Highlights 功能亮点

*  **Keywords search 关键词搜索**

  * AU：Google Shopping（SerpApi）
  * CN：Google Shopping + 中文电商域名过滤（jd/tmall/taobao…），多地区/多引擎兜底 (我计划这样,但我没办法得到中国国内购物平台的API)
  * AU: Google Shopping (SerpAPI)
  * CN: Google Shopping + Chinese e-commerce domain filters (jd/tmall/taobao …), with multi-region / multi-engine fallback (I plan to do this, but I can't get the API of the Chinese domestic shopping platform)
*  **链接取价**：粘贴商品 URL（如官网页），尝试抓取标题/价格
*  **Link Pricing**: paste a product URL (e.g., an official product page) and the app will try to extract the title/price
*  **实时汇率** `/fx`：默认自动拉取 CNY→AUD（1 小时缓存），用户可手动修改
*  **Real-time FX** `/fx`: automatically fetches CNY→AUD (1-hour cache); users can edit the rate
*  **省额度**：各 Provider 内置 **1 小时缓存**（命中直接返回）
*  **Quota Saver**: each provider uses a 1-hour cache (cache hits return immediately)

---

## Quick Start 快速开始

### 1) Requirements 环境要求

* Python 3.10+ (3.12 recommended)
* A SerpAPI API key (free tier is fine)

### 2) Install dependencies 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt`：

```
fastapi
uvicorn[standard]
requests
python-dotenv
```

### 3) Environment variables 配置环境变量（.env）

Create `.env` at the project root:
在项目根目录创建 `.env`：

```
SERPAPI_KEY=your_serpapi_key
# Optional: add these when integrating JD/Taobao affiliate APIs (not set yet)**
# 可选：以后接入京东联盟/淘宝联盟再加 (可惜我没有!!)
# JD_APP_KEY=xxx
# JD_APP_SECRET=xxx
```

### 4) Launch 启动

```bash
python main.py
```

Open打开：`http://127.0.0.1:8000/`

---

## Project structure 项目结构

```
.
├─ main.py                    # FastAPI 入口（静态页 + API）
├─ static/
│  └─ index.html              # 前端（纯 HTML/CSS/JS）
└─ providers/
   ├─ serpapi_au.py           # 澳洲搜索（SerpApi）
   ├─ serpapi_cn_sites.py     # 中国搜索（SerpApi，多组合兜底）
   ├─ url_link.py             # 链接取价（简易解析）
   └─ fx.py                   # 实时汇率（exchangerate.host / frankfurter，1h 缓存）
```
```
.
├─ main.py                    # FastAPI entry (static page + API)
├─ static/
│  └─ index.html              # Frontend (plain HTML/CSS/JS)
└─ providers/
   ├─ serpapi_au.py           # AU search (SerpAPI)
   ├─ serpapi_cn_sites.py     # CN search (SerpAPI, multiple combos/fallback)
   ├─ url_link.py             # Link pricing (lightweight parser)
   └─ fx.py                   # Real-time FX (exchangerate.host / frankfurter, 1h cache)
```
---

## Tips 使用技巧

* **关键词越具体越好**：中文电商对中文词命中更高（如“雀巢 金牌 咖啡 210g”）。
* **Be specific with keywords**: Chinese marketplaces match Chinese terms better (e.g., “Nestlé coffee 210g”).
* **汇率**：页面加载会自动拉取 `/fx`，你也可以手动修改，右侧 CNY→AUD 估算即时刷新。
* **FX rate**: page loads will call /fx automatically; you can edit the rate and the CNY→AUD estimates on the right update instantly.
* **链接取价**：如果页面需要登录/JS 动态渲染，可能拿不到；这是演示能力，后续建议换官方 API。
* **Link pricing**: if a page requires login or heavy JS, extraction may fail; this is a demo—consider official APIs later.
---

## Render-generated web link (may be inactive,backend isn’t always running)
## 由Render生成的web link (不一定有效 后端非实时运行)
https://compare-product-price-in-cn-and-au.onrender.com

![UI preview](\web_example.png)
---

## License 许可

For learning and demo purposes only. When using data from third-party sites, follow their Terms of Service and applicable laws.
仅学习与演示用途。使用各站数据请遵守对应站点的服务条款（TOS）与法律法规。

