#!/usr/bin/env python3
"""Regenerate the source tables in README.md from sources.csv (idempotent).
Only the text between <!-- SOURCES:START --> and <!-- SOURCES:END --> is replaced."""
import csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- SOURCES:START -->", "<!-- SOURCES:END -->"
CATEGORIES = [
    ("官方博客/模型厂商", "Official blogs & labs"), ("X 账号", "X accounts"),
    ("中文媒体", "Chinese media"), ("英文媒体", "English media"),
    ("Newsletter", "Newsletters"), ("研究/论文", "Research & papers"),
    ("开源/工具", "Open source & tools"), ("社区聚合", "Communities & aggregators"),
    ("播客/视频", "Podcasts & video"), ("政策监管", "Policy & regulation"),
]
# sources.csv column names (as delivered by 报报) -> internal field
COLS = {"分类": "category", "名称": "name", "链接": "url", "类型": "type",
        "语言": "language", "更新频率": "frequency", "一句话推荐": "why"}
BSTART, BEND = "<!-- BADGE:START -->", "<!-- BADGE:END -->"
OSTART, OEND = "<!-- OVERVIEW:START -->", "<!-- OVERVIEW:END -->"

def replace_block(text, s, e, body):
    if text.count(s) != 1 or text.count(e) != 1 or text.index(s) > text.index(e):
        sys.exit(f"README.md must contain exactly one {s} ... {e} pair")
    head, rest = text.split(s, 1)
    _, tail = rest.split(e, 1)
    return f"{head}{s}\n{body}\n{e}{tail}"

def overview(rows):
    out = ["| 分类 Category | 源数量 Sources |", "|---|---|"]
    for zh, en in CATEGORIES:
        n = sum(1 for r in rows if r["category"] == zh)
        out.append(f"| {zh} · {en} | {n if n else '0（待补）'} |")
    out.append(f"| **合计 Total** | **{len(rows)}** |")
    return "\n".join(out)

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
            out += ["| 名称 Name | 类型 Type | 更新频率 Frequency | 语言 Lang | 为什么值得看 Why |", "|---|---|---|---|---|"]
            out += [f"| [{cell(r['name'])}]({cell(r['url'])}) | {cell(r['type'])} | {cell(r['frequency'])} | {cell(r['language'])} | {cell(r['why'])} |" for r in items]
        else:
            out.append("_待补 · Coming soon_")
        out += ["", CTA, ""]
    return "\n".join(out)

def main():
    with open(ROOT / "sources.csv", encoding="utf-8", newline="") as f:
        raw = list(csv.DictReader(f))
    missing = set(COLS) - set(raw[0].keys() if raw else COLS)
    if missing:
        sys.exit(f"sources.csv missing columns: {sorted(missing)}")
    rows = [{COLS[k]: v for k, v in r.items() if k in COLS} for r in raw]
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    new = replace_block(text, START, END, build(rows))
    new = replace_block(new, OSTART, OEND, overview(rows))
    badge = f"[![sources](https://img.shields.io/badge/sources-{len(rows)}-2ea44f)](#信源--sources)"
    new = replace_block(new, BSTART, BEND, badge)
    if new == text:
        print(f"README.md unchanged ({len(rows)} sources)")
    else:
        readme.write_text(new, encoding="utf-8")
        print(f"README.md updated ({len(rows)} sources)")

if __name__ == "__main__":
    main()
