import streamlit as st
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(page_title="论文精读", page_icon="", layout="wide")
st.title("论文精读助手")
st.caption("上传学术论文 PDF 或粘贴文本，AI 自动生成结构化精读报告")

uploaded = st.file_uploader("上传论文（PDF）", type=["pdf"])
pasted = st.text_area("或直接粘贴论文文本", height=200, placeholder="在此粘贴论文内容...")

if st.button("开始精读", type="primary"):
    paper_text = ""

    if uploaded:
        try:
            import pdfplumber

            with pdfplumber.open(uploaded) as pdf:
                paper_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        except ImportError:
            st.error("请安装 pdfplumber：pip install pdfplumber")
            st.stop()
    elif pasted.strip():
        paper_text = pasted.strip()
    else:
        st.warning("请上传 PDF 或粘贴论文文本。")
        st.stop()

    with st.spinner("AI 正在精读论文，请稍候…"):
        from paper_reader.reader import read_paper

        result = read_paper(paper_text)

    st.markdown("---")
    st.markdown(result)

    st.download_button(
        label="下载报告（Markdown）",
        data=result,
        file_name="paper_report.md",
        mime="text/markdown",
    )
