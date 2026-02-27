import os
import json
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route("/news")
def get_news():
    limit = request.args.get("limit", 10, type=int)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT raw_data, received_at FROM raw_news ORDER BY id DESC LIMIT %s", (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    results = [{"data": r[0], "received_at": r[1].isoformat()} for r in rows]
    return jsonify({"success": True, "count": len(results), "data": results})

@app.route("/news_search", methods=["POST"])
def news_search():
    body = request.get_json() or {}
    limit = body.get("limit", 10)
    page = body.get("page", 1)
    q = body.get("q", None)
    coins = body.get("coins", None)
    has_coin = body.get("hasCoin", False)
    offset = (page - 1) * limit
    
    base_query = "SELECT raw_data, received_at FROM raw_news WHERE 1=1"
    params = []
    
    if q:
        base_query += " AND (raw_data::jsonb->>'title' ILIKE %s OR raw_data::jsonb->>'body' ILIKE %s OR raw_data::jsonb->>'en' ILIKE %s)"
        q_pattern = f"%{q}%"
        params.extend([q_pattern, q_pattern, q_pattern])
    
    if coins and isinstance(coins, list) and len(coins) > 0:
        coin_conditions = []
        for coin in coins:
            coin_conditions.append("raw_data::jsonb->>'coin' ILIKE %s")
            params.append(f"%{coin}%")
            coin_conditions.append("raw_data::text ILIKE %s")
            params.append(f"%\"{coin}\"%")
        base_query += " AND (" + " OR ".join(coin_conditions) + ")"
    
    if has_coin:
        base_query += " AND raw_data::jsonb->>'coin' IS NOT NULL AND raw_data::jsonb->>'coin' != ''"
    
    base_query += " ORDER BY id DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(base_query, tuple(params))
    rows = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) FROM raw_news")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    data = []
    for row in rows:
        raw = row[0]
        received_at = row[1]
        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except:
                raw = {}
        
        item = {
            "id": raw.get("_id", ""),
            "text": raw.get("title", raw.get("en", "")),
            "body": raw.get("body", ""),
            "newsType": raw.get("sourceName", raw.get("type", "Twitter")),
            "engineType": "news",
            "link": raw.get("link", raw.get("url", "")),
            "coins": [],
            "aiRating": {"score": None, "grade": None, "signal": None, "status": "pending", "summary": None, "enSummary": None},
            "ts": raw.get("time", 0),
            "receivedAt": received_at.isoformat() if received_at else None
        }
        
        if raw.get("coin"):
            item["coins"].append({"symbol": raw.get("coin"), "market_type": "spot", "match": "title"})
        
        suggestions = raw.get("suggestions", [])
        for sug in suggestions:
            if sug.get("coin") and sug.get("coin") != raw.get("coin"):
                item["coins"].append({"symbol": sug.get("coin"), "market_type": "spot", "match": "body", "symbols": sug.get("symbols", [])})
        
        data.append(item)
    
    return jsonify({"success": True, "data": data, "limit": limit, "page": page, "total": total, "quota": "unlimited"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/")
def index():
    return jsonify({"service": "ToA News API", "version": "2.0", "endpoints": ["/news", "/news_search", "/health"]})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
