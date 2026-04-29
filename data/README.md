# Data Directory

Put MinerU output folders under `data/input/`.

Expected input structure:

```text
data/input/{paper_id}/
  full.md
  images/
    ...
```

Codex writes generated summaries to:

```text
data/output/{paper_id}_summary.md
```

When using Codex, open this repository and say something like:

- `开始工作`
- `处理 input`
- `把 input 里的东西转化为推送`

The root `AGENTS.md` file tells Codex how to discover inputs, generate summaries, and run validation.
