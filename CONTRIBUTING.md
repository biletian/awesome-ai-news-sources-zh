# 贡献指南 · Contributing

## 收录标准 · Criteria
- 链接可达，近 90 天内有更新 / Reachable and updated within the last 90 days.
- 与 AI 资讯直接相关，优先一手出处（官方博客、官方账号）/ AI-focused; first-hand sources preferred.
- 一句「为什么值得看」，只写事实，不贬低别家 / One factual "why" line; no disparaging others.
- 不收未核实、刷量或付费推广的源 / No unverified, spammy, or paid-promotion sources.

## 怎么加 · How to add
1. 只改 `sources.csv`（列：`分类,名称,链接,类型,语言,更新频率,一句话推荐`），`分类` 必须是 README 里的十类之一。
   Edit `sources.csv` only; `category` must be one of the ten in README.
2. 运行 / Run `python3 scripts/gen_table.py`，README 会自动更新。
3. 提 PR，写明这个源为什么值得看 / Open a PR explaining why the source is worth reading.

停更或 404 的源会移出并记录在 `REMOVED.md`。Dead or stale sources are removed and logged in `REMOVED.md`.

By contributing you agree your contribution is released under CC0 1.0.
