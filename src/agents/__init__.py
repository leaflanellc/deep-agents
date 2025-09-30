"""
Agents module for Deep Agents.

This module contains various agent implementations that can be used
with the Deep Agents framework.
"""

from .coding_agent import agent as coding_agent
from .research_agent import agent as research_agent
from .simple_agent import agent as simple_agent
from .supabase_agent import agent as supabase_agent
from .weaviate_agent import agent as weaviate_agent

__all__ = ["coding_agent", "research_agent", "simple_agent", "supabase_agent", "weaviate_agent"]
