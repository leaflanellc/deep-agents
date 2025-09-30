#!/usr/bin/env python3
"""
Test script for the Weaviate Agent.

This script demonstrates the complete functionality of the Weaviate agent including
web research, file uploads, and semantic search.
"""

import os
import json
from dotenv import load_dotenv
from src.agents.weaviate_agent import agent

# Load environment variables
load_dotenv()

def test_weaviate_agent():
    """Test the complete Weaviate agent functionality."""
    
    print("🤖 Testing Weaviate Agent")
    print("=" * 50)
    
    # Test 1: Check connection
    print("\n1. Testing Weaviate connection...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Check if Weaviate is connected and ready"}]
        })
        print(f"   Response: {result['messages'][-1]['content'][:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 2: List existing collections
    print("\n2. Listing existing collections...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "List all available collections in Weaviate"}]
        })
        print(f"   Response: {result['messages'][-1]['content'][:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Web research and collection creation
    print("\n3. Testing web research and collection creation...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Research 'artificial intelligence trends 2024' and create a knowledge base collection with the findings"}]
        })
        print(f"   Response: {result['messages'][-1]['content'][:300]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: File upload simulation (using sample data)
    print("\n4. Testing file upload and processing...")
    
    # Create sample JSON data
    sample_data = [
        {
            "title": "Machine Learning Basics",
            "content": "Machine learning is a subset of artificial intelligence that enables computers to learn from data.",
            "topic": "AI/ML",
            "difficulty": "Beginner",
            "tags": ["AI", "ML", "Basics"]
        },
        {
            "title": "Deep Learning Networks",
            "content": "Deep learning uses neural networks with multiple layers to model complex patterns in data.",
            "topic": "Deep Learning",
            "difficulty": "Intermediate",
            "tags": ["Deep Learning", "Neural Networks"]
        }
    ]
    
    try:
        # Simulate file upload by writing to a temporary file
        with open("temp_upload.json", "w") as f:
            json.dump(sample_data, f, indent=2)
        
        result = agent.invoke({
            "messages": [{"role": "user", "content": "I've uploaded a JSON file called 'temp_upload.json' with machine learning data. Please process it and add it to a collection called 'MLKnowledge'"}]
        })
        print(f"   Response: {result['messages'][-1]['content'][:300]}...")
        
        # Clean up
        os.remove("temp_upload.json")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Semantic search
    print("\n5. Testing semantic search...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Search for information about neural networks in the knowledge base"}]
        })
        print(f"   Response: {result['messages'][-1]['content'][:300]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Hybrid search
    print("\n6. Testing hybrid search...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Perform a hybrid search for 'machine learning algorithms' across all collections"}]
        })
        print(f"   Response: {result['messages'][-1]['content'][:300]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 7: Collection management
    print("\n7. Testing collection management...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Show me information about all collections and their contents"}]
        })
        print(f"   Response: {result['messages'][-1]['content'][:300]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ Weaviate Agent test completed!")

def test_file_processing():
    """Test file processing capabilities separately."""
    
    print("\n📁 Testing File Processing")
    print("=" * 30)
    
    # Test CSV processing
    print("\n1. Testing CSV processing...")
    csv_data = """title,content,topic,difficulty
Python Basics,Introduction to Python programming,Programming,Beginner
Data Analysis,Using pandas for data analysis,Data Science,Intermediate
Machine Learning,Introduction to ML algorithms,AI/ML,Advanced"""
    
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": f"Process this CSV data and add it to a collection:\n\n{csv_data}"}]
        })
        print(f"   Response: {result['messages'][-1]['content'][:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test Markdown processing
    print("\n2. Testing Markdown processing...")
    markdown_data = """# Introduction to AI

This is a comprehensive guide to artificial intelligence.

## Machine Learning
Machine learning is a subset of AI that focuses on algorithms.

## Deep Learning
Deep learning uses neural networks with multiple layers.

## Applications
AI has applications in various fields including healthcare, finance, and transportation."""
    
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": f"Process this Markdown document and add it to a collection:\n\n{markdown_data}"}]
        })
        print(f"   Response: {result['messages'][-1]['content'][:200]}...")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_weaviate_agent()
    test_file_processing()
