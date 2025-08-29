# Price Compare MVP (AU vs CN)

**这是演示版（不含真实抓取）**：前端+后端一体，输入关键词，展示“澳大利亚 vs 中国”的价格卡片（假数据）。下一步可替换为真实 API 或允许抓取的来源。

## 运行

```bash
# 1) 建立虚拟环境（可选）
python -m venv .venv && source .venv/bin/activate  

# 2) 安装依赖
pip install -r requirements.txt

# 3) 启动
python main.py
# 打开浏览器： http://127.0.0.1:8000
```

## 目录结构
```
price-compare-mvp/
  main.py                # FastAPI 应用，提供 /search 接口并托管静态页面
  requirements.txt
  providers/
    au_demo.py           # AU 假数据提供者（后续换成真实来源）
    cn_demo.py           # CN 假数据提供者（后续换成真实来源）
  static/
    index.html           # 简单 UI
```

## 接入真实数据的建议（合规优先）
- **优先官方/公开 API**（如平台开放平台、联盟 API、搜索 API）。
- **遵守 TOS 与 robots.txt**，不要绕过登录、反爬或地理限制。
- **频控与缓存**：加 `ETag/Last-Modified` 缓存，设置 `Rate Limit`，避免高频访问。
- **商品“同款”匹配**：对品牌、容量、型号做归一化，避免把“套装/小样”与“正装”混在一起。
- **汇率**：用官方/公开汇率源（如央行/ECB APIs）；本 Demo 在前端用文本框手动输入汇率。
- **首期 MVP**：支持“用户粘贴具体商品链接→抓取页面上的价格”模式（较少风控风险），再扩展到站内搜索。

## R 语言路线（如果更熟 R）
- 用 `rvest` + `polite` 抓取**允许**的页面；
- 用 `plumber` 暴露 REST 接口；
- 前端可用 Shiny 或任意静态页面 `fetch()` 你的 plumber 接口。

最小 plumber 示例：
```r
# plumber.R
library(plumber)
#* @get /search
function(q="prada lip balm"){
  list(
    query=q,
    au=list(list(title="Demo AU", price=62, currency="AUD")),
    cn=list(list(title="演示 CN", price=268, currency="CNY"))
  )
}
# 运行：
# pr <- plumb("plumber.R"); pr$run(host="0.0.0.0", port=8000)
```

## 下一步可以做什么
- 接入 1~2 个真实来源（先选**易用/允许**的数据源）。
- 做“同款判定”与“价格含税/运费”统一展示。
- 加上“历史价格曲线”和“到手价计算器（汇率、税费、邮费）”。
- 部署到云端（任意支持 Python 的平台）。
