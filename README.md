# MVP-ToA

Tree of Alpha 新闻数据 MVP 管道

## 架构


ToA WebSocket → worker.py (http://worker.py/) → SQLite → server.py (http://server.py/) → API


## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 终端1: 启动搬运工
python worker.py

# 终端2: 启动API
python server.py

# 测试
curl http://localhost:8000/news?limit=5

环境变量

| 变量          | 说明               |
| ----------- | ---------------- |
| TOA_WSS_URL | ToA WebSocket 地址 |
| TOA_API_KEY | ToA API Key      |
| PORT        | API 端口 (默认 8000) |

TODO

• [ ] 数据清洗逻辑
• [ ] Stripe 鉴权
• [ ] Supabase 用户管理
• [ ] Vercel 部署

点 **Commit changes**

---

## ✅ 完成后的结构


mvp-toa/
├── README.md (http://readme.md/)
├── .gitignore
├── requirements.txt
├── worker.py (http://worker.py/)      ← WS 监听
└── server.py (http://server.py/)      ← HTTP API


---

**一个一个创建，完成后告诉我，我们继续下一步！** 🚀
