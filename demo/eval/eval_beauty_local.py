#!/usr/bin/env python3
"""
花漾肌研 客服 Demo — 本地评测（beauty-cs-demo 项目版）
- 复用框架代码：~/rag-agent-system（可用 RAG_FRAMEWORK 环境变量覆盖）
- 本项目数据：../data  向量库：../vector_db  Prompt：../prompts/beauty_system_prompt.md
- 50 题 × 5 维度（召回/耗时/完整性/准确率/幻觉），记录检索/生成双段耗时 + 完整回答

用法：
    cd ~/beauty-cs-demo
    ~/rag-agent-system/venv/bin/python eval/eval_beauty_local.py
"""
import sys, os, json, time
from pathlib import Path
from datetime import datetime

BEAUTY = Path(__file__).resolve().parents[1]          # ~/beauty-cs-demo
FRAMEWORK = Path(os.getenv("RAG_FRAMEWORK", str(Path.home() / "rag-agent-system"))).expanduser()
os.chdir(BEAUTY)

for _p in (str(FRAMEWORK), str(FRAMEWORK / "core"), str(FRAMEWORK / "infra"), str(BEAUTY / "eval")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dotenv import load_dotenv
load_dotenv(BEAUTY / ".env")

from simple_rag import SimpleRAG
from beauty_questions import BEAUTY_QUESTIONS


def run_evaluation():
    print("=" * 70)
    print(f"花漾肌研 客服 Demo 评测 — {len(BEAUTY_QUESTIONS)} 道题 × 5 个维度（含检索耗时）")
    print(f"框架: {FRAMEWORK} | 项目: {BEAUTY}")
    print("=" * 70)

    rag = SimpleRAG()
    results = []

    for i, item in enumerate(BEAUTY_QUESTIONS):
        q = item["q"]
        print(f"\n[{i+1}/{len(BEAUTY_QUESTIONS)}] {q}")

        start = time.time()
        try:
            result = rag.query(q)
            elapsed = time.time() - start
            answer = result.answer if hasattr(result, "answer") else str(result)
            sources = result.sources if hasattr(result, "sources") else []
            retrieval_time = getattr(result, "retrieval_time", 0.0)
            success = result.success if hasattr(result, "success") else True
        except Exception as e:
            elapsed = time.time() - start
            answer = f"ERROR: {e}"
            sources = []
            retrieval_time = 0.0
            success = False

        gen_time = max(0.0, elapsed - retrieval_time)
        print(f"  回答: {answer[:120]}...")
        print(f"  检索: {retrieval_time:.2f}s | 生成: {gen_time:.2f}s | 总计: {elapsed:.2f}s")

        results.append({
            "id": item["id"],
            "question": q,
            "category": item["category"],
            "answer": answer,                    # 完整回答（不截断）
            "sources_count": len(sources),
            "retrieval_time": round(retrieval_time, 3),
            "generation_time": round(gen_time, 3),
            "elapsed": round(elapsed, 3),
            "success": success,
            "expected_keywords": item["expected_keywords"],
            "expected_answer": item["expected_answer"],
            "anti_keywords": item["anti_keywords"],
        })

    return results


def score_results(results):
    print("\n" + "=" * 70)
    print("评分结果")
    print("=" * 70)

    scored = []
    category_scores = {}

    for r in results:
        answer = r["answer"]
        expected_kw = r["expected_keywords"]
        anti_kw = r["anti_keywords"]

        kw_hits = sum(1 for kw in expected_kw if kw in answer)
        kw_ratio = kw_hits / len(expected_kw) if expected_kw else 1
        recall_score = round(kw_ratio * 10, 1)

        elapsed = r["elapsed"]
        if elapsed <= 3: latency_score = 10
        elif elapsed <= 6: latency_score = 8
        elif elapsed <= 10: latency_score = 6
        elif elapsed <= 15: latency_score = 4
        else: latency_score = 2

        alen = len(answer)
        if alen >= 100: completeness_score = 10
        elif alen >= 50: completeness_score = 8
        elif alen >= 20: completeness_score = 6
        elif alen >= 5: completeness_score = 4
        else: completeness_score = 2

        hallucination_hits = [kw for kw in anti_kw if kw in answer]
        accuracy_score = recall_score
        if hallucination_hits:
            accuracy_score = max(0, accuracy_score - len(hallucination_hits) * 3)

        hallucination_score = 10
        if hallucination_hits:
            hallucination_score = max(0, 10 - len(hallucination_hits) * 5)
        fail_markers = ["抱歉", "未找到", "查询失败", "ERROR", "错误"]
        if any(m in answer for m in fail_markers):
            hallucination_score = max(0, hallucination_score - 3)

        total = round((recall_score + latency_score + completeness_score
                       + accuracy_score + hallucination_score) / 5, 1)

        scored.append({
            "id": r["id"], "question": r["question"], "category": r["category"],
            "recall": recall_score, "latency": latency_score,
            "completeness": completeness_score, "accuracy": accuracy_score,
            "hallucination": hallucination_score, "total": total,
            "retrieval_time": r["retrieval_time"],
            "generation_time": r["generation_time"],
            "elapsed": r["elapsed"],
            "kw_hits": f"{kw_hits}/{len(expected_kw)}",
            "anti_hits": hallucination_hits,
            "answer": r["answer"],
            "expected_answer": r["expected_answer"],
        })

        cat = r["category"]
        category_scores.setdefault(cat, []).append(total)
        print(f"[{r['id']:>2}] {cat} | 总分 {total} | 召回 {recall_score} "
              f"| 检索 {r['retrieval_time']:.2f}s | 生成 {r['generation_time']:.2f}s "
              f"| 幻觉 {'⚠' if hallucination_hits else '✓'}")

    avg = round(sum(s["total"] for s in scored) / len(scored), 2)
    avg_retrieval = round(sum(s["retrieval_time"] for s in scored) / len(scored), 2)
    avg_gen = round(sum(s["generation_time"] for s in scored) / len(scored), 2)
    avg_total_time = round(sum(s["elapsed"] for s in scored) / len(scored), 2)

    print("\n" + "=" * 70)
    print(f"平均总分: {avg}/10")
    print(f"平均检索耗时: {avg_retrieval}s | 平均生成耗时: {avg_gen}s | 平均总耗时: {avg_total_time}s")
    for cat, vals in category_scores.items():
        print(f"  {cat}: {round(sum(vals)/len(vals), 2)} ({len(vals)}题)")
    print("=" * 70)

    summary = {
        "avg_total": avg,
        "avg_retrieval_time": avg_retrieval,
        "avg_generation_time": avg_gen,
        "avg_total_time": avg_total_time,
        "category_scores": {k: round(sum(v)/len(v), 2) for k, v in category_scores.items()},
    }
    return scored, summary


def main():
    t0 = datetime.now()
    results = run_evaluation()
    scored, summary = score_results(results)

    out = {
        "meta": {
            "name": "花漾肌研 客服 Demo 评测 v3",
            "time": t0.strftime("%Y-%m-%d %H:%M:%S"),
            "framework": str(FRAMEWORK),
            "collection": os.getenv("COLLECTION_NAME", "beauty_cs_demo"),
            "llm_model": os.getenv("LLM_MODEL", ""),
            **summary,
        },
        "details": scored,
    }
    outdir = BEAUTY / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / f"beauty_eval_{t0.strftime('%Y%m%d_%H%M%S')}.json"
    outfile.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\n结果已保存: {outfile}")


if __name__ == "__main__":
    main()
