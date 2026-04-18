# AI Code Reviewer

基于 Groq (Llama-3/gpt-oss) 的自动化代码审查工具。

## 功能
- **核心逻辑 (`reviewer.py`)**: 支持代码字符串和文件输入，自动识别语言并进行全维度 Review。
- **命令行界面 (`cli.py`)**: 提供彩色格式化输出，方便开发者在终端快速查看建议。
- **Web UI (`app.py`)**: 使用 Streamlit 构建，左侧输入/上传代码，右侧按严重程度分组展示 Review 结果。

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置 API Key
在项目根目录创建 `.env` 文件，并添加你的 Groq API Key：
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. 使用 CLI
```bash
# 审查文件
python -m code_review.cli review path/to/your/file.py

# 审查代码字符串
python -m code_review.cli review --code "def my_func(): pass"
```

### 4. 运行 Web UI
```bash
streamlit run code_review/app.py
```

## 项目结构
```
ai-tools/
├── code_review/
│   ├── reviewer.py      # 核心 Review 逻辑
│   ├── cli.py           # CLI 入口
│   ├── app.py           # Streamlit Web UI
│   └── prompts.py       # prompt 管理
├── requirements.txt
└── README.md
```
