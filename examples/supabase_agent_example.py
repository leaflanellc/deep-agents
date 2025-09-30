"""
Example demonstrating the Supabase Agent for knowledge base management.

This example shows how to:
1. Create a collection in Supabase with pgvector support
2. Add documents with automatic embedding generation
3. Perform semantic searches
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.supabase_agent import agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_agent():
    """Test the Supabase agent with a simple knowledge base."""
    
    print("=" * 80)
    print("Supabase Agent Example: US States Knowledge Base")
    print("=" * 80)
    
    # Check required environment variables
    if not os.getenv("SUPABASE_PROJECT_ID"):
        print("❌ Error: SUPABASE_PROJECT_ID not set in environment variables")
        return
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not set in environment variables")
        return
    
    # Test 1: Check connection
    print("\n📡 Test 1: Checking Supabase connection...")
    result = agent.invoke({
        "messages": [
            ("user", "Check the Supabase connection status")
        ]
    })
    print(f"Response: {result['messages'][-1].content}")
    
    # Test 2: Create a collection
    print("\n📝 Test 2: Creating US States collection...")
    result = agent.invoke({
        "messages": [
            ("user", """Create a collection called 'us_states' with these fields:
            - title (text)
            - content (text)
            - capital (text)
            - region (text)
            - population (text)
            
            Include pgvector support for semantic search.""")
        ]
    })
    print(f"Response: {result['messages'][-1].content}")
    
    # Test 3: Add documents
    print("\n📚 Test 3: Adding 5 US states with descriptions...")
    result = agent.invoke({
        "messages": [
            ("user", """Add these 5 US states to the us_states collection:
            
            1. California - The Golden State, known for Hollywood, Silicon Valley, beautiful beaches, and diverse geography from deserts to mountains. Capital: Sacramento, Region: West Coast, Population: 39 million
            
            2. Texas - The Lone Star State, famous for oil industry, cattle ranching, BBQ, and major cities like Houston and Dallas. Capital: Austin, Region: South, Population: 30 million
            
            3. Florida - The Sunshine State, renowned for theme parks, beaches, warm climate, and retirement communities. Capital: Tallahassee, Region: Southeast, Population: 22 million
            
            4. New York - Home to NYC, Wall Street, Statue of Liberty, and diverse culture. Capital: Albany, Region: Northeast, Population: 19 million
            
            5. Hawaii - The Aloha State, tropical paradise with volcanic activity, surfing, and unique Polynesian culture. Capital: Honolulu, Region: Pacific, Population: 1.4 million
            
            Generate embeddings automatically for semantic search.""")
        ]
    })
    print(f"Response: {result['messages'][-1].content}")
    
    # Test 4: Semantic search
    print("\n🔍 Test 4: Searching for 'states with beaches and warm weather'...")
    result = agent.invoke({
        "messages": [
            ("user", "Search the us_states collection for 'states with beaches and warm weather' - return top 3 results")
        ]
    })
    print(f"Response: {result['messages'][-1].content}")
    
    # Test 5: Another search
    print("\n🔍 Test 5: Searching for 'technology and innovation hubs'...")
    result = agent.invoke({
        "messages": [
            ("user", "Search the us_states collection for 'technology and innovation hubs' - return top 3 results")
        ]
    })
    print(f"Response: {result['messages'][-1].content}")
    
    # Test 6: List collections
    print("\n📋 Test 6: Listing all collections...")
    result = agent.invoke({
        "messages": [
            ("user", "Show me all the tables/collections in the database")
        ]
    })
    print(f"Response: {result['messages'][-1].content}")
    
    print("\n" + "=" * 80)
    print("✅ Supabase Agent Example Complete!")
    print("=" * 80)


if __name__ == "__main__":
    test_supabase_agent()

