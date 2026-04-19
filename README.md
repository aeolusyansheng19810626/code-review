# AI 工具箱

基于 Groq 的软件工程师效率工具集合。项目提供统一 Streamlit 入口，也保留部分工具的独立 CLI / Web 页面，适合用于代码审查、技术方案分析、论文精读、会议纪要、SQL 优化和正则表达式生成。

## 上传信息

- 上传者：Codex
- 本次更新内容：新增统一入口 `app.py`，新增 `paper_reader`、`meeting_minutes`、`sql_optimizer`、`regex_generator` 工具模块，并调整 `code_review` 与 `tech_decision` 的根目录运行兼容性。

## 功能列表

| 工具 | 入口 Key | 功能 |
| --- | --- | --- |
| 代码 Review | `code_review` | 粘贴或上传代码，AI 输出评分、优点、问题、修复建议和总体建议 |
| 技术方案决策 | `tech_decision` | 根据需求生成候选技术方案，或对已有方案做多维度评估 |
| 论文精读 | `paper_reader` | 上传 PDF 或粘贴论文文本，生成结构化中文精读报告 |
| 会议纪要 | `meeting_minutes` | 粘贴会议记录，生成完整纪要或简洁要点摘要 |
| SQL 优化 | `sql_optimizer` | 分析 SQL 查询性能，给出索引建议、结构优化和优化后 SQL |
| 正则生成器 | `regex_generator` | 根据自然语言需求生成正则表达式、解释和使用示例 |

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

## 本次新增/修改功能

- 新增统一 Streamlit 入口 `app.py`，通过侧边栏切换所有工具。
- 新增 `paper_reader`：支持 PDF / 文本论文精读，输出 Markdown 报告。
- 新增 `meeting_minutes`：支持完整会议纪要和简洁摘要两种模式。
- 新增 `sql_optimizer`：支持 MySQL、PostgreSQL、SQLite、Oracle、SQL Server 的 SQL 优化建议。
- 新增 `regex_generator`：根据自然语言需求生成正则表达式、解释和示例。
- 修改 `code_review/app.py`：改为浅色 Streamlit 风格，降低视觉刺激。
- 修改 `code_review/reviewer.py` 和 `tech_decision/advisor.py`：兼容从项目根目录按包导入运行。
- 修改新增工具的模型调用：统一使用 `GROQ_API_KEY`，不依赖 Anthropic / Claude。

## 注意事项

- `.env`、缓存文件、截图和本地测试文件不应提交到仓库。
- PDF 文本提取依赖 `pdfplumber`，扫描版 PDF 可能无法直接提取文字。
- 代码审查和技术方案决策依赖模型输出 JSON，如模型返回格式异常，页面会显示错误信息。
