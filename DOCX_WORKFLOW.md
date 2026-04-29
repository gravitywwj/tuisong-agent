# DOCX Conversion Workflow

This workflow extends the existing Markdown literature note pipeline by converting each validated Markdown summary into a Word document that follows the reference template under `data/example format/`.

## Template Analysis

The current reference template is:

```text
data/example format/数据稀缺条件下的跨流域水质预测：基于深度表征学习的方法.docx
```

The template is a one-section A4 document with these reusable formatting traits:

- Page setup: A4, left/right margins 3.17 cm, top/bottom margins 2.54 cm.
- Body text: `Normal` style, Chinese font 宋体, Latin font Times New Roman, 12 pt, justified alignment, first-line indent about two Chinese characters, fixed 20 pt line spacing.
- Section headings: `Heading 1`, 黑体, 14 pt, bold, no first-line indent.
- Subsection headings: `Heading 2`, bold, no first-line indent.
- Figure layout: centered inline pictures, width about 14.65 cm, followed by centered captions using the template `Title` style at 10.5 pt.
- Footer block: disclosure line, DOI source link, contact line, and reading-note author line.

The first large object in the template is an image of the source article header, not editable Word text. The converter does not reuse it and does not generate a replacement cover by default. If MinerU does not provide a usable cover, the DOCX starts from the editable title section so a cover can be added manually later. The generated DOCX is created from a blank document with template-like styles so that hidden media from the reference template cannot remain in `word/media/`.

## Commands

After the Markdown summary passes existing validation:

```powershell
python src\md_to_docx.py <paper_id>
python src\check_docx.py <paper_id>
```

Default paths:

```text
Markdown input: data/output/<paper_id>_summary.md
Image source:    data/input/<paper_id>/images/
DOCX output:    data/output/<paper_id>_summary.docx
```

## Conversion Rules

- The converter loads the template `.docx`, clears its body, and keeps the template styles and page setup.
- The converter does not generate a cover by default. Use `--generate-cover` only when an auto-generated article-info cover is explicitly desired.
- The first two Markdown H1 headings become the English and Chinese title lines under the Word `题目` heading.
- Markdown `##` headings become Word `Heading 1`; Markdown `###` headings become Word `Heading 2`.
- `## 主要内容与核心发现` is normalized to `主要内容` to match the reference template.
- Markdown images must point to real files under `images/`; each image is inserted where it appears in Markdown and receives the Markdown alt text as its caption.
- If MinerU exposes a reliable graphical abstract image before the main article body, it is inserted immediately after the Chinese abstract section and captioned `图文摘要`.
- DOI is extracted from the Markdown, `full.md`, or MinerU JSON files. If no DOI is found, the converter leaves the DOI footer out rather than fabricating one.
- The template title, template DOI, template cover, and hidden template media must not remain in the generated DOCX.
