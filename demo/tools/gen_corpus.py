#!/usr/bin/env python3
"""
花漾肌研 语料生成器
把种子数据渲染成 ~175 个 markdown 文档（类生产规模知识库）

用法:
  python3 tools/gen_corpus.py --out ~/rag-agent-system/data [--clean]
"""
import argparse
import shutil
from pathlib import Path

from seed_products import PRODUCTS, render_product
from seed_docs_a import POLICIES, CHANNELS, CAMPAIGNS
from seed_docs_b import TRAININGS, CASES, INGREDIENTS


def render_ingredient(t: tuple) -> str:
    name, cat, func, conc, pair, caution = t
    return f"""# 成分词典 · {name}

- **成分类别**：{cat}
- **作用概述**：{func}

## 作用解读
{func}。在护肤配方中，该成分的稳定性与配伍性由品牌实验室按标准工艺控制；不同产品中的添加量存在差异，具体以商品页"核心成分"栏为准。

## 建议浓度 / 用法
{conc}

## 搭配建议
{pair}

## 使用误区
- 误区一：浓度越高越好——多数成分存在适宜区间，过高可能增加刺激风险。
- 误区二：见效越快越好——皮肤代谢周期约 28 天，功效类成分建议按周期观察。
- 误区三：可以替代药品——化妆品成分不具备治疗作用，皮肤问题请就医。

## 注意事项
{caution}

## 常见问题（FAQ）
- 问：{name} 所有人都能用吗？答：多数成分温和适用，敏感肌建议先耳后测试；特殊人群（孕期/哺乳期）见上方"注意事项"。
- 问：和花漾肌研哪些产品相关？答：可在商品页搜索"{name}"查看含有该成分的在售商品，或咨询客服获取搭配建议。
- 问：出现刺痛泛红怎么办？答：立即停用该产品并清水洗净；持续不适请联系客服走售后通道。

## 品牌说明
本词条为花漾肌研内部成分知识库条目，仅用于客服培训与知识查询，不构成医疗建议或用药指导。
"""


def write_dir(out: Path, subdir: str, prefix: str, entries, renderer):
    d = out / subdir
    d.mkdir(parents=True, exist_ok=True)
    count, chars = 0, 0
    for e in entries:
        name = e["name"]
        text = renderer(e) if renderer is not None else e["text"]
        text = text if text.startswith("#") else f"# {prefix} · {name}\n\n{text}"
        safe = name.replace("/", "·").replace("\\", "·").replace(":", "：")
        fname = f"{prefix}-{safe}.md".replace(" ", "")
        (d / fname).write_text(text, encoding="utf-8")
        count += 1
        chars += len(text)
    return count, chars


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path.home() / "rag-agent-system" / "data"))
    ap.add_argument("--clean", action="store_true", help="先清空本生成器创建的子目录")
    args = ap.parse_args()
    out = Path(args.out).expanduser()

    mine = ["products", "policies", "channels", "campaigns", "training", "cases", "ingredients"]
    if args.clean:
        for d in mine:
            p = out / d
            if p.exists():
                shutil.rmtree(p)

    report = []
    c, ch = write_dir(out, "products", "商品", PRODUCTS, render_product)
    report.append(("商品（5线SKU）", c, ch))
    c, ch = write_dir(out, "policies", "政策", POLICIES, None)
    report.append(("政策细则", c, ch))
    c, ch = write_dir(out, "channels", "渠道", CHANNELS, None)
    report.append(("渠道差异", c, ch))
    c, ch = write_dir(out, "campaigns", "活动", CAMPAIGNS, None)
    report.append(("活动规则", c, ch))
    c, ch = write_dir(out, "training", "培训", TRAININGS, None)
    report.append(("培训手册", c, ch))
    c, ch = write_dir(out, "cases", "案例", CASES, None)
    report.append(("案例库", c, ch))

    # 成分词典（元组种子，专用渲染器）
    d = out / "ingredients"
    d.mkdir(parents=True, exist_ok=True)
    ic, ich = 0, 0
    for t in INGREDIENTS:
        text = render_ingredient(t)
        (d / f"成分-{t[0]}.md").write_text(text, encoding="utf-8")
        ic += 1
        ich += len(text)
    report.append(("成分词典", ic, ich))

    print("=" * 60)
    print(f"输出目录: {out}")
    total_files, total_chars = 0, 0
    for name, c, ch in report:
        print(f"  {name:<12} {c:>3} 篇   {ch:>7} 字")
        total_files += c
        total_chars += ch
    print("-" * 60)
    print(f"  新增合计      {total_files} 篇   {total_chars} 字")
    print(f"  预估 chunks（按 280 字/块）: ~{total_chars // 280}")
    print(f"  加上原有 3 篇 → 总计 {total_files + 3} 篇文档")
    print("=" * 60)


if __name__ == "__main__":
    main()
