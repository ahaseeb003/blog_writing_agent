import json
import re
from langchain_openai import ChatOpenAI
from blog_writing_agent.core.state import BlogState, Section
from blog_writing_agent.config.settings import settings


def extract_json(text: str) -> dict:
    text = text.strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in response: {text!r}")
    return json.loads(match.group(0))


class PlanningAgents:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )

    async def router_node(self, state: BlogState):
        prompt = f"Topic: {state.topic}\nDecide if research is required. Output JSON: {{'research_required': bool}}"
        response = await self.llm.ainvoke(prompt)
        data = extract_json(response.content)
        return {"research_required": data.get("research_required", True)}

    async def planner_node(self, state: BlogState):
        prompt = f"Topic: {state.topic}\nCreate a detailed blog structure. Output JSON: {{'title': '...', 'sections': [{{'id': 1, 'heading': '...', 'research_needed': bool}}]}}"
        response = await self.llm.ainvoke(prompt)
        data = extract_json(response.content)
        sections = [Section(**s) for s in data.get("sections", [])]
        return {"outline": sections}
