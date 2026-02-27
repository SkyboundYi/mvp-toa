# MVP-ToA

# 📡 ToA News API

[English](#english) | [中文](#中文)

---

# English

Real-time cryptocurrency news API with millisecond-level market intelligence, running 24/7 in the cloud.

## 🎯 How to Use

### Method 1: Give to OpenClaw (Recommended)

1. Give `openclaw-skill/toa-news/SKILL.md` to OpenClaw
2. Chat directly:
   - "Get me the latest 10 news"
   - "Search BTC related news"
   - "Find news containing OpenAI"

### Method 2: Call API Directly

**Base URL**: `https://web-production-666f44.up.railway.app`

---

## 📌 API Endpoints

### GET /news — Simple Fetch

```bash
curl "https://web-production-666f44.up.railway.app/news?limit=10"
```

### POST /news_search — Advanced Search (Recommended)

```bash
# Get latest news
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}'

# Keyword search
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"q": "OpenAI", "limit": 10, "page": 1}'

# Filter by coin
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["BTC", "ETH"], "limit": 10, "page": 1}'
```

### Search Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | ✅ | Results per page (1-100) |
| `page` | integer | ✅ | Page number |
| `q` | string | ❌ | Keyword search |
| `coins` | string[] | ❌ | Filter by coins `["BTC", "ETH"]` |
| `hasCoin` | boolean | ❌ | Only return news with coins |

### GET /health — Health Check

```bash
curl "https://web-production-666f44.up.railway.app/health"
```

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User / AI Agent                       │
│              "Get me BTC related news"                   │
└─────────────────────┬───────────────────────────────────┘
                      │ Read SKILL.md
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   OpenClaw (AI Assistant)                │
│              Call API based on instructions              │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP Request
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 Railway (Cloud 24/7)                     │
│  ┌──────────────┐              ┌──────────────┐         │
│  │   worker     │              │     web      │         │
│  │  WebSocket   │              │  Flask API   │         │
│  │  Listen ToA  │              │ /news_search │         │
│  └──────┬───────┘              └──────┬───────┘         │
│         └────────────┬────────────────┘                 │
│                      ▼                                  │
└─────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    Supabase                             │
│                  PostgreSQL                             │
│               Persistent Storage                        │
└─────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Tree of Alpha WebSocket                    │
│                Real-time News Source                    │
└─────────────────────────────────────────────────────────┘
```

### Components

| Component | Function |
|-----------|----------|
| **worker.py** | 24/7 listen ToA WebSocket, store to DB |
| **server.py** | Flask API, provide /news and /news_search |
| **Supabase** | PostgreSQL cloud database, persistent storage |
| **Railway** | Cloud deployment, 24/7 running |
| **SKILL.md** | AI Agent instruction manual |

---

## 📁 Project Structure

```
mvp-toa/
├── worker.py              # WebSocket listener, store data
├── server.py              # Flask API, return data
├── requirements.txt       # Python dependencies
├── Procfile               # Railway deployment config
└── openclaw-skill/
    └── toa-news/
        └── SKILL.md       # OpenClaw skill instruction
```

---

## 📊 Response Example

```json
{
  "success": true,
  "total": 190,
  "page": 1,
  "limit": 10,
  "data": [
    {
      "id": "2027386976161136831",
      "text": "CoinDesk (@CoinDesk)",
      "body": "Amazon just committed $50B to OpenAI...",
      "newsType": "direct",
      "engineType": "news",
      "link": "https://twitter.com/CoinDesk/status/...",
      "ts": 1772201697111,
      "receivedAt": "2026-02-27T14:14:57.711390+00:00",
      "coins": [
        {
          "symbol": "WLD",
          "market_type": "spot",
          "match": "body",
          "symbols": [
            {"exchange": "binance-futures", "symbol": "WLDUSDT"},
            {"exchange": "binance", "symbol": "WLDUSDT"}
          ]
        }
      ],
      "aiRating": {
        "status": "pending",
        "score": null,
        "grade": null,
        "signal": null
      }
    }
  ]
}
```

---

## 🚀 Roadmap

### ✅ Done
- [x] WebSocket real-time listener
- [x] Cloud 24/7 deployment (Railway)
- [x] PostgreSQL persistence (Supabase)
- [x] /news endpoint
- [x] /news_search advanced search
- [x] Keyword search
- [x] Coin filter
- [x] Pagination
- [x] SKILL.md (OpenClaw integration)

### ⏳ TODO
- [ ] AI Rating (score/grade/signal)
- [ ] User Authentication (API Token)
- [ ] Stripe Billing
- [ ] Data Cleaning Layer

---

## 📝 License

MIT

---
---
---

# 中文

实时加密货币新闻 API，毫秒级市场情报，24/7 云端运行。

## 🎯 使用方法

### 方式一：交给 OpenClaw（推荐）

1. 将 `openclaw-skill/toa-news/SKILL.md` 交给 OpenClaw
2. 直接对话：
   - "给我最新10条新闻"
   - "搜索 BTC 相关新闻"
   - "查找包含 OpenAI 的新闻"

### 方式二：直接调用 API

**Base URL**: `https://web-production-666f44.up.railway.app`

---

## 📌 API 接口

### GET /news — 简单获取

```bash
curl "https://web-production-666f44.up.railway.app/news?limit=10"
```

### POST /news_search — 高级搜索（推荐）

```bash
# 获取最新新闻
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}'

# 关键词搜索
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"q": "OpenAI", "limit": 10, "page": 1}'

# 币种过滤
curl -X POST "https://web-production-666f44.up.railway.app/news_search" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["BTC", "ETH"], "limit": 10, "page": 1}'
```

### 搜索参数

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| `limit` | integer | ✅ | 每页数量 (1-100) |
| `page` | integer | ✅ | 页码 |
| `q` | string | ❌ | 关键词搜索 |
| `coins` | string[] | ❌ | 币种过滤 `["BTC", "ETH"]` |
| `hasCoin` | boolean | ❌ | 仅返回有币种的新闻 |

### GET /health — 健康检查

```bash
curl "https://web-production-666f44.up.railway.app/health"
```

---

## 🏗 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户 / AI Agent                       │
│              "给我 BTC 相关最新新闻"                      │
└─────────────────────┬───────────────────────────────────┘
                      │ 读取 SKILL.md
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   OpenClaw (AI 助手)                     │
│              根据说明书调用 API                           │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP 请求
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 Railway (云端 24/7)                      │
│  ┌──────────────┐              ┌──────────────┐         │
│  │   worker     │              │     web      │         │
│  │  WebSocket   │              │  Flask API   │         │
│  │  监听 ToA    │              │ /news_search │         │
│  └──────┬───────┘              └──────┬───────┘         │
│         └────────────┬────────────────┘                 │
│                      ▼                                  │
└─────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    Supabase                             │
│                  PostgreSQL                             │
│                   永久存储                               │
└─────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Tree of Alpha WebSocket                    │
│                  实时新闻源                              │
└─────────────────────────────────────────────────────────┘
```

### 组件说明

| 组件 | 作用 |
|-----|------|
| **worker.py** | 24/7 监听 ToA WebSocket，实时入库 |
| **server.py** | Flask API，提供 /news 和 /news_search |
| **Supabase** | PostgreSQL 云数据库，永久存储 |
| **Railway** | 云端部署，24/7 运行 |
| **SKILL.md** | AI Agent 调用说明书 |

---

## 📁 项目结构

```
mvp-toa/
├── worker.py              # WebSocket 监听，存数据
├── server.py              # Flask API，返数据
├── requirements.txt       # Python 依赖
├── Procfile               # Railway 部署配置
└── openclaw-skill/
    └── toa-news/
        └── SKILL.md       # OpenClaw 技能说明书
```

---

## 📊 返回数据示例

```json
{
  "success": true,
  "total": 190,
  "page": 1,
  "limit": 10,
  "data": [
    {
      "id": "2027386976161136831",
      "text": "CoinDesk (@CoinDesk)",
      "body": "Amazon just committed $50B to OpenAI...",
      "newsType": "direct",
      "engineType": "news",
      "link": "https://twitter.com/CoinDesk/status/...",
      "ts": 1772201697111,
      "receivedAt": "2026-02-27T14:14:57.711390+00:00",
      "coins": [
        {
          "symbol": "WLD",
          "market_type": "spot",
          "match": "body",
          "symbols": [
            {"exchange": "binance-futures", "symbol": "WLDUSDT"},
            {"exchange": "binance", "symbol": "WLDUSDT"}
          ]
        }
      ],
      "aiRating": {
        "status": "pending",
        "score": null,
        "grade": null,
        "signal": null
      }
    }
  ]
}
```

---

## 🚀 开发路线图

### ✅ 已完成
- [x] WebSocket 实时监听
- [x] 云端 24/7 部署 (Railway)
- [x] PostgreSQL 持久化 (Supabase)
- [x] /news 接口
- [x] /news_search 高级搜索
- [x] 关键词搜索
- [x] 币种过滤
- [x] 分页支持
- [x] SKILL.md (OpenClaw 集成)

### ⏳ 待开发
- [ ] AI 评分 (score/grade/signal)
- [ ] 用户鉴权 (API Token)
- [ ] Stripe 计费
- [ ] 数据清洗层

---

## 📝 License

MIT
