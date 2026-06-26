import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Settings:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    DEEPSEEK_MODEL = "deepseek/deepseek-chat"
    DEFAULT_RESEARCH_DEPTH = "advanced"

settings = Settings()
