# 个人文献精读与总结工作流 (Personal Literature Agent Workflow)

这是一个轻量级的个人 GitHub 仓库，设计用于配搭 AI 编程助手（如 Cursor, Copilot 等）自动执行学术文献的提炼与改写。

核心目标：基于大模型的语义理解，将 MinerU 提取的学术文献（Markdown 文本及图片）自动转换为排版规范、用词严谨、无第一人称视角的学术阅读笔记。项目注重极简与实用，主要依赖核心 Prompt 及自动化验证脚本实现质量控制。

## 🤖 直接用 Codex 启动

本仓库已经内置 `AGENTS.md`，用于告诉 Codex 如何自动识别输入、生成总结并执行校验。后续把项目从 GitHub 拉到本地后，只要在 Codex 中打开该仓库，再把 MinerU 输出文件夹放入 `data/input/`，即可直接用自然语言触发工作流，例如：

> 开始工作

或：

> 把 input 里的东西转化为推送

Codex 会按照 `AGENTS.md` 的规则扫描 `data/input/` 下的论文文件夹，读取 `full.md` 和真实存在的 `images/` 文件，生成 `data/output/<编号>_summary.md`，并运行验证脚本检查图片链接与第一人称表述。

## 📂 仓库结构
- **`AGENTS.md`**: Codex 自动执行入口，定义自然语言触发语、输入选择规则、输出约定、校验流程与图像引用规则。
- **`data/input/`**: 输入区，放置 MinerU 提取好的论文文件夹（内含 `full.md` 和 `images/` 图片包）。
- **`data/output/`**: 输出区，最终生成的阅读笔记会自动存于该目录。
- **`data/README.md`**: 输入输出目录的结构说明。
- **`AGENT_WORKFLOW.md`**: 🌟 核心控制指令（英文版），包含完整的文献处理与排版规范，强制约束模型的输出行为。
- **`AGENT_WORKFLOW_zh.md`**: 中文版的工作流规范说明，供使用者参考。
- **`src/`**: 包含两个轻量级的 Python 验证脚本，用于核验生成结果的准确性与格式合规性。

## 🚀 工作流：如何使用

1. 将包含 `full.md` 及 `images/` 的文件夹放入 `data/input/`。
2. 在 AI 助手对话框中输入指令：
   > "请遵循 `AGENT_WORKFLOW.md` 的规范，处理 `data/input/<编号>` 文件夹内的论文。"
3. 检查 `data/output/` 下生成的总结文档。
4. （可选）运行 `src/` 中的验证脚本，核验内容的客观视角及图像链接有效性。

## 🛠️ 质量验证脚本
提供了两个用于验证内容的 Python 脚本：
- **验证图像引用有效性**：`python src/check_images.py data/input/<编号>/images data/output/<编号>_summary.md`
- **核验客观学术人称（无第一人称）**：`python src/check_phrases.py data/output/<编号>_summary.md`
- **一次性执行全部校验**：`python src/validate_output.py <编号>`

这些脚本在发现问题时会返回非零退出码，便于 Codex、CI 或其他自动化流程判断输出是否合格。
