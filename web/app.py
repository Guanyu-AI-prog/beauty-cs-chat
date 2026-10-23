#!/usr/bin/env python3
"""花漾肌研 · 轻量中文客服界面

只做两件事：
  GET  /            -> 单文件前端（HTML/CSS/JS 全内联，无构建、无外部依赖）
  POST /api/chat    -> 代理到本机 RAG 后端 (127.0.0.1:8001)，原样透传 SSE 流

刻意保持轻量：不引入会话编排、不存库、不做鉴权，只负责"问一句、答一句、给出处"。
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import requests
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

HERE = Path(__file__).resolve().parent
UPSTREAM_BASE = os.getenv("RAG_BASE", "http://127.0.0.1:8001")
CHAT_URL = f"{UPSTREAM_BASE}/v1/chat/completions"
MODELS_URL = f"{UPSTREAM_BASE}/v1/models"
DEFAULT_MODEL = os.getenv("RAG_MODEL", "beauty-cs-rag")

app = FastAPI(title="花漾肌研 · 轻量客服界面")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(HERE / "index.html", headers={"Cache-Control": "no-cache"})


@app.get("/api/health")
def health():
    try:
        r = requests.get(f"{UPSTREAM_BASE}/health", timeout=5)
        return {"frontend": "ok", "upstream": r.json()}
    except Exception as exc:  # noqa: BLE001
        return JSONResponse({"frontend": "ok", "upstream": str(exc)}, status_code=503)


@app.get("/api/models")
def models():
    try:
        return requests.get(MODELS_URL, timeout=5).json()
    except Exception as exc:  # noqa: BLE001
        return JSONResponse({"error": str(exc)}, status_code=503)


@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    body.setdefault("model", DEFAULT_MODEL)
    body["stream"] = True
    payload = json.dumps(body, ensure_ascii=False).encode()

    def event_stream():
        try:
            with requests.post(
                CHAT_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
                stream=True,
                timeout=(10, 300),
            ) as resp:
                resp.raise_for_status()
                for chunk in resp.iter_content(chunk_size=None):
                    if chunk:
                        yield chunk
        except Exception as exc:  # noqa: BLE001
            err = json.dumps(
                {"error": {"message": f"后端不可用：{exc}", "type": "upstream_error"}},
                ensure_ascii=False,
            )
            yield f"data: {err}\n\n".encode()
            yield b"data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
