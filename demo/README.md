# 花漾肌研 · 电商客服 RAG 评测项目（beauty-cs-demo）

> 虚拟品牌「花漾肌研」的美妆护肤客服知识库 + 评测集 + 评测流水线。
> **全部数据为合成数据**（品牌/商品/政策均虚构），用于 RAG 客服开发与评测演练。
> 关联：框架 `~/rag-agent-system`（框架与项目分离，本项目不复制框架代码）

## 架构：框架与项目分离

```
~/rag-agent-system/          ← 框架（纯代码，不装本项目数据）
~/beauty-cs-demo/            ← 本项目（数据/提示词/评测全部自包含）
   运行时通过 .env 引用框架：
   DATA_DIR / VECTOR_DB_PATH / COLLECTION_NAME / PROMPT_FILE
```

## 目录结构

```
beauty-cs-demo/
├── README.md
├── .env                       ← 本项目配置（绝对路径指向本目录）
├── prompts/
│   └── beauty_system_prompt.md   ← 美妆客服 System Prompt（框架通过 PROMPT_FILE 加载）
├── tools/                     ← 语料生成器（可复现、可扩规模）
│   ├── seed_products.py       ← 68 商品种子 + 渲染器
│   ├── seed_docs_a.py         ← 政策/渠道/活动种子
│   ├── seed_docs_b.py         ← 培训/案例/成分种子
│   └── gen_corpus.py          ← 渲染主程序
├── data/                      ← 知识库语料（178 篇 md）
│   ├── 商品资料.md / 售后政策.md / 客服Q&A.md   ← v1 手写三件套
│   ├── products/ policies/ channels/ campaigns/ training/ cases/ ingredients/  ← 批量生成
│   └── eval/questions.json    ← v1 题库（30题源文件，现行版见 eval/beauty_questions.py）
├── eval/
│   ├── beauty_questions.py    ← 50 题评测集（带 ground truth + anti_keywords）
│   └── eval_beauty_local.py   ← 评测主程序（5 维度 + 双段耗时 + 完整回答）
├── results/                   ← 评测结果 JSON
├── vector_db/                 ← 向量库（593 chunks，ChromaDB）
└── legacy/                    ← 旧版归档（kb_v0_originals / rag_agent_system.env.bak）
```

## 运行

```bash
# 1. 重建语料（可选：改种子后重新生成）
python3 tools/gen_corpus.py --out ~/beauty-cs-demo/data --clean

# 2. 重建向量库（需要 SILICONFLOW_API_KEY，走 .env）
cd ~/beauty-cs-demo
set -a && source .env && set +a
~/rag-agent-system/venv/bin/python ~/rag-agent-system/vector/build_vectors.py --force

# 3. 单题测试
printf '积雪草面膜一盒几片，多少钱？\n' | ~/rag-agent-system/venv/bin/python ~/rag-agent-system/core/simple_rag.py

# 4. 全量评测（50 题，约 3-4 分钟）
~/rag-agent-system/venv/bin/python eval/eval_beauty_local.py
```

## 评测结果（归档）

| 版本 | 规模 | 题数 | 平均分 |
|---|---|---|---|
| v1 基线 | 31 chunks | 30 | 5.49 |
| v2 | 31 chunks | 30 | 8.86 |
| v3 | 593 chunks | 50 | 8.94 |

详见 Obsidian：`03-RAG/项目案例/电商客服RAG (beauty_cs_demo).md`

---
*创建：2026-10-08*
