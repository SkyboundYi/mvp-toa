#!/usr/bin/env python3
"""
News API Server - MVP 版本
直接返回生肉数据
"""
import os
import json
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = "news.db"

# ============================================
# TODO: 未来在这里接入 Stripe 鉴权和 Token 扣费逻辑
# ============================================
def verify_token(token: str) -> bool:
    # TODO: 查 Supabase 验证 token
    # TODO: 检查用户余额
    # TODO: 扣费
    return True  # MVP: 暂时放行所有请求

# ============================================
# /news 接口
# ============================================
@app.route("/news", methods=["GET"])
def get_news():
    # TODO: 鉴权逻辑预留位
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not verify_token(token):
        return jsonify({"error": "Unauthorized"}), 401
    
    limit = request.args.get("limit", 10, type=int)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "SELECT raw_data, received_at FROM raw_news ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    # TODO: 未来在这里接入数据清洗逻辑
    # results = [clean_output(json.loads(r[0])) for r in rows]
    
    results = []
    for row in rows:
        results.append({
            "data": json.loads(row[0]),
            "received_at": row[1]
        })
return jsonify({
        "success": True,
        "count": len(results),
        "data": results
    })

# ============================================
# 健康检查
# ============================================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "ToA News MVP",
        "endpoints": ["/news", "/health"]
    })

# ============================================
# 启动
# ============================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
