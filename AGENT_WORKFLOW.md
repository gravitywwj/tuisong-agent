# 🤖 Personal Literature Agent Workflow

This is a lightweight personal workflow for reading and summarizing literature. It is designed to guide AI coding assistants (such as Codex, Cursor, and Copilot) in processing academic papers extracted by MinerU.

## 📌 Objective
As an AI assistant, your task is to read lengthy Markdown papers extracted by MinerU and convert them into well-structured, highly professional academic reading notes **in Chinese**, written strictly from a third-person perspective. You must also ensure that all charts/images referenced in the text are absolutely authentic and never hallucinated.

## 📁 Directory Convention
- **Input Directory**: `data/input/{paper_folder}/` (Contains the original `full.md` and the extracted `images/` folder).
- **Markdown Output**: `data/output/{paper_id}_summary.md`
- **Word Output**: `data/output/{paper_id}_summary.docx`

## 🛠️ Execution Steps (Agent Step-by-Step)
Upon receiving a command from the user to process literature, execute the following steps in order:

1. **Read Input**:
   - Extract and read the `full.md` file in the target paper's folder.
   - Use commands like `ls` or read the directory structure to obtain the exact names of the actual image files in the `images/` directory. This establishes a reliable mapping of available images.
2. **Generate a Structured Summary (MUST BE IN CHINESE)**:
   - **Title**: Preserve the original English paper title exactly. Provide a faithful, professional Chinese translation as the second title line. Concision requirements apply to section headings, not to the original paper title.
   - **Abstract**: Provide a direct, faithful academic translation of the original Abstract into Chinese. Keep the original essence without omitting the core structure. **Most importantly**: Strictly replace all 1st-person phrases (e.g., "we", "our study", "this paper") with 3rd-person academic narrations (e.g., "该研究", "科研作者", "文章指出").
   - **Methodology**: Describe the core research framework, model architecture, or experimental design thoroughly and professionally. If corresponding images of experimental setups, flowcharts, or formulas are found in the original document, you **must** link them in this paragraph with appropriate captions.
   - **Core Findings**: Divide into no more than 4 logical subsections with concise subtitles, preferably within 18 Chinese characters. Do not force a one-section-one-figure structure; each subsection may include multiple related figures or tables if they support the same argument. **Absolutely no colloquialisms or exaggerated rhetorical devices**. Use rigorous, objective, scientific written language throughout. **Each subsection must be highly detailed and expanded to at least 500 Chinese characters**, deeply dissecting mechanisms, key quantitative evidence, and comparative analysis. Depend on and cite relevant result charts/images.
   - **Conclusion**: End with a single section titled `结论`. Do not write a standalone `环境意义`, `精读结论`, or `精度结论` section. The conclusion should synthesize the conceptual contribution and mechanism rather than repeat prediction accuracy metrics.
   - **Typography & Style**: The content must be rich, and paragraphs must be full and coherent. The quality should strictly align with the standard of an extensive, high-tier journal reading note. Refuse simple bullet-point lists.
3. **Save Markdown Output**: Save the fully integrated Markdown summary as `{paper_id}_summary.md` in the `data/output/` directory.
4. **Convert to DOCX**: After Markdown validation passes, run `python src/md_to_docx.py {paper_id}` to generate `{paper_id}_summary.docx` using the reference template under `data/example format/`.
5. **Validate DOCX**: Run `python src/check_docx.py {paper_id}` and fix any title, DOI, or image insertion issue before delivery.

## ⚠️ Mistakes to Avoid (Absolute Directives)
This directly impacts the document's usability. Strictly comply!
1. **No Hallucinated Images**:
   - For ANY image referenced in your summary using the format `![Caption](images/xxx.jpg)`, the corresponding path **MUST exist 100% authentically in the original `images/` directory**.
   - If a suitable image cannot be found, use pure text descriptions instead. **NEVER** fabricate fake paths like `images/figure1.jpg`.
2. **Enforce 3rd-Person Academic Narration**:
   - Original papers often use "we found," "our study," or "we propose."
   - When translating and rewriting into Chinese, **strictly prohibit** using first-person language such as: "我们发现" (we found), "我们的方法" (our method), "本研究" (this study), "本文" (this paper).
   - **Must be replaced with**: "该研究发现" (the research found), "所提方法" (the proposed method), "科研团队指出" (the research team pointed out), "该文章" (the article).
3. **No Template Leakage in DOCX**:
   - Generated Word documents must not keep the reference template's original paper title, DOI, body content, figures, cover image, or hidden media.
   - Do not auto-generate a cover. If MinerU does not provide a usable cover, leave the cover absent/blank for manual editing.
   - Insert Markdown images in their corresponding positions and use the Markdown captions as centered Word figure captions.
   - If a reliable graphical abstract image exists in the MinerU input, insert it immediately after the Chinese abstract section.
