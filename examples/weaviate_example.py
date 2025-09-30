#!/usr/bin/env python3
"""
Example showing how to use Weaviate tools with Deep Agents.

This demonstrates creating a knowledge base and performing semantic search.
"""

import os
from dotenv import load_dotenv
from deepagents import create_deep_agent
from src.tools.weaviate_tools import (
    create_weaviate_collection,
    add_documents_to_weaviate,
    search_similar_documents,
    hybrid_search_documents,
    check_weaviate_connection,
)

# Load environment variables
load_dotenv()

def setup_knowledge_base():
    """Set up a sample knowledge base with Weaviate."""
    
    print("📚 Setting up knowledge base...")
    
    # Check connection first
    connection_result = check_weaviate_connection()
    print(f"Connection: {connection_result}")
    
    if "❌" in connection_result:
        print("Please check your Weaviate credentials in .env file")
        return None
    
    # Create collection
    collection_name = "KnowledgeBase"
    properties = [
        {"name": "title", "data_type": "text"},
        {"name": "content", "data_type": "text"},
        {"name": "topic", "data_type": "text"},
        {"name": "difficulty", "data_type": "text"}
    ]
    
    create_result = create_weaviate_collection(collection_name, properties)
    print(f"Collection creation: {create_result}")
    
    # Add sample knowledge documents
    knowledge_docs = [
        {
            "title": "Introduction to Machine Learning",
            "content": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed. It involves algorithms that can identify patterns in data and make predictions or classifications.",
            "topic": "Machine Learning",
            "difficulty": "Beginner"
        },
        {
            "title": "Deep Learning Fundamentals",
            "content": "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model and understand complex patterns in data. It has revolutionized fields like computer vision, natural language processing, and speech recognition.",
            "topic": "Deep Learning",
            "difficulty": "Intermediate"
        },
        {
            "title": "Python for Data Science",
            "content": "Python is a powerful programming language for data science, offering libraries like NumPy, Pandas, Matplotlib, and Scikit-learn. It's widely used for data analysis, visualization, and machine learning projects.",
            "topic": "Programming",
            "difficulty": "Beginner"
        },
        {
            "title": "Neural Network Architecture",
            "content": "Neural networks consist of interconnected nodes (neurons) organized in layers. The architecture includes input layers, hidden layers, and output layers. Different architectures like CNNs, RNNs, and Transformers are suited for different tasks.",
            "topic": "Neural Networks",
            "difficulty": "Advanced"
        },
        {
            "title": "Data Preprocessing Techniques",
            "content": "Data preprocessing is crucial for machine learning success. It includes cleaning data, handling missing values, feature scaling, encoding categorical variables, and splitting data into training and testing sets.",
            "topic": "Data Science",
            "difficulty": "Intermediate"
        }
    ]
    
    add_result = add_documents_to_weaviate(collection_name, knowledge_docs)
    print(f"Documents added: {add_result}")
    
    return collection_name

def main():
    """Main function demonstrating Weaviate tools with Deep Agents."""
    
    print("🤖 Deep Agents with Weaviate Integration")
    print("=" * 50)
    
    # Set up knowledge base
    collection_name = setup_knowledge_base()
    if not collection_name:
        return
    
    # Create agent with Weaviate tools
    agent = create_deep_agent(
        tools=[
            search_similar_documents,
            hybrid_search_documents,
            check_weaviate_connection
        ],
        instructions=f"""You are a helpful AI assistant with access to a knowledge base stored in Weaviate.

Available tools:
- search_similar_documents: Search for similar content using vector similarity
- hybrid_search_documents: Combine vector and keyword search for better results
- check_weaviate_connection: Verify Weaviate connection status

The knowledge base collection is called '{collection_name}' and contains information about:
- Machine Learning
- Deep Learning  
- Python Programming
- Neural Networks
- Data Science

When users ask questions, use the search tools to find relevant information from the knowledge base.
Always provide helpful and accurate answers based on the search results.""",
    )
    
    print("\n🔍 Testing the agent with knowledge base queries...")
    print("-" * 50)
    
    # Test queries
    test_queries = [
        "What is machine learning and how does it work?",
        "Tell me about neural networks and their architecture",
        "How can I get started with Python for data science?",
        "What are the key steps in data preprocessing?"
    ]
    
    for query in test_queries:
        print(f"\nUser: {query}")
        try:
            result = agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })
            print(f"Agent: {result['messages'][-1]['content'][:300]}...")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n✅ Example completed! The agent can now search the knowledge base using Weaviate.")

if __name__ == "__main__":
    main()
