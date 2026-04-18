import streamlit as st
import json
import plotly.graph_objects as go
from advisor import TechAdvisor

st.set_page_config(page_title="AI Tech Decision Advisor", layout="wide")

def create_radar_chart(dimensions):
    categories = [d['name'] for d in dimensions]
    scores = [d['score'] for d in dimensions]
    
    # Repeat the first element to close the radar
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
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0'
    )
    return fig

def main():
    st.title("💡 AI Tech Decision Advisor")
    st.markdown("---")

    mode = st.radio("Select Mode", ["Requirement -> Solution Generation", "Existing Solution Evaluation"], horizontal=True)

    col_input, col_result = st.columns([1, 2], gap="large")

    with col_input:
        st.subheader("Input")
        if mode == "Requirement -> Solution Generation":
            input_text = st.text_area("Describe your technical requirement:", height=300, placeholder="e.g., We need a high-concurrency message queue system for 10M messages/day.")
        else:
            input_text = st.text_area("Describe your existing technical solution:", height=300, placeholder="e.g., Use Redis as a message queue for 10M messages/day.")

        api_key = st.text_input("Groq API Key (Optional)", type="password")
        action_btn = st.button("Generate Advice", type="primary")

    with col_result:
        st.subheader("Advice")
        if action_btn and input_text:
            with st.spinner("Analyzing with AI Architecture Advisor..."):
                try:
                    advisor = TechAdvisor(api_key=api_key if api_key else None)
                    if mode == "Requirement -> Solution Generation":
                        result = advisor.generate_solutions(input_text)
                        
                        if "error" in result:
                            st.error(result['error'])
                        else:
                            st.info(f"**Requirement Summary:** {result['requirement']}")
                            
                            cols = st.columns(3)
                            for idx, sol in enumerate(result['solutions']):
                                with cols[idx]:
                                    is_rec = sol['id'] == result['recommendation']
                                    if is_rec:
                                        st.success(f"🏆 **{sol['name']}**")
                                    else:
                                        st.markdown(f"### {sol['name']}")
                                    
                                    st.write(sol['description'])
                                    st.markdown("**Tech Stack:** " + ", ".join(sol['tech_stack']))
                                    
                                    with st.expander("Pros & Cons"):
                                        st.markdown("**Pros:**")
                                        for p in sol['pros']: st.write(f"- {p}")
                                        st.markdown("**Cons:**")
                                        for c in sol['cons']: st.write(f"- {c}")
                                    
                                    st.markdown(f"- **Complexity:** {sol['complexity']}")
                                    st.markdown(f"- **Cost:** {sol['cost']}")
                                    st.markdown(f"- **Timeline:** {sol['timeline']}")
                            
                            st.success(f"**Recommendation Reasoning:**\n\n{result['recommendation_reasoning']}")
                    else:
                        result = advisor.evaluate_solution(input_text)
                        if "error" in result:
                            st.error(result['error'])
                        else:
                            col_score, col_radar = st.columns([1, 2])
                            with col_score:
                                st.metric("Overall Score", f"{result['overall_score']}/10")
                                st.markdown(f"**Decision:** {result['decision']}")
                                st.markdown(f"**Reasoning:** {result['decision_reasoning']}")
                            
                            with col_radar:
                                fig = create_radar_chart(result['dimensions'])
                                st.plotly_chart(fig, use_container_width=True)
                            
                            st.markdown("### Dimension Analysis")
                            for dim in result['dimensions']:
                                with st.expander(f"{dim['name']} - {dim['score']}/10"):
                                    st.write(dim['analysis'])
                                    if dim['risks']:
                                        st.markdown("**Risks:**")
                                        for r in dim['risks']: st.write(f"- {r}")
                                    if dim['suggestions']:
                                        st.markdown("**Suggestions:**")
                                        for s in dim['suggestions']: st.write(f"- {s}")
                            
                            if result.get('alternatives'):
                                st.markdown("### Alternatives")
                                for alt in result['alternatives']: st.write(f"- {alt}")

                except Exception as e:
                    st.error(f"Error: {str(e)}")
        elif action_btn:
            st.warning("Please enter some text to analyze.")

if __name__ == "__main__":
    main()
