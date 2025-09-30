"""
Coding assistant agent for LangGraph UI integration.
This agent helps with coding tasks, debugging, and code reviews.
"""

from deepagents import create_deep_agent
from tools.coding_tools import (
    write_code,
    run_tests,
    debug_code,
    code_review,
    generate_documentation,
)

# Create coding agent
agent = create_deep_agent(
    tools=[write_code, run_tests, debug_code, code_review, generate_documentation],
    instructions="""You are a helpful coding assistant that can:
    1. Write and organize code in various programming languages
    2. Run tests and check for issues
    3. Debug code and suggest fixes
    4. Perform code reviews and suggest improvements
    5. Generate documentation for code
    6. Help with best practices and coding standards
    
    Always provide clear, well-commented code and explain your reasoning.
    When suggesting fixes, explain why the changes are needed.
    Be helpful and educational in your responses.""",
)
