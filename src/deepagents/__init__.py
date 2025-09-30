from deepagents.graph import create_deep_agent, async_create_deep_agent
from deepagents.middleware import PlanningMiddleware, FilesystemMiddleware, SubAgentMiddleware
from deepagents.state import DeepAgentState
from deepagents.types import SubAgent, CustomSubAgent
from deepagents.model import get_default_model

# Import tools and agents for easy access
# Note: These imports are done lazily to avoid circular imports
def _import_agents():
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from agents import coding_agent, research_agent, simple_agent
    return coding_agent, research_agent, simple_agent

def _import_tools():
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from tools import (
        write_todos, ls, read_file, write_file, edit_file,
        internet_search, write_code, run_tests, debug_code, 
        code_review, generate_documentation, calculate_area, get_weather
    )
    return {
        'write_todos': write_todos, 'ls': ls, 'read_file': read_file, 
        'write_file': write_file, 'edit_file': edit_file,
        'internet_search': internet_search, 'write_code': write_code, 
        'run_tests': run_tests, 'debug_code': debug_code, 
        'code_review': code_review, 'generate_documentation': generate_documentation, 
        'calculate_area': calculate_area, 'get_weather': get_weather
    }

# Make agents available at module level
try:
    coding_agent, research_agent, simple_agent = _import_agents()
except ImportError:
    # Fallback if agents can't be imported
    coding_agent = research_agent = simple_agent = None
