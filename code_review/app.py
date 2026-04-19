import streamlit as st

from reviewer import CodeReviewer


st.set_page_config(page_title="AI Code Reviewer", layout="wide")


def main():
    st.title("AI Code Reviewer")
    st.markdown("---")

    col_input, col_result = st.columns([1, 2], gap="large")

    with col_input:
        st.subheader("输入代码")

        input_method = st.radio("输入方式", ["文本输入", "文件上传"], horizontal=True)

        code = ""
        if input_method == "文本输入":
            code = st.text_area("粘贴代码:", height=420, placeholder="# 在这里粘贴需要审查的代码...")
        else:
            uploaded_file = st.file_uploader(
                "上传代码文件",
                type=["py", "js", "ts", "java", "c", "cpp", "go", "rs", "php", "rb", "txt"],
            )
            if uploaded_file:
                code = uploaded_file.read().decode("utf-8")
                st.code(code, line_numbers=True)

        api_key = st.text_input("Groq API Key (可选)", type="password", placeholder="gsk_...")
        review_btn = st.button("开始审查", type="primary")

    with col_result:
        st.subheader("审查结果")

        if review_btn and code:
            with st.spinner("AI 正在审查代码..."):
                try:
                    reviewer = CodeReviewer(api_key=api_key if api_key else None)
                    result = reviewer.review_code(code)
                except Exception as e:
                    st.error(f"系统错误: {str(e)}")
                    return

            if "error" in result:
                st.error(f"错误: {result['error']}")
                return

            if result.get("_model"):
                st.caption(f"使用模型：{result['_model']}")

            score = result.get("score", 0)
            summary = result.get("summary", "")

            c1, c2 = st.columns([1, 3])
            with c1:
                st.metric("综合评分", f"{score}/10")
            with c2:
                st.info(summary)

            if result.get("strengths"):
                st.markdown("### 优点")
                for strength in result["strengths"]:
                    st.write(f"- {strength}")

            issues = result.get("issues", [])
            if not issues:
                st.balloons()
                st.success("未发现明显问题。")
            else:
                st.markdown(f"### 发现问题: {len(issues)}")
                for issue in issues:
                    title = f"#{issue.get('id', '-')} {issue.get('category', '问题')}"
                    severity = issue.get("severity", "未知")
                    line = issue.get("line") or "通用"

                    with st.expander(f"{title} | {severity} | 行号: {line}", expanded=True):
                        st.write(issue.get("description", ""))
                        if issue.get("suggestion"):
                            st.markdown("**修改建议**")
                            st.write(issue["suggestion"])
                        if issue.get("code_fix"):
                            st.markdown("**参考修复代码**")
                            st.code(issue["code_fix"], language="python")

            if result.get("overall_suggestion"):
                st.markdown("### 总体建议")
                st.success(result["overall_suggestion"])
        else:
            st.markdown(
                """
                <div style="height:300px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px; color:gray;">
                    <p>在左侧输入或上传代码，然后点击 <b>开始审查</b>。</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
