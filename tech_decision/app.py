import streamlit as st
import json
import plotly.graph_objects as go
from advisor import TechAdvisor

# Page configuration
st.set_page_config(page_title="AI Tech Decision Advisor", layout="wide")

def create_radar_chart(dimensions):
    categories = [d['name'] for d in dimensions]
    scores = [d['score'] for d in dimensions]
    categories.append(categories[0])
    scores.append(scores[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Score',
        line_color='#4f8ef7'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def main():
    st.title("💡 AI Tech Decision Advisor")
    st.markdown("---")

    mode = st.radio("选择模式", ["需求 → 方案生成", "已有方案深度评估"], horizontal=True)

    col_input, col_result = st.columns([1, 2], gap="large")

    with col_input:
        st.subheader("输入内容")
        if mode == "需求 → 方案生成":
            input_text = st.text_area("描述您的技术需求:", height=300, placeholder="例如：我们需要一个高并发的消息队列系统...")
        else:
            input_text = st.text_area("描述您的技术方案:", height=300, placeholder="例如：使用 Redis 做消息队列，预计日消息量1000万...")

        api_key = st.text_input("Groq API Key (可选)", type="password", placeholder="gsk_...")
        action_btn = st.button("开始分析", type="primary")

    with col_result:
        st.subheader("分析结果")
        
        if action_btn and input_text:
            with st.spinner("AI 架构师正在思考中..."):
                try:
                    advisor = TechAdvisor(api_key=api_key if api_key else None)
                    if mode == "需求 → 方案生成":
                        result = advisor.generate_solutions(input_text)
                        
                        if "error" in result:
                            st.error(result['error'])
                        else:
                            if result.get('_model'):
                                st.caption(f"使用模型：{result['_model']}")
                            st.info(f"**需求摘要:** {result['requirement']}")
                            
                            cols = st.columns(3)
                            for idx, sol in enumerate(result['solutions']):
                                with cols[idx]:
                                    is_rec = sol['id'] == result['recommendation']
                                    if is_rec:
                                        st.success(f"🏆 **{sol['name']} (推荐)**")
                                    else:
                                        st.markdown(f"### {sol['name']}")
                                    
                                    st.write(sol['description'])
                                    st.markdown("**技术栈:** " + ", ".join(sol['tech_stack']))
                                    
                                    with st.expander("优缺点分析"):
                                        st.markdown("**优点:**")
                                        for p in sol['pros']: st.write(f"- {p}")
                                        st.markdown("**缺点:**")
                                        for c in sol['cons']: st.write(f"- {c}")
                                    
                                    st.markdown(f"**复杂度:** {sol['complexity']} | **成本:** {sol['cost']}")

                            st.success(f"**推荐理由:**\n\n{result['recommendation_reasoning']}")
                    else:
                        result = advisor.evaluate_solution(input_text)
                        if "error" in result:
                            st.error(result['error'])
                        else:
                            if result.get('_model'):
                                st.caption(f"使用模型：{result['_model']}")
                            c1, c2 = st.columns([1, 2])
                            with c1:
                                st.metric("综合评分", f"{result['overall_score']}/10")
                                st.markdown(f"**最终决策:** `{result['decision']}`")
                                st.write(result['decision_reasoning'])
                            
                            with c2:
                                st.plotly_chart(create_radar_chart(result['dimensions']), use_container_width=True)
                            
                            st.markdown("### 维度评估详情")
                            for dim in result['dimensions']:
                                with st.expander(f"{dim['name']} - {dim['score']}/10"):
                                    st.write(dim['analysis'])
                                    if dim['risks']:
                                        st.markdown("**风险点:**")
                                        for r in dim['risks']: st.write(f"- {r}")
                                    if dim['suggestions']:
                                        st.markdown("**改进建议:**")
                                        for s in dim['suggestions']: st.write(f"- {s}")
                except Exception as e:
                    st.error(f"系统错误: {str(e)}")
        else:
            st.markdown("""
                <div style="height:300px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px; color:gray;">
                    <div style="font-size:48px; opacity:0.3;">🧠</div>
                    <p>在左侧输入您的技术问题，AI 架构师将为您提供专业建议。</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
