#!/usr/bin/env python3
"""
Comprehensive example of using the Weaviate Agent.

This example demonstrates all the key features of the Weaviate agent:
- Web research and knowledge base creation
- File upload and processing
- Semantic search capabilities
- Collection management
"""

import os
import json
from dotenv import load_dotenv
from src.agents.weaviate_agent import agent

# Load environment variables
load_dotenv()

def demonstrate_web_research():
    """Demonstrate web research and knowledge base creation."""
    
    print("🔍 Web Research & Knowledge Base Creation")
    print("=" * 50)
    
    # Example 1: Research a specific topic
    print("\n1. Researching 'Quantum Computing Applications'...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Research quantum computing applications in 2024 and create a comprehensive knowledge base collection called 'QuantumComputing2024'"}]
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Research multiple topics
    print("\n2. Researching 'Climate Change Solutions'...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Research renewable energy solutions for climate change and create a knowledge base called 'ClimateSolutions'"}]
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
    except Exception as e:
        print(f"Error: {e}")

def demonstrate_file_upload():
    """Demonstrate file upload and processing capabilities."""
    
    print("\n📁 File Upload & Processing")
    print("=" * 30)
    
    # Example 1: JSON data upload
    print("\n1. Uploading JSON data...")
    json_data = {
        "documents": [
            {
                "title": "Introduction to Blockchain",
                "content": "Blockchain is a distributed ledger technology that maintains a continuously growing list of records.",
                "topic": "Blockchain",
                "difficulty": "Beginner",
                "tags": ["Blockchain", "Technology", "Cryptocurrency"]
            },
            {
                "title": "Smart Contracts",
                "content": "Smart contracts are self-executing contracts with the terms directly written into code.",
                "topic": "Blockchain",
                "difficulty": "Intermediate",
                "tags": ["Smart Contracts", "Ethereum", "Programming"]
            }
        ]
    }
    
    try:
        # Save to temporary file
        with open("blockchain_data.json", "w") as f:
            json.dump(json_data, f, indent=2)
        
        result = agent.invoke({
            "messages": [{"role": "user", "content": "I've uploaded a JSON file called 'blockchain_data.json' with blockchain information. Please process it and add it to a collection called 'BlockchainKnowledge'"}]
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
        
        # Clean up
        os.remove("blockchain_data.json")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: CSV data upload
    print("\n2. Uploading CSV data...")
    csv_content = """title,content,topic,difficulty,tags
Python Programming,Learn Python from basics to advanced,Programming,Beginner,"Python,Programming,Basics"
Data Science,Comprehensive guide to data science,Data Science,Intermediate,"Data Science,Python,Statistics"
Machine Learning,Introduction to ML algorithms,AI/ML,Advanced,"Machine Learning,AI,Algorithms"
Web Development,Building modern web applications,Web Development,Intermediate,"Web Development,HTML,CSS,JavaScript"
Database Design,Principles of database design,Database,Intermediate,"Database,SQL,Design" """
    
    try:
        with open("tech_topics.csv", "w") as f:
            f.write(csv_content)
        
        result = agent.invoke({
            "messages": [{"role": "user", "content": "I've uploaded a CSV file called 'tech_topics.csv' with technology topics. Please process it and add it to a collection called 'TechTopics'"}]
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
        
        # Clean up
        os.remove("tech_topics.csv")
        
    except Exception as e:
        print(f"Error: {e}")

def demonstrate_search_capabilities():
    """Demonstrate search capabilities."""
    
    print("\n🔍 Search Capabilities")
    print("=" * 25)
    
    # Example 1: Semantic search
    print("\n1. Semantic search for 'artificial intelligence'...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Search for information about artificial intelligence across all collections"}]
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Hybrid search
    print("\n2. Hybrid search for 'machine learning algorithms'...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Perform a hybrid search for 'machine learning algorithms' to find both exact matches and similar concepts"}]
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Specific collection search
    print("\n3. Search in specific collection...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Search for 'blockchain technology' in the BlockchainKnowledge collection"}]
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
    except Exception as e:
        print(f"Error: {e}")

def demonstrate_collection_management():
    """Demonstrate collection management capabilities."""
    
    print("\n📚 Collection Management")
    print("=" * 25)
    
    # Example 1: List all collections
    print("\n1. Listing all collections...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Show me all available collections and their basic information"}]
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Get detailed collection info
    print("\n2. Getting detailed collection information...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Show me detailed information about the TechTopics collection"}]
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
    except Exception as e:
        print(f"Error: {e}")

def demonstrate_advanced_workflows():
    """Demonstrate advanced workflows."""
    
    print("\n🚀 Advanced Workflows")
    print("=" * 20)
    
    # Example 1: Research and compare
    print("\n1. Research and compare two technologies...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "Research both 'React' and 'Vue.js' web frameworks, create collections for each, and then search for similarities and differences between them"}]
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Multi-step knowledge building
    print("\n2. Multi-step knowledge building...")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": "First, research 'cloud computing basics' and create a collection. Then, research 'AWS services' and add it to the same collection. Finally, search for 'scalability' in that collection."}
        })
        print(f"Response: {result['messages'][-1]['content'][:400]}...")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main function to run all demonstrations."""
    
    print("🤖 Weaviate Agent Comprehensive Demo")
    print("=" * 50)
    print("This demo showcases all the key features of the Weaviate agent:")
    print("- Web research and knowledge base creation")
    print("- File upload and processing")
    print("- Semantic and hybrid search")
    print("- Collection management")
    print("- Advanced workflows")
    print("\nNote: Make sure your .env file contains valid Weaviate credentials!")
    print("=" * 50)
    
    # Run all demonstrations
    demonstrate_web_research()
    demonstrate_file_upload()
    demonstrate_search_capabilities()
    demonstrate_collection_management()
    demonstrate_advanced_workflows()
    
    print("\n✅ Demo completed! The Weaviate agent is ready for use.")
    print("\nNext steps:")
    print("1. Use the agent through the UI by selecting 'Weaviate Agent'")
    print("2. Try uploading your own files")
    print("3. Research topics that interest you")
    print("4. Build comprehensive knowledge bases")

if __name__ == "__main__":
    main()
