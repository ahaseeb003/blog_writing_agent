# Multi-Agent Blog Writing System

This project implements a production-grade multi-agent blog writing system using LangGraph, LangChain, OpenAI, OpenRouter/DeepSeek, Tavily, and Streamlit. The system automates the process of generating high-quality blog posts from a user-provided topic, following a Planning → Research → Writing → Review → Publish workflow.

## Features

*   **Topic Input**: Users can provide a blog topic through a Streamlit frontend.
*   **Research Toggle**: Option to enable or disable external research.
*   **Model Selection**: Choose between DeepSeek-Chat (via OpenRouter) and GPT-4-Turbo (via OpenAI) for different stages.
*   **Progress Tracking**: Real-time updates on agent activity.
*   **Blog Preview**: View the generated blog post directly in the application.
*   **Markdown Download**: Download the final blog post as a Markdown file.
*   **Modular Agent Architecture**: Specialized agents for routing, planning, research, writing, image suggestion, review, and final editing.
*   **LangGraph Workflow**: Orchestrates the agents and manages the state throughout the blog generation process.

## Architecture Overview

The system is built around a LangGraph StateGraph, defining a clear workflow for blog generation:

1.  **Router Node**: Receives user requests, detects request type, decides workflow path, and determines if research is required. Routes the request to the planner.
2.  **Planner Node**: Analyzes the topic, creates a detailed blog structure with headings and subheadings, and generates an execution plan.
3.  **Research Agent**: (If research is enabled) Uses Tavily Search to gather authoritative sources, extract facts, statistics, and references, and stores citations.
4.  **Worker Agents (Writer, Image)**: 
    *   **Writer Agent**: Creates blog content for each section based on the outline and research.
    *   **Image Agent**: Suggests relevant images for each section, including title, alt text, description, and image prompt.
5.  **Reviewer Agent**: Checks the generated draft for grammar, readability, coherence, factual consistency, and SEO quality, providing improvement suggestions.
6.  **Final Editor Agent**: Incorporates feedback from the reviewer and creates a publication-ready blog in Markdown format, including a table of contents, citations, image placeholders, conclusion, and references.

## Tech Stack

*   **Python**
*   **LangGraph**: For building robust, stateful multi-agent applications.
*   **LangChain**: For interacting with LLMs and various tools.
*   **OpenAI API**: For GPT models (e.g., GPT-4-Turbo) for review and editing.
*   **OpenRouter API**: For DeepSeek models for planning, research, and drafting.
*   **Tavily Search**: For internet research and data gathering.
*   **Streamlit**: For creating an interactive web-based user interface.
*   **Pydantic**: For data validation and settings management.
*   **Asyncio**: For asynchronous operations.
*   **python-dotenv**: For managing environment variables.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ahaseeb003/blog_writing_agent
cd blog_writing_agent
```

*(Note: Replace `<repository_url>` with the actual repository URL once available.)*

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project and add your API keys:

```
OPENAI_API_KEY="your_openai_api_key"
OPENROUTER_API_KEY="your_openrouter_api_key"
TAVILY_API_KEY="your_tavily_api_key"
```

*   **OpenAI API Key**: Obtain from [OpenAI Platform](https://platform.openai.com/).
*   **OpenRouter API Key**: Obtain from [OpenRouter](https://openrouter.ai/).
*   **Tavily API Key**: Obtain from [Tavily AI](https://tavily.com/).

### 5. Run the Streamlit Application

To ensure the `blog_writing_agent` module is correctly recognized, run the application from the **parent directory** of the project or set the `PYTHONPATH`:

#### Option A: Run from the parent directory
```bash
# Navigate to the parent directory of blog_writing_agent
cd ..
streamlit run blog_writing_agent/frontend/app.py
```

#### Option B: Set PYTHONPATH (Recommended)
```bash
# In the root directory of the project
export PYTHONPATH=$PYTHONPATH:.
streamlit run frontend/app.py
```

Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Deployment Guide

This application can be deployed on various platforms that support Python and Streamlit applications. Here are general steps for deployment:

### Heroku (Example)

1.  **Create a `Procfile`** in the root directory:
    ```
    web: sh setup.sh && streamlit run frontend/app.py --server.port=$PORT --server.enableCORS=false --server.enableXsrfProtection=false
    ```
2.  **Create a `setup.sh`** script for Heroku to install dependencies and set up environment:
    ```bash
    mkdir -p ~/.streamlit/
echo "[general]\nemail = \"your-email@example.com\"\n" > ~/.streamlit/credentials.toml
echo "[server]\nheadless = true\nenableCORS=false\nenableXsrfProtection=false\nport = $PORT\n" > ~/.streamlit/config.toml
    ```
3.  **Set Environment Variables**: Configure `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, and `TAVILY_API_KEY` in your Heroku app settings.
4.  **Deploy**: Push your code to Heroku Git remote.

### Other Platforms

For other platforms like AWS, Google Cloud, Azure, or Docker, you would typically:

*   Containerize the application using Docker.
*   Set up a web server (e.g., Gunicorn) to serve the Streamlit app.
*   Configure environment variables securely.
*   Ensure persistent storage if needed (though this app is stateless).

## Future Enhancements

*   Integration with more LLM providers and models.
*   Advanced task decomposition and parallel execution strategies.
*   Support for different output formats (e.g., PDF export directly from the app).
*   Enhanced UI for better progress visualization and agent interaction logging.
*   Database integration for storing generated blogs and user preferences.

---

**Author**: Manus AI
**Date**: June 25, 2026
