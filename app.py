import streamlit as st
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(
    page_title="AI 工具箱",
    page_icon="🧰",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
:root {
    --brand:     #6366F1;
    --brand-lt:  #EEF2FF;
    --brand-bd:  #C7D2FE;
    --green:     #10B981;
    --green-lt:  #D1FAE5;
    --bg:        #F8FAFC;
    --card:      #FFFFFF;
    --border:    #E2E8F0;
    --text-1:    #1E293B;
    --text-2:    #64748B;
    --text-3:    #94A3B8;
    --radius:    10px;
    --shadow:    0 1px 4px rgba(0,0,0,0.06);
}
#MainMenu,footer { display:none !important; }

.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"] {
    background: var(--bg) !important;
    font-family: -apple-system,'Segoe UI','PingFang SC','Hiragino Sans GB',sans-serif !important;
}
[data-testid="stMainBlockContainer"] { padding-top: 0 !important; max-width: 1100px !important; }

.tool-header {
    background: var(--card);
    border-bottom: 1px solid var(--border);
    padding: 16px 0 14px;
    margin: 0 0 24px;
}
.tool-title { font-size: 1.3rem; font-weight: 700; color: var(--text-1); margin: 0; }
.tool-desc  { font-size: 0.85rem; color: var(--text-2); margin: 4px 0 0; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
</style>
""",
    unsafe_allow_html=True,
)

TOOLS = [
    ("", "代码 Review", "code_review"),
    ("⚖️", "技术方案决策", "tech_decision"),
    ("", "论文精读", "paper_reader"),
    ("", "会议纪要", "meeting_minutes"),
    ("", "SQL 优化", "sql_optimizer"),
    ("", "正则生成器", "regex_generator"),
    ("", "技术周报", "weekly_report"),
    ("", "需求拆解", "task_breakdown"),
]

if "active_tool" not in st.session_state:
    st.session_state.active_tool = "code_review"

with st.sidebar:
    st.title("AI 工具箱")
    st.caption("软件工程师效率工具")
    st.markdown("**工具列表**")
    st.markdown("---")

    for icon, label, key in TOOLS:
        is_active = st.session_state.active_tool == key
        btn_type = "primary" if is_active else "secondary"
        if st.button(
            f"{icon} {label}",
            key=f"nav_{key}",
            use_container_width=True,
            type=btn_type,
        ):
            st.session_state.active_tool = key
            st.rerun()


def render_code_review():
    st.markdown(
        '<div class="tool-header"><p class="tool-title">代码 Review</p>'
        '<p class="tool-desc">粘贴或上传代码，AI 自动审查并给出改进建议</p></div>',
        unsafe_allow_html=True,
    )
    from code_review.reviewer import CodeReviewer

    col_in, col_out = st.columns([1, 2], gap="large")
    with col_in:
        input_method = st.radio("输入方式", ["文本输入", "文件上传"], horizontal=True)
        code = ""
        if input_method == "文本输入":
            code = st.text_area("粘贴代码", height=380, placeholder="# 在此粘贴代码...")
        else:
            uploaded = st.file_uploader(
                "上传代码文件",
                type=["py", "js", "ts", "java", "c", "cpp", "go", "rs", "php", "rb", "txt"],
            )
            if uploaded:
                code = uploaded.read().decode("utf-8")
                st.code(code, line_numbers=True)
        run = st.button("开始审查", type="primary", use_container_width=True)

    with col_out:
        if not run:
            st.info("在左侧输入或上传代码后开始审查。")
            return
        if not code:
            st.warning("请先输入或上传代码。")
            return

        with st.spinner("AI 正在审查代码…"):
            try:
                result = CodeReviewer().review_code(code)
            except Exception as e:
                st.error(str(e))
                return

        if "error" in result:
            st.error(result["error"])
            return

        if result.get("_model"):
            st.caption(f"使用模型：{result['_model']}")

        score = result.get("score", 0)
        c1, c2 = st.columns([1, 3])
        with c1:
            st.metric("综合评分", f"{score}/10")
        with c2:
            st.info(result.get("summary", ""))

        if result.get("strengths"):
            st.markdown("### 优点")
            for strength in result["strengths"]:
                st.write(f"- {strength}")

        issues = result.get("issues", [])
        if not issues:
            st.success("未发现明显问题。")
        else:
            st.markdown(f"### 发现问题（{len(issues)}）")
            for issue in issues:
                with st.expander(
                    f"#{issue.get('id', '-')} {issue.get('category', '问题')} | {issue.get('severity', '未知')}",
                    expanded=True,
                ):
                    st.write(issue.get("description", ""))
                    if issue.get("suggestion"):
                        st.markdown(f"**建议：** {issue['suggestion']}")
                    if issue.get("code_fix"):
                        st.code(issue["code_fix"], language="python")

        if result.get("overall_suggestion"):
            st.markdown("### 总体建议")
            st.success(result["overall_suggestion"])


def render_tech_decision():
    st.markdown(
        '<div class="tool-header"><p class="tool-title">技术方案决策</p>'
        '<p class="tool-desc">生成候选方案，或对已有技术方案做多维度评估</p></div>',
        unsafe_allow_html=True,
    )
    from tech_decision.advisor import TechAdvisor

    mode = st.radio("模式", ["需求生成方案", "评估已有方案"], horizontal=True)
    prompt = st.text_area(
        "输入内容",
        height=220,
        placeholder="例如：我们需要一个支持千万级日活的实时聊天系统",
    )
    run = st.button("开始分析", type="primary")

    if not run:
        return
    if not prompt.strip():
        st.warning("请先输入要分析的内容。")
        return

    with st.spinner("AI 正在分析…"):
        try:
            advisor = TechAdvisor()
            if mode == "需求生成方案":
                result = advisor.generate_solutions(prompt)
            else:
                result = advisor.evaluate_solution(prompt)
        except Exception as e:
            st.error(str(e))
            return

    if "error" in result:
        st.error(result["error"])
        return

    st.markdown("---")
    if result.get("_model"):
        st.caption(f"使用模型：{result['_model']}")
    if mode == "需求生成方案":
        st.info(f"**需求摘要：** {result.get('requirement', '')}")
        solutions = result.get("solutions", [])
        cols = st.columns(max(1, min(3, len(solutions))))
        for idx, solution in enumerate(solutions):
            with cols[idx % len(cols)]:
                rec = solution.get("id") == result.get("recommendation")
                title = f"{solution.get('name', '方案')}" + ("（推荐）" if rec else "")
                st.markdown(f"### {title}")
                st.write(solution.get("description", ""))
                st.markdown("**技术栈：** " + ", ".join(solution.get("tech_stack", [])))
                with st.expander("优缺点分析"):
                    st.markdown("**优点：**")
                    for item in solution.get("pros", []):
                        st.write(f"- {item}")
                    st.markdown("**缺点：**")
                    for item in solution.get("cons", []):
                        st.write(f"- {item}")
                st.markdown(
                    f"**复杂度：** {solution.get('complexity', '-')}"
                    f" | **成本：** {solution.get('cost', '-')}"
                    f" | **工期：** {solution.get('timeline', '-')}"
                )
        if result.get("recommendation_reasoning"):
            st.success(f"**推荐理由：**\n\n{result['recommendation_reasoning']}")
    else:
        c1, c2 = st.columns([1, 3])
        with c1:
            st.metric("综合评分", f"{result.get('overall_score', 0)}/10")
        with c2:
            st.markdown(f"**最终决策：** `{result.get('decision', '')}`")
            st.write(result.get("decision_reasoning", ""))

        for dim in result.get("dimensions", []):
            with st.expander(f"{dim.get('name', '维度')} - {dim.get('score', '-')}/10"):
                st.write(dim.get("analysis", ""))
                if dim.get("risks"):
                    st.markdown("**风险点：**")
                    for risk in dim["risks"]:
                        st.write(f"- {risk}")
                if dim.get("suggestions"):
                    st.markdown("**改进建议：**")
                    for suggestion in dim["suggestions"]:
                        st.write(f"- {suggestion}")

        if result.get("alternatives"):
            st.markdown("### 可替代方案")
            for alternative in result["alternatives"]:
                st.write(f"- {alternative}")


def render_paper_reader():
    st.markdown(
        '<div class="tool-header"><p class="tool-title">论文精读</p>'
        '<p class="tool-desc">上传学术论文 PDF 或粘贴文本，AI 自动生成结构化精读报告</p></div>',
        unsafe_allow_html=True,
    )
    from paper_reader.reader import read_paper

    uploaded = st.file_uploader("上传论文（PDF）", type=["pdf"])
    pasted = st.text_area("或直接粘贴论文文本", height=200, placeholder="在此粘贴论文内容...")
    run = st.button("开始精读", type="primary")

    if not run:
        return

    paper_text = ""
    if uploaded:
        try:
            import pdfplumber

            with pdfplumber.open(uploaded) as pdf:
                paper_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        except ImportError:
            st.error("请安装 pdfplumber：pip install pdfplumber")
            return
    elif pasted.strip():
        paper_text = pasted.strip()
    else:
        st.warning("请上传 PDF 或粘贴论文文本。")
        return

    with st.spinner("AI 正在精读…"):
        try:
            result, used_model = read_paper(paper_text, return_model=True)
        except Exception as e:
            st.error(str(e))
            return

    st.markdown("---")
    if used_model:
        st.caption(f"使用模型：{used_model}")
    st.markdown(result)
    st.download_button("下载报告（Markdown）", result, "paper_report.md", "text/markdown")


def render_meeting_minutes():
    st.markdown(
        '<div class="tool-header"><p class="tool-title">会议纪要</p>'
        '<p class="tool-desc">粘贴会议记录，AI 自动生成结构化纪要</p></div>',
        unsafe_allow_html=True,
    )
    from meeting_minutes.summarizer import summarize

    transcript = st.text_area("粘贴会议记录", height=300, placeholder="在此粘贴会议记录内容...")
    mode = st.radio("输出模式", ["完整纪要", "要点摘要"], horizontal=True)
    mode_key = "full" if mode == "完整纪要" else "brief"
    run = st.button("生成纪要", type="primary")

    if not run:
        return
    if not transcript.strip():
        st.warning("请先粘贴会议记录。")
        return

    with st.spinner("AI 正在生成纪要…"):
        try:
            result, used_model = summarize(transcript, mode=mode_key, return_model=True)
        except Exception as e:
            st.error(str(e))
            return

    st.markdown("---")
    if used_model:
        st.caption(f"使用模型：{used_model}")
    st.markdown(result)
    st.download_button("下载纪要（Markdown）", result, "meeting_minutes.md", "text/markdown")


def render_sql_optimizer():
    st.markdown(
        '<div class="tool-header"><p class="tool-title">SQL 查询优化</p>'
        '<p class="tool-desc">粘贴 SQL，AI 分析性能瓶颈并给出优化建议</p></div>',
        unsafe_allow_html=True,
    )
    from sql_optimizer.optimizer import optimize_sql

    sql = st.text_area("粘贴 SQL 查询", height=200, placeholder="SELECT * FROM orders WHERE ...")
    db_type = st.selectbox("数据库类型", ["MySQL", "PostgreSQL", "SQLite", "Oracle", "SQL Server"])
    schema_info = st.text_area(
        "表结构（可选，粘贴 CREATE TABLE 语句）",
        height=100,
        placeholder="CREATE TABLE orders (...)",
    )
    run = st.button("开始优化", type="primary")

    if not run:
        return
    if not sql.strip():
        st.warning("请先粘贴 SQL 查询。")
        return

    with st.spinner("AI 正在分析…"):
        try:
            result, used_model = optimize_sql(sql, db_type=db_type, schema_info=schema_info, return_model=True)
        except Exception as e:
            st.error(str(e))
            return

    st.markdown("---")
    if used_model:
        st.caption(f"使用模型：{used_model}")
    st.markdown(result)
    st.download_button("下载报告（Markdown）", result, "sql_report.md", "text/markdown")


def render_regex_generator():
    st.markdown(
        '<div class="tool-header"><p class="tool-title">正则表达式生成器</p>'
        '<p class="tool-desc">描述匹配需求，AI 生成正则并逐段解释</p></div>',
        unsafe_allow_html=True,
    )
    from regex_generator.generator import generate_regex

    description = st.text_area(
        "描述你的匹配需求",
        height=120,
        placeholder="例如：匹配日本手机号码，格式为 090-1234-5678 或 08012345678",
    )
    language = st.selectbox("编程语言", ["Python", "JavaScript", "Java", "Go", "Rust", "PHP"])
    samples = st.text_input(
        "测试样本（可选，用逗号分隔）",
        placeholder="090-1234-5678, 08012345678, 03-1234-5678",
    )
    run = st.button("生成正则", type="primary")

    if not run:
        return
    if not description.strip():
        st.warning("请先描述匹配需求。")
        return

    with st.spinner("AI 正在生成…"):
        try:
            result, used_model = generate_regex(description, language=language, samples=samples, return_model=True)
        except Exception as e:
            st.error(str(e))
            return

    st.markdown("---")
    if used_model:
        st.caption(f"使用模型：{used_model}")
    st.markdown(result)
    st.download_button("下载结果（Markdown）", result, "regex_result.md", "text/markdown")


def render_weekly_report():
    st.markdown(
        '<div class="tool-header"><p class="tool-title">技术周报生成</p>'
        '<p class="tool-desc">输入本周工作内容，AI 自动生成格式规范的技术周报</p></div>',
        unsafe_allow_html=True,
    )
    from weekly_report.generator import generate_report

    col1, col2 = st.columns(2)
    with col1:
        author = st.text_input("姓名/团队", placeholder="张伟 / 后端团队")
    with col2:
        week = st.text_input("周次", placeholder="2026年第16周")
    content = st.text_area(
        "本周工作内容",
        height=200,
        placeholder="随意填写，例如：\n- 修复了登录超时 bug\n- 完成了消息推送模块开发\n- 参加了架构评审会议",
    )
    next_plan = st.text_area(
        "下周计划（可选）",
        height=100,
        placeholder="例如：\n- 开始数据导出功能开发\n- 优化首页加载速度",
    )
    run = st.button("生成周报", type="primary")

    if not run:
        return
    if not content.strip():
        st.warning("请先填写本周工作内容。")
        return

    with st.spinner("AI 正在生成周报…"):
        try:
            result, used_model = generate_report(
                content,
                author=author,
                week=week,
                next_plan=next_plan,
                return_model=True,
            )
        except Exception as e:
            st.error(str(e))
            return

    st.markdown("---")
    if used_model:
        st.caption(f"使用模型：{used_model}")
    st.markdown(result)
    st.download_button("下载周报（Markdown）", result, "weekly_report.md", "text/markdown")


def render_task_breakdown():
    st.markdown(
        '<div class="tool-header"><p class="tool-title">需求拆解</p>'
        '<p class="tool-desc">输入需求描述，AI 自动拆解为可执行工程任务清单</p></div>',
        unsafe_allow_html=True,
    )
    from task_breakdown.generator import break_down_tasks

    requirement = st.text_area(
        "需求描述",
        height=180,
        placeholder="例如：开发一个支持用户注册、登录、个人资料编辑和权限管理的后台系统",
    )
    col1, col2 = st.columns(2)
    with col1:
        tech_stack = st.text_input("技术栈（可选）", placeholder="例如：Python, FastAPI, PostgreSQL, React")
    with col2:
        team_size = st.text_input("团队规模（可选）", placeholder="例如：2名前端、3名后端、1名测试")
    run = st.button("开始拆解", type="primary")

    if not run:
        return
    if not requirement.strip():
        st.warning("请先填写需求描述。")
        return

    with st.spinner("AI 正在拆解需求…"):
        try:
            result, used_model = break_down_tasks(
                requirement,
                tech_stack=tech_stack,
                team_size=team_size,
                return_model=True,
            )
        except Exception as e:
            st.error(str(e))
            return

    st.markdown("---")
    if used_model:
        st.caption(f"使用模型：{used_model}")
    st.markdown(result)
    st.download_button("下载任务清单（Markdown）", result, "task_breakdown.md", "text/markdown")


tool = st.session_state.active_tool
if tool == "code_review":
    render_code_review()
elif tool == "tech_decision":
    render_tech_decision()
elif tool == "paper_reader":
    render_paper_reader()
elif tool == "meeting_minutes":
    render_meeting_minutes()
elif tool == "sql_optimizer":
    render_sql_optimizer()
elif tool == "regex_generator":
    render_regex_generator()
elif tool == "weekly_report":
    render_weekly_report()
elif tool == "task_breakdown":
    render_task_breakdown()
