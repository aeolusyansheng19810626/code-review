import streamlit as st
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(page_title="会议纪要", page_icon="", layout="wide")
st.title("会议纪要助手")
st.caption("粘贴会议记录，AI 自动生成结构化纪要")

transcript = st.text_area("粘贴会议记录", height=300, placeholder="在此粘贴会议记录内容...")

mode = st.radio("输出模式", ["完整纪要", "要点摘要"], horizontal=True)
mode_key = "full" if mode == "完整纪要" else "brief"

if st.button("生成纪要", type="primary"):
    if not transcript.strip():
        st.warning("请先粘贴会议记录。")
        st.stop()

    with st.spinner("AI 正在生成纪要，请稍候…"):
        from meeting_minutes.summarizer import summarize

        result = summarize(transcript, mode=mode_key)

    st.markdown("---")
    st.markdown(result)

    st.download_button(
        label="下载纪要（Markdown）",
        data=result,
        file_name="meeting_minutes.md",
        mime="text/markdown",
    )
