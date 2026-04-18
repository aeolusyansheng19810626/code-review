# AI Tools & Code Reviewer

基于 Groq 的 AI 开发工具集，旨在辅助开发者进行代码审查和架构决策。

## 项目结构
```
ai-tools/
├── code_review/         # AI 代码审查工具
│   ├── reviewer.py      # 核心逻辑 (5-tier 级联模型)
│   ├── cli.py           # 彩色命令行界面 (支持语法高亮)
│   └── app.py           # 现代化 Web UI
├── tech_decision/       # AI 技术决策顾问
│   ├── advisor.py       # 架构师逻辑 (5-tier 级联模型)
│   ├── cli.py           # 决策分析 CLI (带可视化评分条)
│   └── app.py           # 带雷达图的 Web UI
├── requirements.txt
└── README.md
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置 API Key
在根目录创建 `.env`：
```env
GROQ_API_KEY=your_key
```

### 3. 使用 AI 代码审查 (Code Reviewer)
```bash
cd code_review
# CLI: 审查文件或代码
python cli.py review ../test_code.py
# Web UI
streamlit run app.py
```

### 4. 使用 AI 技术决策顾问 (Tech Decision Advisor)
#### CLI 模式
```bash
cd tech_decision
# 模式1: 方案生成 (对比 3 个方案)
python cli.py generate "我们需要一个支持千万级日活的实时聊天系统"
# 模式2: 方案评估 (量化评估维度)
python cli.py evaluate "使用 Redis 存储聊天记录，MySQL 存储用户信息"
```

#### Web UI 模式
```bash
cd tech_decision
streamlit run app.py
```

## 功能亮点
- **5-tier 模型级联**: 自动在顶级模型 (gpt-oss-120b) 与备用模型 (llama-3.3-70b) 间切换，确保高可用。
- **可视化分析**: 
    - **Web 端**: 使用 Plotly 雷达图直观展示系统各维度的平衡性。
    - **CLI 端**: 使用 Rich 进度条在终端呈现直观的评分强弱分布。
- **高兼容性**: 所有模块均支持直接进入目录通过脚本运行，方便快速测试。
