from typing import List, Dict

def search_cn(q: str) -> List[Dict]:
    # Stubbed demo results (pretend from CN platforms). Replace with real providers.
    data = [
        {
            "title": "Prada 口红润唇膏 3.2g",
            "price": 268.00,
            "currency": "CNY",
            "source": "Demo CN Shop A",
            "url": "https://example-cn-a.com/prada-lip-balm",
            "shipping": "全国包邮",
            "last_checked": "demo"
        },
        {
            "title": "Prada 润唇膏 单支装",
            "price": 239.00,
            "currency": "CNY",
            "source": "Demo CN Shop B",
            "url": "https://example-cn-b.com/prada-lip-care",
            "shipping": "运费¥10",
            "last_checked": "demo"
        },
        {
            "title": "Prada 润唇膏 双支套装",
            "price": 458.00,
            "currency": "CNY",
            "source": "Demo CN Shop C",
            "url": "https://example-cn-c.com/prada-balm-set",
            "shipping": "包邮",
            "last_checked": "demo"
        },
    ]
    # naive filter for demo
    q_low = q.lower()
    return [x for x in data if all(t in x["title"].lower() for t in q_low.split())] or data
