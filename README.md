# AI 工具箱

基于 Groq 的软件工程师效率工具集合。项目提供统一 Streamlit 入口，也保留部分工具的独立 CLI / Web 页面，适合用于代码审查、技术方案分析、论文精读、会议纪要、SQL 优化、正则表达式生成、技术周报和需求拆解。

## 上传信息

- 上传者：Codex
- 本次提交者：Codex
- 本次提交内容：新增 `weekly_report`、`task_breakdown` 工具模块；为所有 AI 结果增加实际使用模型显示；同步更新统一入口和 README。

## 功能列表

| 工具 | 入口 Key | 功能 |
| --- | --- | --- |
| 代码 Review | `code_review` | 粘贴或上传代码，AI 输出评分、优点、问题、修复建议和总体建议 |
| 技术方案决策 | `tech_decision` | 根据需求生成候选技术方案，或对已有方案做多维度评估 |
| 论文精读 | `paper_reader` | 上传 PDF 或粘贴论文文本，生成结构化中文精读报告 |
| 会议纪要 | `meeting_minutes` | 粘贴会议记录，生成完整纪要或简洁要点摘要 |
| SQL 优化 | `sql_optimizer` | 分析 SQL 查询性能，给出索引建议、结构优化和优化后 SQL |
| 正则生成器 | `regex_generator` | 根据自然语言需求生成正则表达式、解释和使用示例 |
| 技术周报 | `weekly_report` | 输入本周工作内容，生成格式规范的技术周报 |
| 需求拆解 | `task_breakdown` | 输入需求描述，拆解为含优先级、工时、依赖关系的任务清单 |

## 项目结构

```text
ai-tools/
├── app.py                    # 统一 Streamlit 入口
├── code_review/              # AI 代码审查工具
│   ├── reviewer.py
│   ├── prompts.py
│   ├── cli.py
│   └── app.py
├── tech_decision/            # AI 技术方案决策工具
│   ├── advisor.py
│   ├── prompts.py
│   ├── cli.py
│   └── app.py
├── paper_reader/             # 论文精读工具
│   ├── reader.py
│   ├── prompts.py
│   ├── cli.py
│   └── app.py
├── meeting_minutes/          # 会议纪要工具
│   ├── summarizer.py
│   ├── prompts.py
│   ├── cli.py
│   └── app.py
├── sql_optimizer/            # SQL 查询优化工具
│   ├── optimizer.py
│   └── prompts.py
├── regex_generator/          # 正则表达式生成工具
│   ├── generator.py
│   └── prompts.py
├── weekly_report/            # 技术周报生成工具
│   ├── generator.py
│   └── prompts.py
├── task_breakdown/           # 需求拆解工具
│   ├── generator.py
│   └── prompts.py
├── requirements.txt
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

如果 Windows 上 `streamlit` 命令不在 PATH 中，请使用 `py -m streamlit` 方式启动。

### 2. 配置 API Key

在项目根目录创建 `.env`：

```env
GROQ_API_KEY=your_key
```

所有 AI 工具默认使用 Groq API，不需要 `ANTHROPIC_API_KEY`。

### 3. 启动统一入口

```bash
cd C:\ai-tools
py -m streamlit run app.py
```

如果默认端口被占用：

```bash
py -m streamlit run app.py --server.port 8503
```

打开浏览器访问：

```text
http://localhost:8501
```

或访问你指定的端口。

## 独立工具用法

### 代码 Review

```bash
cd C:\ai-tools
py -m streamlit run code_review\app.py
```

CLI：

```bash
cd C:\ai-tools\code_review
python cli.py review ..\test_code.py
```

### 技术方案决策

```bash
cd C:\ai-tools
py -m streamlit run tech_decision\app.py
```

CLI：

```bash
cd C:\ai-tools\tech_decision
python cli.py generate "我们需要一个支持千万级日活的实时聊天系统"
python cli.py evaluate "使用 Redis 存储聊天记录，MySQL 存储用户信息"
```

### 论文精读

```bash
cd C:\ai-tools
py -m streamlit run paper_reader\app.py
```

CLI：

```bash
cd C:\ai-tools
py -m paper_reader.cli path\to\paper.pdf -o paper_report.md
```

### 会议纪要

```bash
cd C:\ai-tools
py -m streamlit run meeting_minutes\app.py
```

CLI：

```bash
cd C:\ai-tools
py -m meeting_minutes.cli meeting.txt --mode full -o meeting_minutes.md
py -m meeting_minutes.cli meeting.txt --mode brief -o meeting_brief.md
```

## 模型策略

工具默认使用 Groq 模型级联策略。优先调用高能力模型，失败后逐步降级到备用或测试模型，提高可用性：

```text
openai/gpt-oss-120b
→ openai/gpt-oss-20b
→ qwen/qwen3-32b
→ meta-llama/llama-4-scout-17b-16e-instruct
→ llama-3.3-70b-versatile
→ llama-3.1-8b-instant
```

页面和 CLI 会在结果上方显示本次实际使用的模型，例如：

```text
使用模型：openai/gpt-oss-120b
```

如果高级模型失败并降级，这里会显示最终成功返回结果的 fallback 模型。

## 本次新增/修改功能

- 新增 `weekly_report`：输入本周工作、下周计划等信息，生成 Markdown 技术周报。
- 新增 `task_breakdown`：输入需求、技术栈和团队规模，生成结构化任务拆解清单。
- 修改统一入口 `app.py`：侧边栏新增 `技术周报` 和 `需求拆解`，目前共 8 个工具。
- 修改所有 Groq 工具：在结果上方展示实际使用模型，便于确认推理来源。
- 保持模型策略统一：所有新增工具使用 `GROQ_API_KEY` 和 Groq 模型级联，不依赖 Anthropic / Claude。

## 注意事项

- `.env`、缓存文件、截图和本地测试文件不应提交到仓库。
- PDF 文本提取依赖 `pdfplumber`，扫描版 PDF 可能无法直接提取文字。
- 代码审查和技术方案决策依赖模型输出 JSON，如模型返回格式异常，页面会显示错误信息。
