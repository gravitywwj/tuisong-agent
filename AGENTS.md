# Codex Literature Workflow Instructions

This repository is a reusable Codex workflow for converting academic papers extracted by MinerU into polished Chinese reading notes or publication-ready Markdown drafts.

## Natural-Language Triggers

When the user says any phrase with the following intent, treat it as a request to run this workflow:

- "开始工作"
- "处理 input"
- "处理输入目录"
- "把 input 里的东西转化为推送"
- "生成文献总结"
- "生成阅读笔记"
- "转成推送"

Do not stop at explaining the workflow. Unless the user explicitly asks for a plan only, inspect `data/input/`, process the eligible paper folders, write outputs, and run validation.

## Directory Contract

- Input folders live under `data/input/{paper_id}/`.
- Each input folder should contain:
  - `full.md`
  - `images/` with MinerU-extracted figures, tables, formulas, or page images
- Output files must be written to `data/output/{paper_id}_summary.md`.

An eligible input folder is any direct child of `data/input/` that contains `full.md`.

## Paper Selection Rules

- If the user names a paper id or folder, process that folder only.
- If the user asks to process `input`, `全部`, or all papers, process every eligible folder.
- If the user says a vague trigger such as "开始工作" and there is exactly one eligible folder, process it.
- If the user says a vague trigger and there are multiple eligible folders, process every eligible folder that does not already have a matching output file.
- If an output file already exists, skip it unless the user explicitly asks to overwrite or regenerate.
- If no eligible folder exists, briefly explain the required structure and stop.

## Required Workflow

For each selected paper:

1. Read `data/input/{paper_id}/full.md`.
2. List the exact files under `data/input/{paper_id}/images/`.
3. Generate a Chinese structured academic reading note according to `AGENT_WORKFLOW.md`.
4. Save the result as `data/output/{paper_id}_summary.md`.
5. Run validation:
   - `python src/check_images.py data/input/{paper_id}/images data/output/{paper_id}_summary.md`
   - `python src/check_phrases.py data/output/{paper_id}_summary.md`
   - or `python src/validate_output.py {paper_id}`
6. If validation fails, revise the output and rerun validation before final response.

## Writing Standards

- Output must be in Chinese unless the user explicitly asks otherwise.
- Keep a rigorous academic tone.
- Rewrite first-person and author-perspective phrases into third-person academic narration.
- Do not use "我们发现", "我们的方法", "本研究", or "本文".
- Do not use colloquial, promotional, exaggerated, or self-media style phrasing unless the user explicitly asks for a lighter style.
- When the user asks for "推送", produce clean Markdown suitable for publication while preserving the same academic rigor.

## Image Rules

- Never fabricate image paths.
- Before inserting any image reference, confirm that the filename exists in the input `images/` folder.
- Markdown image links must use the format `![caption](images/exact_filename.ext)` unless the user asks for a different export layout.
- If no reliable matching image exists, describe the result in text instead of inventing an image.

## Final Response

After completing the workflow, report:

- Which input folders were processed.
- Which output files were created or updated.
- Whether validation passed.
- Any skipped folders and the reason.
