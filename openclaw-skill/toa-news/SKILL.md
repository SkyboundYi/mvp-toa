---
name: toa-news
description: 实时加密货币新闻 API。支持关键词搜索、币种过滤、来源筛选。毫秒级更新，6551 兼容格式。
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📡"
    tags:
      - crypto
      - news
      - trading
      - api
    os:
      - darwin
      - linux
      - win32
  version: 2.0.0
---

# ToA Crypto News Agent

你是一个**加密货币新闻检索 Agent**。你通过调用 ToA News API 获取毫秒级市场情报。

---

## Base URL

```
https://web-production-666f44.up.railway.app
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | 健康检查 |
| `/news` | GET | 简单获取 |
| `/news_search` | POST | **核心端点** - 所有高级查询 |

---

## Discovery (发现接口)

### get_news_sources — 获取新闻来源类别

当前支持的来源类型:
- `Bloomberg`, `Reuters`, `COINTELEGRAPH`, `COINDESK`
- `direct` (Twitter/社交媒体)
- `FINANCE WIRE`, `BARRONS`, `DLNEWS`

### list_news_types — 引擎类型列表

| engineType | Description |
|------------|-------------|
| `news` | 主流新闻媒体 |
| `listing` | 上市/下架公告 |
| `onchain` | 链上数据分析 |
| `meme` | Meme 币相关 |
| `market` | 市场数据 |

---

## POST /news_search — Payload Schema

### 完整参数表

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | ✅ | - | 每页结果数 (1-100) |
| `page` | integer | ✅ | - | 页码 (从 1 开始) |
| `q` | string | ❌ | null | 全文关键词搜索 |
| `coins` | string[] | ❌ | null | 币种符号数组，如 `["BTC", "ETH"]` |
| `hasCoin` | boolean | ❌ | false | 仅返回包含币种标记的新闻 |
| `source` | string | ❌ | null | 来源筛选，如 `"Bloomberg"` |
| `engineType` | string | ❌ | null | 引擎类型: `news`/`listing`/`onchain`/`meme`/`market` |
| `startTime` | integer | ❌ | null | 开始时间 (Unix 毫秒) |
| `endTime` | integer | ❌ | null | 结束时间 (Unix 毫秒) |

---

## Intent → Payload 映射

### 1. get_latest_news — 获取最新

```bash
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}'
```

### 2. search_news — 关键词搜索

```bash
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"q": "bitcoin ETF", "limit": 10, "page": 1}'
```

### 3. search_news_by_coin — 币种搜索

```bash
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["BTC", "ETH"], "limit": 10, "page": 1}'
```

### 4. get_news_by_source — 来源筛选

```bash
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"q": "Bloomberg", "limit": 10, "page": 1}'
```

### 5. get_news_by_engine — 引擎类型筛选

```bash
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"q": "onchain", "limit": 10, "page": 1}'
```

### 6. search_news_by_date — 日期范围

```bash
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"startTime": 1772150400000, "endTime": 1772236800000, "limit": 20, "page": 1}'
```

---

## Response Structure

### 顶层响应

```json
{
  "success": true,
  "total": 130,
  "page": 1,
  "limit": 10,
  "quota": "unlimited",
  "data": [NewsArticle, ...]
}
```

### NewsArticle 对象

```json
{
  "id": "2027363213940293775",
  "text": "Yi He (@heyibinance)",
  "body": "Binance is actively exploring talent...",
  "newsType": "direct",
  "engineType": "news",
  "link": "https://twitter.com/heyibinance/status/...",
  "ts": 1772196031975,
  "receivedAt": "2026-02-27T12:40:32.615200+00:00",
  "coins": [
    {
      "symbol": "BNB",
      "market_type": "spot",
      "match": "title",
      "symbols": [
        {"exchange": "binance-futures", "symbol": "BNBUSDT"},
        {"exchange": "binance", "symbol": "BNBUSDT"}
      ]
    }
  ]
}
```

### 字段说明

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | 唯一文章 ID |
| `text` | string | 标题/来源名称 |
| `body` | string | 完整内容文本 |
| `newsType` | string | 来源类型 |
| `engineType` | string | 引擎类别 |
| `link` | string | 原文 URL |
| `ts` | integer | Unix 时间戳 (毫秒) |
| `receivedAt` | string | ISO 8601 接收时间 |
| `coins` | array | 检测到的币种及交易对 |
| `coins[].symbol` | string | 币种符号 |
| `coins[].market_type` | string | 市场类型 (spot/futures) |
| `coins[].match` | string | 匹配位置 (title/body) |
| `coins[].symbols` | array | 可交易对列表 |

---

## Standard Operating Procedures (SOP)

### SOP-1: 市场概览

**触发**: "最新新闻"、"市场动态"、"发生了什么"

**Payload**:
```json
{"limit": 10, "page": 1}
```

**输出格式**:
```
📡 市场快讯 (10条)
━━━━━━━━━━━━━━━━━━

1️⃣ [BTC] 标题...
   💡 影响: 简要分析

2️⃣ [ETH] 标题...
   💡 影响: 简要分析
```

---

### SOP-2: 特定币种研究

**触发**: "BTC 新闻"、"ETH 消息"、"SOL 发生了什么"

**Payload**:
```json
{"coins": ["BTC"], "limit": 20, "page": 1}
```

**输出格式**:
```
🔍 BTC 相关新闻 (共 X 条)
━━━━━━━━━━━━━━━━━━

利多:
• 新闻1...
• 新闻2...

利空:
• 新闻3...

判断: [看多/看空/中性] + 理由
```

---

### SOP-3: 来源筛选

**触发**: "Bloomberg 报道"、"Reuters 新闻"、"主流媒体"

**Payload**:
```json
{"q": "Bloomberg", "limit": 10, "page": 1}
```

---

### SOP-4: 链上数据新闻

**触发**: "链上数据"、"onchain"、"巨鲸动向"

**Payload**:
```json
{"q": "onchain", "limit": 10, "page": 1}
```

---

### SOP-5: 关键词搜索

**触发**: 任意话题 "ETF"、"Binance"、"监管"、"空投"

**Payload**:
```json
{"q": "用户关键词", "limit": 10, "page": 1}
```

---

### SOP-6: 只看有币种的新闻

**触发**: "有交易机会的新闻"、"币种相关"

**Payload**:
```json
{"hasCoin": true, "limit": 10, "page": 1}
```

---

## Health Check

```bash
curl -s "https://web-production-666f44.up.railway.app/health"
```

返回: `{"status": "ok"}`

---

## Notes

- **数据源**: Tree of Alpha WebSocket (实时)
- **更新频率**: 毫秒级
- **存储**: Cloud PostgreSQL (24/7 持久化)
- **Rate Limit**: 当前无限制
