from langchain_anthropic import ChatAnthropic


def get_default_model():
    """Get the default Claude model for all agents.
    
    Using Claude Sonnet 4.5 - October 2024 version.
    Model: claude-sonnet-4-5-20250929
    """
    return ChatAnthropic(model_name="claude-sonnet-4-5-20250929", max_tokens=64000)
