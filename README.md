# 个人文献精读与总结工作流 (Personal Literature Agent Workflow)

这是一个极轻量级的个人 GitHub 代码仓库，专为搭配 AI 编程助手（如 Cursor, Copilot, Codex 等）使用而设立。

它的核心诉求只有一个：利用大模型，将 MinerU 提取出来的一堆庞杂的学术文献（Markdown + 碎块图片），提炼改写为整洁、准确、去除了第一人称视角的学术阅读总结笔记。

该项目彻底摒弃了复杂的管道和长篇大论的架构设计，回归极简与实用，主要依靠核心 Prompt 以及最基本的内容查错脚本，让你每次查阅文献都能轻松拿走直接可用的干货。

## 📂 仓库结构
- **`data/input/`**: 输入区，放置 MinerU 提取好的论文文件夹（内含 `full.md` 和 `images/` 图片包）。
- **`data/output/`**: 输出区，AI 最终生成的 MD 阅读笔记会自动落在该目录下。
- **`AGENT_WORKFLOW.md`**: 🌟 给 AI 助手的最高法律指南，内含完整的处理规则和防错准则。
- **`src/`**: 轻量级工具箱，仅提供两份几百 KB 大小的 Python 脚本，辅助确认模型有没有胡说八道。

## 🚀 工作流：如何使用

1. 把 MinerU 抽取的文件夹放入 `data/input/`。
2. 在 Cursor 或 Copilot 会话窗口中，直接输入指令，并 @ 本项目的说明书：
   > "请查阅 `AGENT_WORKFLOW.md` 的规范，帮我处理 `data/input/480` 文件夹里的论文"
3. 等待几分钟，模型会自动生成总结至 `data/output/`！
4. （可选防错）运行 `src/` 里面的脚本扫一眼生成的文件是否有第一人称等错误写法。

## 🛠️ 轻巧检查脚本
为了治理 AI 的通病（胡编乱造路径和第一人称视角的机器口吻），这里提供了两个短小精悍的 Python 脚本。
- **验证图像引用的存活性**：`python src/check_images.py data/input/480/images data/output/480_summary.md`
- **扫描第一人称视角敏感词**：`python src/check_phrases.py data/output/480_summary.md`