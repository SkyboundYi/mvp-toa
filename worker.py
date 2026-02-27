cat > worker.py << 'EOF'
#!/usr/bin/env python3
import os, json, time
from datetime import datetime
import websocket
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_news (
            id SERIAL PRIMARY KEY,
            raw_data JSONB NOT NULL,
            received_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database initialized")

def save_raw(data):
    # TODO: 未来在这里接入数据清洗逻辑
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO raw_news (raw_data) VALUES (%s)", (json.dumps(data),))
    conn.commit()
    cur.close()
    conn.close()
    print("💾 Saved")

def on_message(ws, msg):
    try:
        data = json.loads(msg)
        print(f"📥 {str(data)[:80]}...")
        save_raw(data)
    except Exception as e:
        print(f"❌ {e}")

def on_open(ws):
    print("✅ Connected to ToA")

def on_error(ws, err):
    print(f"❌ WS Error: {err}")

def on_close(ws, code, msg):
    print(f"🔌 Closed: {code}")

def main():
    if not DATABASE_URL:
        print("❌ DATABASE_URL not set!")
        return
    init_db()
    print("🚀 Connecting to ToA WebSocket...")
    ws = websocket.WebSocketApp(
        "wss://news.treeofalpha.com/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    while True:
        try:
            ws.run_forever()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"🔄 Reconnecting in 5s... {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
EOF
