#!/usr/bin/env python3
"""
Example showing how to use Deep Agents with environment variables from .env file.
This demonstrates loading API keys from a .env file and using them with Deep Agents.
"""

import os
from dotenv import load_dotenv
from deepagents import create_deep_agent

# Load environment variables from .env file
load_dotenv()

def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle"""
    return length * width

def get_weather(city: str) -> str:
    """Get weather information for a city (mock function)"""
    return f"The weather in {city} is sunny with 72°F"

def main():
    """Main function to demonstrate Deep Agents with .env file"""
    
    print("🔧 Deep Agents with .env Configuration")
    print("=" * 50)
    
    # Check if API keys are loaded from .env file
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_key = os.getenv("WEAVIATE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    print(f"ANTHROPIC_API_KEY loaded: {'✅ Yes' if anthropic_key and anthropic_key != 'your_anthropic_api_key_here' else '❌ No (using placeholder)'}")
    print(f"TAVILY_API_KEY loaded: {'✅ Yes' if tavily_key and tavily_key != 'your_tavily_api_key_here' else '❌ No (using placeholder)'}")
    print(f"WEAVIATE_URL loaded: {'✅ Yes' if weaviate_url and weaviate_url != 'your_weaviate_url_here' else '❌ No (using placeholder)'}")
    print(f"WEAVIATE_API_KEY loaded: {'✅ Yes' if weaviate_key and weaviate_key != 'your_weaviate_api_key_here' else '❌ No (using placeholder)'}")
    print(f"OPENAI_API_KEY loaded: {'✅ Yes' if openai_key and openai_key != 'your_openai_api_key_here' else '❌ No (using placeholder)'} - Optional for Weaviate vectorization")
    
    if not anthropic_key or anthropic_key == 'your_anthropic_api_key_here':
        print("\n⚠️  Please update your .env file with your actual API keys:")
        print("   1. Open the .env file in this directory")
        print("   2. Replace 'your_anthropic_api_key_here' with your actual Anthropic API key")
        print("   3. Replace 'your_tavily_api_key_here' with your actual Tavily API key (optional)")
        print("   4. Replace 'your_weaviate_url_here' with your Weaviate Cloud URL")
        print("   5. Replace 'your_weaviate_api_key_here' with your Weaviate API key")
        print("   6. Replace 'your_openai_api_key_here' with your OpenAI API key (optional - Weaviate uses its own embeddings)")
        print("\n   Example .env file content:")
        print("   ANTHROPIC_API_KEY=sk-ant-api03-...")
        print("   TAVILY_API_KEY=tvly-...")
        print("   WEAVIATE_URL=https://your-cluster-url.weaviate.network")
        print("   WEAVIATE_API_KEY=your-weaviate-api-key")
        print("   OPENAI_API_KEY=sk-...")
        return
    
    # Create agent with custom tools
    agent = create_deep_agent(
        tools=[calculate_area, get_weather],
        instructions="""You are a helpful assistant that can:
        1. Calculate the area of rectangles using length and width
        2. Provide weather information for cities
        
        When asked to calculate area, use the calculate_area tool.
        When asked about weather, use the get_weather tool.
        Always be helpful and provide clear explanations.""",
    )
    
    print("\n🤖 Testing Deep Agents with API key from .env file...")
    print("-" * 50)
    
    # Test the agent with a simple query
    try:
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": "What's the area of a rectangle with length 5 and width 3?"}
            ]
        })
        
        print("User: What's the area of a rectangle with length 5 and width 3?")
        print(f"Agent: {result['messages'][-1]['content']}")
        
        print("\n✅ Deep Agents is working with .env configuration!")
        
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        print("   Make sure your ANTHROPIC_API_KEY in .env is valid")

if __name__ == "__main__":
    main()
