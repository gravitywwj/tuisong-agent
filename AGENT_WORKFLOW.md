# 🤖 Personal Literature Agent Workflow

This is a lightweight personal workflow for reading and summarizing literature. It is designed to guide AI coding assistants (such as Codex, Cursor, and Copilot) in processing academic papers extracted by MinerU.

## 📌 Objective
As an AI assistant, your task is to read lengthy Markdown papers extracted by MinerU and convert them into well-structured, highly professional academic reading notes **in Chinese**, written strictly from a third-person perspective. You must also ensure that all charts/images referenced in the text are absolutely authentic and never hallucinated.

## 📁 Directory Convention
- **Input Directory**: `data/input/{paper_folder}/` (Contains the original `full.md` and the extracted `images/` folder).
- **Output Directory**: `data/output/{paper_id}_summary.md`

## 🛠️ Execution Steps (Agent Step-by-Step)
Upon receiving a command from the user to process literature, execute the following steps in order:

1. **Read Input**:
   - Extract and read the `full.md` file in the target paper's folder.
   - Use commands like `ls` or read the directory structure to obtain the exact names of the actual image files in the `images/` directory. This establishes a reliable mapping of available images.
2. **Generate a Structured Summary (MUST BE IN CHINESE)**:
   - **Title**: Provide a bilingual (English and Chinese) title. The Chinese translation must be highly professional and tailored to the respective academic field (e.g., environmental science).
   - **Abstract**: Provide a direct, faithful academic translation of the original Abstract into Chinese. Keep the original essence without omitting the core structure. **Most importantly**: Strictly replace all 1st-person phrases (e.g., "we", "our study", "this paper") with 3rd-person academic narrations (e.g., "该研究", "科研作者", "文章指出").
   - **Methodology**: Describe the core research framework, model architecture, or experimental design thoroughly and professionally. If corresponding images of experimental setups, flowcharts, or formulas are found in the original document, you **must** link them in this paragraph with appropriate captions.
   - **Core Findings**: Divide into 3-5 logical subsections with clear subtitles. **Absolutely no colloquialisms or exaggerated rhetorical devices**. You MUST use extremely rigorous, objective, and scientific standard written academic language throughout. **Each subsection must be highly detailed and expanded to at least 500 Chinese characters**, deeply dissecting the internal mechanisms of the models, providing exhaustive quantitative data results, and offering profound comparative experimental analysis. Depend heavily on and cite relevant result charts/images.
   - **Typography & Style**: The content must be rich, and paragraphs must be full and coherent. The quality should strictly align with the standard of an extensive, high-tier journal reading note. Refuse simple bullet-point lists.
3. **Save Output**: Save the fully integrated Markdown summary as `{paper_id}_summary.md` in the `data/output/` directory.

## ⚠️ Mistakes to Avoid (Absolute Directives)
This directly impacts the document's usability. Strictly comply!
1. **No Hallucinated Images**:
   - For ANY image referenced in your summary using the format `![Caption](images/xxx.jpg)`, the corresponding path **MUST exist 100% authentically in the original `images/` directory**.
   - If a suitable image cannot be found, use pure text descriptions instead. **NEVER** fabricate fake paths like `images/figure1.jpg`.
2. **Enforce 3rd-Person Academic Narration**:
   - Original papers often use "we found," "our study," or "we propose."
   - When translating and rewriting into Chinese, **strictly prohibit** using first-person language such as: "我们发现" (we found), "我们的方法" (our method), "本研究" (this study), "本文" (this paper).
   - **Must be replaced with**: "该研究发现" (the research found), "所提方法" (the proposed method), "科研团队指出" (the research team pointed out), "该文章" (the article).