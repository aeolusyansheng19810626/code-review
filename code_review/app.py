import streamlit as st
import json
import os
from reviewer import CodeReviewer

# Page configuration
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS inspired by code_reviewer.html
STYLE = """
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #0d0f14;
        --surface: #13161e;
        --surface2: #1a1e29;
        --border: #252a38;
        --border2: #2e3548;
        --accent: #4f8ef7;
        --accent2: #6ee7b7;
        --accent3: #f59e0b;
        --red: #f87171;
        --orange: #fb923c;
        --yellow: #fbbf24;
        --green: #34d399;
        --text: #ffffff;
        --text2: #cbd5e1;
        --text3: #94a3b8;
        --mono: 'JetBrains Mono', monospace;
        --sans: 'Syne', sans-serif;
    }

    /* Main Container overrides */
    .stApp {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: var(--sans);
    }

    /* Ensure all text elements are visible */
    .stMarkdown, .stText, p, span, label, div {
        color: var(--text) !important;
    }
    
    .stMarkdown p, .stMarkdown li {
        color: var(--text2) !important;
    }

    /* Background grid */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(79,142,247,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(79,142,247,0.05) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
    }

    /* Header Styling */
    .header-container {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--border);
    }
    .logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, var(--accent), #7c3aed);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
    .logo-text {
        font-size: 24px;
        font-weight: 800;
        color: var(--text);
    }
    .logo-text span {
        color: var(--accent);
    }

    /* Panel Headers */
    .panel-header {
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 500;
        color: var(--text2);
        letter-spacing: 2px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 1rem;
    }
    .panel-header::before {
        content: '';
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--accent2);
        box-shadow: 0 0 8px var(--accent2);
    }

    /* Score Card */
    .score-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 24px;
    }
    .score-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 4px solid var(--score-color);
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: var(--mono);
        font-size: 28px;
        font-weight: 700;
        color: var(--score-color);
        flex-shrink: 0;
    }
    .score-info { flex: 1; }
    .score-label {
        font-family: var(--mono);
        font-size: 11px;
        color: var(--text3);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 4px;
        font-weight: 600;
    }
    .score-summary {
        font-size: 15px;
        color: var(--text);
        line-height: 1.5;
        font-weight: 500;
    }

    /* Strengths section */
    .strengths-box {
        background: rgba(52,211,153,0.05);
        border: 1px solid rgba(52,211,153,0.15);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
    }
    .strengths-title {
        font-family: var(--mono);
        font-size: 11px;
        color: var(--green);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Issue card */
    .issue-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 4px solid var(--sev-color);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .issue-meta {
        display: flex;
        gap: 8px;
        margin-bottom: 8px;
        align-items: center;
    }
    .sev-badge {
        font-family: var(--mono);
        font-size: 10px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        background: rgba(var(--sev-rgb), 0.15);
        color: var(--sev-color);
    }
    .cat-badge {
        font-family: var(--mono);
        font-size: 10px;
        color: var(--text3);
        background: var(--surface2);
        padding: 2px 8px;
        border-radius: 4px;
    }
    .issue-desc {
        font-size: 14px;
        color: var(--text);
        font-weight: 600;
        margin-bottom: 8px;
    }
    .issue-suggestion {
        font-size: 13px;
        color: var(--text2);
        line-height: 1.6;
        background: rgba(0,0,0,0.2);
        padding: 10px;
        border-radius: 4px;
    }

    /* Streamlit components overrides */
    div.stButton > button {
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.2s !important;
    }
    div.stButton > button:hover {
        background: #3a7de8 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(79,142,247,0.3);
    }
    .stTextArea textarea {
        background-color: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        font-family: var(--mono) !important;
        font-size: 13px !important;
    }
    .stCodeBlock {
        background-color: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
    }
</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <div class="header-container">
            <div class="logo-icon">⚡</div>
            <div class="logo-text">AI Code <span>Reviewer</span></div>
            <div style="margin-left:auto; font-family:'JetBrains Mono'; font-size:11px; color:#4a5568; border:1px solid #252a38; padding:4px 10px; border-radius:20px;">
                POWERED BY GPT-OSS-120B
            </div>
        </div>
    """, unsafe_allow_html=True)

def get_severity_style(sev):
    if sev == "严重":
        return "#f87171", "248,113,113"
    if sev == "中":
        return "#fb923c", "251,146,60"
    return "#fbbf24", "251,191,36"

def get_score_color(score):
    if score >= 8: return "#34d399"
    if score >= 6: return "#fbbf24"
    return "#f87171"

def main():
    render_header()

    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown('<div class="panel-header">Source Code</div>', unsafe_allow_html=True)
        
        # API Key management
        api_key = st.text_input("GROQ API KEY", type="password", placeholder="gsk_...", help="Required if not set in .env")
        
        input_method = st.radio("Input Method", ["Text Input", "File Upload"], horizontal=True)
        
        code = ""
        if input_method == "Text Input":
            code = st.text_area("Paste code here:", height=500, placeholder="# Paste your code here...")
        else:
            uploaded_file = st.file_uploader("Upload a file", type=["py", "js", "ts", "java", "c", "cpp", "go", "rs", "php", "rb", "txt"])
            if uploaded_file:
                code = uploaded_file.read().decode("utf-8")
                st.code(code, line_numbers=True)

        review_btn = st.button("Review Code", type="primary")

    with col_result:
        st.markdown('<div class="panel-header">Review Results</div>', unsafe_allow_html=True)
        
        if review_btn and code:
            with st.spinner("Analyzing code with GPT-OSS-120B..."):
                try:
                    reviewer = CodeReviewer(api_key=api_key if api_key else None)
                    result = reviewer.review_code(code)
                    
                    if "error" in result:
                        st.error(f"Error: {result['error']}")
                    else:
                        # Score Card
                        score_color = get_score_color(result['score'])
                        st.markdown(f"""
                            <div class="score-card">
                                <div class="score-circle" style="border-color: {score_color}; color: {score_color};">
                                    {result['score']}
                                </div>
                                <div class="score-info">
                                    <div class="score-label">Overall Score</div>
                                    <div class="score-summary">{result['summary']}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Strengths
                        if result.get('strengths'):
                            st.markdown('<div class="strengths-box"><div class="strengths-title">✦ Strengths</div>' + 
                                "".join([f'<div style="font-size:13px; color:#94a3b8; margin-bottom:4px;">✓ {s}</div>' for s in result['strengths']]) + 
                                '</div>', unsafe_allow_html=True)
                        
                        # Issues
                        issues = result.get('issues', [])
                        if not issues:
                            st.balloons()
                            st.success("No issues found! Your code is excellent.")
                        else:
                            st.markdown(f'<div style="font-family:var(--mono); font-size:11px; color:#4a5568; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:12px;">Issues Found: {len(issues)}</div>', unsafe_allow_html=True)
                            
                            for issue in issues:
                                sev_color, sev_rgb = get_severity_style(issue['severity'])
                                line_info = f"Line {issue['line']}" if issue['line'] else "General"
                                
                                st.markdown(f"""
                                    <div class="issue-card" style="--sev-color: {sev_color}; --sev-rgb: {sev_rgb};">
                                        <div class="issue-meta">
                                            <span class="sev-badge">{issue['severity']}</span>
                                            <span class="cat-badge">{issue['category']}</span>
                                            <span style="font-family:var(--mono); font-size:11px; color:#4a5568; margin-left:auto;">{line_info}</span>
                                        </div>
                                        <div class="issue-desc">{issue['description']}</div>
                                        <div class="issue-suggestion"><b>Suggestion:</b> {issue['suggestion']}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                if issue.get('code_fix'):
                                    with st.expander("View Code Fix"):
                                        st.code(issue['code_fix'], language="python")

                        # Overall Suggestion
                        if result.get('overall_suggestion'):
                            st.markdown(f"""
                                <div style="background: rgba(79,142,247,0.05); border: 1px solid rgba(79,142,247,0.15); border-radius: 8px; padding: 16px; margin-top: 16px;">
                                    <div style="font-family:var(--mono); font-size:11px; color:#4f8ef7; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:8px;">💡 Overall Suggestion</div>
                                    <div style="font-size:13px; color:#94a3b8; line-height:1.6;">{result['overall_suggestion']}</div>
                                </div>
                            """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"System Error: {str(e)}")
        else:
            st.markdown("""
                <div style="height:300px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px; color:#4a5568;">
                    <div style="font-size:48px; opacity:0.3;">🔍</div>
                    <div style="font-family:'JetBrains Mono'; font-size:13px; text-align:center; line-height:1.7;">
                        Paste your code on the left<br>and click <b>Review Code</b> to start
                    </div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
