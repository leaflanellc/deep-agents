"""
Simple example agent demonstrating Deep Agents functionality.
This example shows how to create a basic agent with custom tools.
"""

import os
from dotenv import load_dotenv
from deepagents import create_deep_agent
from tools.example_tools import calculate_area, get_weather

# Load environment variables from .env file
load_dotenv()

# Create a simple agent with custom tools
agent = create_deep_agent(
    tools=[calculate_area, get_weather],
    instructions="""You are a helpful assistant that can:
        1. Calculate the area of rectangles using length and width
        2. Provide weather information for cities
        
        When asked to calculate area, use the calculate_area tool.
        When asked about weather, use the get_weather tool.
        Always be helpful and provide clear explanations.""",
)
