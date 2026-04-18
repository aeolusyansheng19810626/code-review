# AI Tools & Code Reviewer

基于 Groq 的 AI 开发工具集。

## 项目结构
```
ai-tools/
├── code_review/         # AI 代码审查工具
│   ├── reviewer.py      # 核心逻辑 (5-tier 级联模型)
│   ├── cli.py           # 彩色命令行界面
│   └── app.py           # 现代化 Web UI
├── tech_decision/       # AI 技术决策顾问
│   ├── advisor.py       # 架构师逻辑 (5-tier 级联模型)
│   ├── cli.py           # 决策分析 CLI
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
# 进入目录
cd code_review
# CLI
python cli.py review ../test_code.py
# Web UI
streamlit run app.py
```

### 4. 使用 AI 技术决策顾问 (Tech Decision Advisor)
#### CLI 模式
```bash
# 进入目录
cd tech_decision

# 模式1: 方案生成
python cli.py generate "我们需要一个支持千万级日活的实时聊天系统"

# 模式2: 方案评估
python cli.py evaluate "使用 Redis 存储聊天记录，MySQL 存储用户信息"
```

#### Web UI 模式
```bash
# 进入目录
cd tech_decision
streamlit run app.py
```

## 功能亮点
- **5-tier 模型级联**: 自动在顶级模型 (gpt-oss-120b) 与备用模型间切换，确保高可用。
- **维度评估**: 技术方案评估支持 6 个核心维度，并以雷达图可视化展示。
- **现代化 UI**: 深度定制的 Streamlit 界面，提供 IDE 级的视觉体验。
