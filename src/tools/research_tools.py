"""
Research tools for Deep Agents.

This module contains tools for conducting research and web searches.
"""

import os
from typing import Literal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Optional import for tavily
try:
    from tavily import TavilyClient
    tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
except ImportError:
    TavilyClient = None
    tavily_client = None


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search using Tavily API"""
    if tavily_client is None:
        return {"error": "Tavily client not available. Please install tavily-python package."}
    
    search_docs = tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
    return search_docs
