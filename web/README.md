# 花漾肌研 · 轻量中文客服界面

替代 Open WebUI 的极简前端：单文件 HTML + 一个 uvicorn 进程，直连本机 RAG 后端
`~/rag-agent-system/core/openai_adapter.py`（`beauty-cs-rag`，免鉴权、支持 SSE）。

## 对比

| | Open WebUI（已删除） | 本项目 |
|---|---|---|
| 镜像/进程 | 6.38GB 镜像，常驻 **760MB** | 单进程 **31.5MB**，无镜像 |
| 界面语言 | 英文（该定制版未内置 i18n 语言包） | 全中文 |
| 功能面 | 工作区/文件夹/笔记/频道/自动化/记忆/评测… | 只保留问答 + 引用来源 + 历史 |
| 登录 | 需要鉴权（内置账号 `admin@localhost`/`admin`） | 无登录，直接用 |

## 组成

```
beauty-chat-web/
├── app.py                  FastAPI：GET / 发页面，POST /api/chat 代理 SSE，GET /api/health
├── index.html              单文件前端（HTML/CSS/JS 全内联，零依赖、零构建）
├── screenshots/            界面截图
└── /etc/systemd/system/beauty-chat-web.service   开机自启 + 崩溃自动拉起
```

## 运行

```bash
# 已托管给 systemd，无需手动操作
sudo systemctl status beauty-chat-web
sudo systemctl restart beauty-chat-web

# 手动跑（调试用）
cd ~/beauty-chat-web
~/rag-agent-system/venv/bin/uvicorn app:app --host 127.0.0.1 --port 3000 --app-dir ~/beauty-chat-web
```

访问：**http://127.0.0.1:3000**（仅监听本机）

环境变量：`RAG_BASE`（默认 `http://127.0.0.1:8001`）、`RAG_MODEL`（默认 `beauty-cs-rag`）

## 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/` | 前端页面 |
| GET | `/api/health` | 前端 + RAG 后端健康状况（含知识库篇数） |
| GET | `/api/models` | 模型列表 |
| POST | `/api/chat` | `{messages:[{role,content}]}` → SSE 流式返回 |

## 注意

- RAG 后端**只取最后一条 user 消息**作为检索 query，不做多轮上下文；前端因此只发送当前这一问。
- 回答末尾的 `参考来源：` 会被前端解析成金色引用标签。
- 会话历史存在浏览器 localStorage（最多 40 条），清空记录在侧边抽屉底部。
- 原 Open WebUI 的数据备份仍在 `/opt/webui-data`（266MB，含历史聊天与向量库），确认不需要可删。
