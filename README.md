# 花漾肌研 · 电商客服 RAG + 轻量中文界面

> 虚拟品牌「花漾肌研」的美妆护肤客服知识库 + 评测流水线 + 一个 30MB 的轻量中文聊天前端。
> **全部数据为合成数据**（品牌 / 商品 / 政策均虚构），用于 RAG 客服开发与评测演练。

本仓库包含两部分：

| 目录 | 内容 |
|---|---|
| `demo/` | 知识库语料（178 篇 md）、客服 System Prompt、语料生成器、评测集与评测流水线 |
| `web/` | 单文件中文聊天界面（HTML/CSS/JS 全内联）+ 一个 uvicorn 代理进程 |

底层框架代码在独立仓库 [`Guanyu-AI-prog/rag-agent-system`](https://github.com/Guanyu-AI-prog/rag-agent-system)（框架与项目分离，本仓库不复制框架代码）。

---

## 架构

```
浏览器
  │  中文对话界面（零依赖、零构建）
  ▼
:3000  web/app.py（uvicorn，~31MB）
  │  POST /api/chat  →  SSE 流式透传
  ▼
:8001  rag-agent-system/core/openai_adapter.py（OpenAI 兼容适配器，免鉴权）
  │  SimpleRAG.query()
  ├── 检索：bge-large-zh-v1.5 向量召回（top-3）+ bge-reranker-v2-m3 重排
  ├── 提示词：demo/prompts/beauty_system_prompt.md（美妆客服 System Prompt）
  └── 生成：DeepSeek-V3（SiliconFlow）
  ▼
带「参考来源」的回答（SSE 流式返回）
```

## 快速开始

### 1. 准备 RAG 后端

```bash
git clone https://github.com/Guanyu-AI-prog/rag-agent-system.git
cd rag-agent-system && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt

cd ../beauty-cs-chat/demo
cp .env.example .env          # 填入你的 SiliconFlow Key
../../rag-agent-system/venv/bin/python ../../rag-agent-system/core/openai_adapter.py
```

首次运行需要构建向量库（下载嵌入模型并索引 178 篇语料），耗时取决于机器。

### 2. 启动中文界面

```bash
cd web
python3 -m venv venv && ./venv/bin/pip install fastapi uvicorn requests
./venv/bin/uvicorn app:app --host 127.0.0.1 --port 3000 --app-dir .
```

打开 **http://127.0.0.1:3000** 即可使用。

环境变量：

| 变量 | 默认值 | 说明 |
|---|---|---|
| `RAG_BASE` | `http://127.0.0.1:8001` | RAG 后端地址 |
| `RAG_MODEL` | `beauty-cs-rag` | 模型名 |

## 为什么是自建界面

最初的方案是套 Open WebUI，实测问题：

- **英文**：该定制版镜像未内置 i18n 语言包，改配置也无法切换中文。
- **过重**：镜像 6.38GB，常驻 760MB；而真正提供能力的只有 `beauty-cs-rag` 这一个模型。
- **功能冗余**：工作区 / 文件夹 / 笔记 / 频道 / 自动化 / 记忆等与"问一句答一句"的客服场景无关。

因此改为自建单页前端：**常驻约 31MB，全中文，零依赖零构建**，只保留问答、引用来源与本地历史记录。界面保留了实用的细节：

- 回答末尾的 `参考来源：` 自动解析成金色引用标签（可追溯到具体 md 文件）
- 内置极简 Markdown 渲染（列表 / 加粗 / 行内代码）
- 快捷提问、Enter 发送 / Shift+Enter 换行、流式逐字输出
- 会话历史存浏览器 localStorage，移动端自适应

## 目录结构

```
beauty-cs-chat/
├── web/
│   ├── app.py              FastAPI：GET / 发页面，POST /api/chat 代理 SSE
│   ├── index.html          单文件前端（HTML/CSS/JS 全内联）
│   └── screenshots/        界面截图
├── docs/
│   └── 2026-10-23-工作纪要.md   当日重点、踩坑记录与待办
└── demo/
    ├── .env.example        配置模板（真实 .env 不入库）
    ├── prompts/            美妆客服 System Prompt
    ├── tools/              语料生成器（可复现、可扩规模）
    ├── data/               知识库语料 178 篇 md
    ├── eval/               评测集与评测流水线
    ├── results/            评测输出
    └── legacy/             历史版本留存
```

## 数据说明

`demo/data/` 下 178 篇语料、`eval/` 下的评测集与 `results/` 下的评测输出**全部为合成数据**，品牌「花漾肌研」及其商品、政策、会员规则均虚构，不对应任何真实品牌或真实业务规则。

## 许可

MIT，见 [LICENSE](LICENSE)。
