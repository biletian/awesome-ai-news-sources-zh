#!/usr/bin/env python3
"""Regenerate the source tables in README.md from sources.csv (idempotent).
Only the text between <!-- SOURCES:START --> and <!-- SOURCES:END --> is replaced."""
import csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- SOURCES:START -->", "<!-- SOURCES:END -->"
CATEGORIES = [
    ("官方博客", "Official blogs"), ("模型厂 X", "Model labs on X"),
    ("中文媒体", "Chinese media"), ("聚合站", "Aggregators"),
    ("社区", "Communities (Reddit / HN / Discord)"), ("论文", "Papers"),
    ("GitHub 热榜", "GitHub trending"), ("演讲播客", "Talks & podcasts"),
]
CTA = "> 懒得自己刷？[直接看知一刻](https://zhiyike.cn) · Too busy to scroll? [Just read Zhiyike](https://zhiyike.cn)"

def cell(s):
    return (s or "").strip().replace("|", "\\|").replace("\n", " ")

def build(rows):
    known = {c for c, _ in CATEGORIES}
    bad = sorted({r["category"] for r in rows} - known)
    if bad:
        sys.exit(f"unknown category in sources.csv: {bad}")
    out = []
    for zh, en in CATEGORIES:
        items = sorted((r for r in rows if r["category"] == zh), key=lambda r: r["name"].lower())
        out += [f"### {zh} · {en}", ""]
        if items:
            out += ["| 名称 Name | 更新频率 Frequency | 语言 Lang | 为什么值得看 Why |", "|---|---|---|---|"]
            out += [f"| [{cell(r['name'])}]({cell(r['url'])}) | {cell(r['frequency'])} | {cell(r['language'])} | {cell(r['why'])} |" for r in items]
        else:
            out.append("_待补 · Coming soon_")
        out += ["", CTA, ""]
    return "\n".join(out)

def main():
    with open(ROOT / "sources.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    if text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END):
        sys.exit("README.md must contain exactly one START/END marker pair")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    new = f"{head}{START}\n{build(rows)}\n{END}{tail}"
    if new == text:
        print(f"README.md unchanged ({len(rows)} sources)")
    else:
        readme.write_text(new, encoding="utf-8")
        print(f"README.md updated ({len(rows)} sources)")

if __name__ == "__main__":
    main()
