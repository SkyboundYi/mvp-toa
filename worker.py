#!/usr/bin/env python3
"""
ToA WebSocket Listener - MVP 版本
直接搬运，原样存储
"""
import os
import json
import sqlite3
import time
from datetime import datetime
import websocket

# ============================================
# 配置
# ============================================
TOA_WSS_URL = os.getenv("TOA_WSS_URL", "wss://news.treeofalpha.com/ws")
TOA_API_KEY = os.getenv("TOA_API_KEY", "")
DB_PATH = "news.db"

# ============================================
# 数据库初始化
# ============================================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_data TEXT NOT NULL,
            received_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized")

# ============================================
# 存储原始数据
# ============================================
def save_raw(data: dict):
    # TODO: 未来在这里接入数据清洗和重构逻辑
    # cleaned = clean_and_transform(data)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO raw_news (raw_data, received_at) VALUES (?, ?)",
        (json.dumps(data), datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    print(f"💾 Saved to DB")

# ============================================
# WebSocket 回调
# ============================================
def on_message(ws, message):
    try:
        data = json.loads(message)
        print(f"📥 Received: {str(data)[:100]}...")
        save_raw(data)
    except Exception as e:
        print(f"❌ Error: {e}")

def on_error(ws, error):
    print(f"❌ WS Error: {error}")

def on_close(ws, code, msg):
    print(f"🔌 WS Closed: {code} {msg}")

def on_open(ws):
    print("✅ WS Connected to ToA")

# ============================================
# 主函数
# ============================================
def main():
    init_db()
    print(f"🚀 Connecting to {TOA_WSS_URL}")
    
    ws = websocket.WebSocketApp(
        TOA_WSS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    while True:
        try:
            ws.run_forever()
        except KeyboardInterrupt:
            print("👋 Shutting down...")
            break
        except Exception as e:
            print(f"❌ Reconnecting in 5s... {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
