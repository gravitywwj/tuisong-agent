# Literature Agent Service

该目录为 `tuisong-agent` 的上游文献发现与调度服务，保持现有 `data/input -> data/output` 精读工作流不变。

## MVP 范围

1. 接收 Coze 工作流提交的每日检索任务。
2. 读取两个主题配置：
   - `hazardous_waste_ai`
   - `environmental_compliance_ai`
3. 后续接入 Scopus、ScienceDirect、Web of Science API。
4. 每次最多检索 100 篇，筛选 10 篇，精读 1–2 篇。
5. 全文可获取时转换为 Markdown，并交给仓库现有精读与 DOCX 工作流。
6. DOCX 通过邮件发送；全文不可获取时保留元数据并标记为待人工补充全文。

## 当前状态

当前提交只建立可部署的任务接收 API 和任务状态文件，不会伪造文献检索结果。API 凭据、检索器、全文获取、MinerU、排序模型、邮件发送将在后续阶段接入。

## 启动

```bash
cd literature_agent
cp .env.example .env
docker compose up --build
```

健康检查：

```text
GET /healthz
```

Coze 推荐调用：

```text
POST /api/v1/literature/jobs
```

为兼容当前已导出的 GET 型 Coze 模板，MVP 还提供：

```text
GET /api/v1/literature/trigger
```

生产环境应优先使用 POST，并通过 `X-Agent-Token` 请求头鉴权。
