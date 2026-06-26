import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from blog_writing_agent.core.graph import create_blog_graph
import streamlit as st
import asyncio
from blog_writing_agent.core.graph import create_blog_graph
from blog_writing_agent.core.state import BlogState

st.set_page_config(page_title="Multi-Agent Blog Writer", layout="wide")

st.title("🚀 Multi-Agent Blog Writing System")
st.markdown("Generate production-grade blogs using LangGraph and DeepSeek.")

with st.sidebar:
    st.header("Configuration")
    topic = st.text_input("Blog Topic", placeholder="e.g., The Future of Quantum Computing")
    research_toggle = st.checkbox("Enable Research", value=True)
    model_selection = st.selectbox("Select Model", ["DeepSeek-Chat", "GPT-4-Turbo"])
    generate_btn = st.button("Generate Blog")

if generate_btn and topic:
    st.info(f"Generating blog for: {topic}...")
    
    async def run_workflow():
        graph = create_blog_graph()
        initial_state = BlogState(topic=topic, research_required=research_toggle)
        result = await graph.ainvoke(initial_state)
        return result

    with st.spinner("Agents are working..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_workflow())
        
    st.success("Blog Generated Successfully!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Final Blog Preview")
        st.markdown(result.get("final_blog", "No content generated."))
        
    with col2:
        st.subheader("Agent Activity & Metadata")
        st.json(result)
        
    st.download_button(
        label="Download Markdown",
        data=result.get("final_blog", ""),
        file_name=f"{topic.replace(' ', '_')}.md",
        mime="text/markdown"
    )
else:
    st.info("Enter a topic and click 'Generate Blog' to start.")
