---
name: toa-news
description: Real-time crypto news API with advanced search. Supports keyword search, coin filtering, pagination. 6551-compatible data structure.
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📡"
    os:
      - darwin
      - linux
      - win32
  version: 2.0.0
---

# ToA Crypto News Skill

Query real-time crypto news from Tree of Alpha WebSocket feed. Supports advanced search with keyword and coin filtering.

**Base URL**: `https://web-production-666f44.up.railway.app`

---

## News Operations

### 1. Search News (Primary Endpoint)

`POST /news_search` is the primary search endpoint.

**Get latest news:**
```bash
curl -s -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}'

Search by keyword:
curl -s -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"q": "bitcoin ETF", "limit": 10, "page": 1}'
Search by coin symbol:
curl -s -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["BTC"], "limit": 10, "page": 1}'
Search Parameters
| Parameter | Type     | Required | Description                            |
| --------- | -------- | -------- | -------------------------------------- |
| limit     | integer  | yes      | Max results per page (1-100)           |
| page      | integer  | yes      | Page number (1-based)                  |
| q         | string   | no       | Full-text keyword search               |
| coins     | string[] | no       | Filter by coin symbols (e.g. ["BTC"])  |
| hasCoin   | boolean  | no       | Only return news with associated coins |
2. Simple News Fetch (Legacy)

curl -s "https://web-production-666f44.up.railway.app/news?limit=10"


Data Structures

News Article (6551-compatible)

{
  "id": "unique-article-id",
  "text": "Article headline",
  "body": "Full content text",
  "newsType": "Twitter",
  "engineType": "news",
  "link": "https://...",
  "coins": [
    {"symbol": "BTC", "market_type": "spot", "match": "title"}
  ],
  "aiRating": {
    "score": null,
    "grade": null,
    "signal": null,
    "status": "pending",
    "summary": null,
    "enSummary": null
  },
  "ts": 1772180907371,
  "receivedAt": "2026-02-27T08:28:27+00:00"
}

Response Structure

{
  "success": true,
  "data": [...],
  "limit": 10,
  "page": 1,
  "total": 1000,
"quota": "unlimited"
}
Common Workflows

Quick Market Overview

curl -s -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}' | jq '.data[] | {text, newsType, coins}'

BTC News Only

curl -s -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["BTC"], "limit": 20, "page": 1}'

Search for ETF News

curl -s -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"q": "ETF", "limit": 10, "page": 1}'


Data Processing Guidelines

When presenting news to users:

1. Extract key info: text, body, coins, link
2. Check aiRating: If status == "done", include score/signal
3. Summarize impact: Use professional trading analyst tone
4. Note trading pairs: Extract from coins[].symbols
Example Output Format

📡 Market Flash (3 items)
━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ [BTC] BlackRock ETF sees $500M single-day inflow
   📊 AI Score: 85 | Signal: LONG
   💡 Impact: Institutional accumulation, short-term bullish

2️⃣ [ETH] Vitalik announces L2 scaling roadmap  
   📊 AI Score: pending
   💡 Impact: Bullish for ETH ecosystem

3️⃣ [MACRO] Fed official hints at rate pause
   💡 Impact: Risk-on sentiment for crypto


Health Check

curl -s "https://web-production-666f44.up.railway.app/health"


Notes

• Data source: Tree of Alpha WebSocket (real-time)
• Update frequency: Millisecond-level
• Storage: Cloud PostgreSQL (persistent)
• AI ratings: Coming soon (status="pending" for now)
• Rate limits: None currently
