import json
import re
from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from blog_writing_agent.core.state import BlogState
from blog_writing_agent.config.settings import settings


def extract_json(text: str) -> dict:
    text = text.strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in response: {text!r}")
    return json.loads(match.group(0))


class ExecutionAgents:
    def __init__(self):
        self.tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)
        self.llm = ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )

    async def research_agent(self, state: BlogState):
        results = []
        for section in state.outline:
            if section.research_needed:
                search_query = f"{state.topic} {section.heading}"
                search_result = self.tavily.search(query=search_query, search_depth="advanced")
                results.append({"section_id": section.id, "data": search_result})
        return {"research_data": results}

    async def writer_agent(self, state: BlogState):
        outputs = {}
        for section in state.outline:
            research = next((r for r in state.research_data if r["section_id"] == section.id), None)
            prompt = f"Write section: {section.heading}. Topic: {state.topic}. Research: {research}"
            response = await self.llm.ainvoke(prompt)
            outputs[section.id] = response.content
        return {"worker_outputs": outputs}

    async def image_agent(self, state: BlogState):
        image_suggestions = []
        for section in state.outline:
            prompt = f"Suggest an image for: {section.heading}. Output JSON: {{'title': '...', 'alt_text': '...', 'description': '...', 'image_prompt': '...'}}"
            response = await self.llm.ainvoke(prompt)
            data = extract_json(response.content)
            image_suggestions.append({"section_id": section.id, "suggestion": data})
        return {"images": image_suggestions}
