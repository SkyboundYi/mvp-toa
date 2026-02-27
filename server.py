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

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/")
def index():
    return jsonify({"service": "ToA News MVP"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
