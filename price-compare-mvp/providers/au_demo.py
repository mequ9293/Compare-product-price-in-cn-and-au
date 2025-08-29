from typing import List, Dict

def search_au(q: str) -> List[Dict]:
    # Stubbed demo results (pretend from AU retailers). Replace with real providers.
    data = [
        {
            "title": "Prada Beauty - Lip Balm (Tinted) 3.2g",
            "price": 62.00,
            "currency": "AUD",
            "source": "Demo AU Store A",
            "url": "https://example-au-a.com/prada-lip-balm",
            "shipping": "Free over $50",
            "last_checked": "demo"
        },
        {
            "title": "Prada Lip Care Balm 3g",
            "price": 58.99,
            "currency": "AUD",
            "source": "Demo AU Store B",
            "url": "https://example-au-b.com/prada-lip-care",
            "shipping": "$7.95 standard",
            "last_checked": "demo"
        },
        {
            "title": "Prada Lip Balm Set (2x)",
            "price": 120.00,
            "currency": "AUD",
            "source": "Demo AU Store C",
            "url": "https://example-au-c.com/prada-balm-set",
            "shipping": "Free",
            "last_checked": "demo"
        },
    ]
    # naive filter for demo
    q_low = q.lower()
    return [x for x in data if all(t in x["title"].lower() for t in q_low.split())] or data
