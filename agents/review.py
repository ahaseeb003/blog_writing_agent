from langchain_openai import ChatOpenAI
from blog_writing_agent.core.state import BlogState
from blog_writing_agent.config.settings import settings

class ReviewAgents:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )

    async def reviewer_agent(self, state: BlogState):
        draft = "\n\n".join(state.worker_outputs.values())
        prompt = f"Review this blog draft for grammar, coherence, and SEO: {draft}\nReturn improvement suggestions."
        response = await self.llm.ainvoke(prompt)
        return {"review_feedback": [response.content]}

    async def final_editor_agent(self, state: BlogState):
        draft = "\n\n".join(state.worker_outputs.values())
        feedback = "\n".join(state.review_feedback)
        prompt = f"Finalize this blog based on feedback.\nDraft: {draft}\nFeedback: {feedback}\nOutput full Markdown."
        response = await self.llm.ainvoke(prompt)
        return {"final_blog": response.content}
