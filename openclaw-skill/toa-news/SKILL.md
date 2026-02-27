---
name: toa-news
description: Real-time crypto news from Tree of Alpha WebSocket. Millisecond-level market updates, project announcements, and macro news with coin tagging.
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
  version: 1.0.0
---

# ToA Crypto News Skill

Query real-time crypto news from the Tree of Alpha WebSocket feed. Data is collected via millisecond-level WebSocket and stored in cloud database.

**Base URL**: `https://web-production-666f44.up.railway.app`

---

## News Operations

### 1. Get Latest News

Fetch the most recent news articles.

```bash
curl -s "https://web-production-666f44.up.railway.app/news?limit=10"

2. Get News with Custom Limit

curl -s "https://web-production-666f44.up.railway.app/news?limit=50"

News Parameters

| Parameter | Type    | Required | Description                        |
| --------- | ------- | -------- | ---------------------------------- |
| limit     | integer | no       | Max results to return (default 10) |


Data Structures

News Article

{
  "data": {
    "_id": "unique-article-id",
    "title": "Source Name (@handle)",
    "body": "Full article content or tweet text",
    "coin": "BTC",
    "link": "https://twitter.com/...",
    "time": 1772180907371,
    "type": "direct",
    "suggestions": [
      {
        "coin": "BTC",
        "symbols": [
          {"exchange": "binance-futures", "symbol": "BTCUSDT"},
          {"exchange": "binance", "symbol": "BTCUSDT"}
        ]
      }
    ]
  },
  "received_at": "2026-02-27T08:28:27.993890+00:00"
}

Key Fields

| Field       | Description                          |
| ----------- | ------------------------------------ |
| title       | Source name and handle               |
| body        | Full content text                    |
| coin        | Primary coin mentioned               |
| link        | Original source URL                  |
| time        | Unix timestamp (milliseconds)        |
| suggestions | Coins detected with exchange symbols |


Common Workflows

Quick Market Overview

curl -s "https://web-production-666f44.up.railway.app/news?limit=5" | jq '.data[] | {title: .data.title, body: .data.body, coin: .data.coin}'

Get Trading Pairs for News

curl -s "https://web-production-666f44.up.railway.app/news?limit=10" | jq '.data[].data.suggestions[]?.symbols'


Data Processing Guidelines

When presenting news to users:

1. Extract key info: title, body, coin, link
2. Summarize impact: Use professional trading analyst tone
3. Remove noise: Strip technical fields like _id, icon, info
4. Highlight actionable: Note relevant trading pairs from suggestions
Example Output Format

📡 Market Flash (3 items)
━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ [BTC] BlackRock ETF sees $500M single-day inflow
   💡 Impact: Institutional accumulation, short-term bullish

2️⃣ [ETH] Vitalik announces L2 scaling roadmap  
   💡 Impact: Bullish for ETH ecosystem, watch ARB/OP

3️⃣ [MACRO] Fed official hints at rate pause
   💡 Impact: Risk-on sentiment for crypto


Health Check

curl -s "https://web-production-666f44.up.railway.app/health"

Returns: {"status": "ok"}


Notes

• Data source: Tree of Alpha WebSocket (real-time)
• Update frequency: Millisecond-level
• Storage: Cloud PostgreSQL (persistent)
• Rate limits: None currently
