# Price Compare MVP (AU vs CN)
# 海外价差一键比较 · MVP

一个超轻量的「一搜就比价」小项目：输入关键词或直接粘贴商品链接，左边出 **澳洲价**，右边出 **中国价**，右侧还会按**实时汇率**（可手动改）估算成 AUD。

---

## 功能亮点

*  **关键词搜索**

  * AU：Google Shopping（SerpApi）
  * CN：Google Shopping + 中文电商域名过滤（jd/tmall/taobao…），多地区/多引擎兜底
*  **链接取价**：粘贴商品 URL（如官网页），尝试抓取标题/价格
*  **实时汇率** `/fx`：默认自动拉取 CNY→AUD（1 小时缓存），用户可手动修改
*  **省额度**：各 Provider 内置 **1 小时缓存**（命中直接返回）

---

## 快速开始

### 1) 环境要求

* Python 3.10+（建议 3.12）
* 一个 SerpApi API Key（免费档即可）

### 2) 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt`（最小集）：

```
fastapi
uvicorn[standard]
requests
python-dotenv
```

### 3) 配置环境变量（.env）

在项目根目录创建 `.env`：

```
SERPAPI_KEY=你的_serpapi_key
# 可选：以后接入京东联盟/淘宝联盟再加 (可惜我没有!!)
# JD_APP_KEY=xxx
# JD_APP_SECRET=xxx
```

### 4) 启动

```bash
python main.py
```

打开：`http://127.0.0.1:8000/`

---

## 项目结构

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

---

## API 说明

* `GET /search?q=关键词`
  返回：

  ```json
  {
    "query":"iPad",
    "au":[ {"title":"...","price":123,"currency":"AUD","url":"...","thumb":"..."} ],
    "cn":[ {"title":"...","price":899,"currency":"CNY","url":"...","thumb":"..."} ]
  }
  ```

* `GET /fetch?url=商品链接`
  返回：

  ```json
  { "ok": true, "data": { "title":"...","price":"¥399.00","url":"..." } }
  ```

* `GET /fx`
  返回（前端默认读取并填充汇率输入框）：

  ```json
  { "cny_aud": 0.2137, "ts": 1724920000, "source": "exchangerate.host" }
  ```

---

## 使用技巧

* **关键词越具体越好**：中文电商对中文词命中更高（如“雀巢 金牌 咖啡 210g”）。
* **汇率**：页面加载会自动拉取 `/fx`，你也可以手动修改，右侧 CNY→AUD 估算即时刷新。
* **链接取价**：如果页面需要登录/JS 动态渲染，可能拿不到；这是演示能力，后续建议换官方 API。

---

## 由Render生成的web link (不一定有效 后端非实时运行)
https://compare-product-price-in-cn-and-au.onrender.com

---

## 许可

仅学习与演示用途。使用各站数据请遵守对应站点的服务条款（TOS）与法律法规。



