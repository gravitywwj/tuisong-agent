# Data Directory

Put MinerU output folders under `data/input/`.

Expected input structure:

```text
data/input/{paper_id}/
  full.md
  images/
    ...
```

Codex writes generated Markdown summaries to:

```text
data/output/{paper_id}_summary.md
```

After Markdown validation, Codex also writes Word outputs to:

```text
data/output/{paper_id}_summary.docx
```

The Word reference template should be placed under:

```text
data/example format/
```

When using Codex, open this repository and say something like:

- `开始工作`
- `处理 input`
- `把 input 里的东西转化为推送`

The root `AGENTS.md` file tells Codex how to discover inputs, generate Markdown summaries, convert them to DOCX, and run validation.
