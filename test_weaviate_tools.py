#!/usr/bin/env python3
"""
Test script for Weaviate tools.

This script demonstrates how to use the Weaviate tools with Deep Agents.
"""

import os
from dotenv import load_dotenv
from src.tools.weaviate_tools import (
    check_weaviate_connection,
    create_weaviate_collection,
    add_documents_to_weaviate,
    search_similar_documents,
    hybrid_search_documents,
    list_weaviate_collections,
    get_weaviate_collection_info,
)

# Load environment variables
load_dotenv()

def test_weaviate_tools():
    """Test the Weaviate tools functionality."""
    
    print("🔍 Testing Weaviate Tools")
    print("=" * 50)
    
    # Test 1: Check connection
    print("\n1. Testing Weaviate connection...")
    connection_result = check_weaviate_connection()
    print(f"   {connection_result}")
    
    if "❌" in connection_result:
        print("\n⚠️  Weaviate connection failed. Please check your .env file:")
        print("   - WEAVIATE_URL should be your Weaviate Cloud URL")
        print("   - WEAVIATE_API_KEY should be your Weaviate API key")
        return
    
    # Test 2: List existing collections
    print("\n2. Listing existing collections...")
    collections_result = list_weaviate_collections()
    print(f"   Collections: {collections_result}")
    
    # Test 3: Create a test collection
    print("\n3. Creating test collection...")
    collection_name = "TestCollection"
    properties = [
        {"name": "title", "data_type": "text"},
        {"name": "description", "data_type": "text"},
        {"name": "category", "data_type": "text"}
    ]
    
    create_result = create_weaviate_collection(collection_name, properties)
    print(f"   {create_result}")
    
    # Test 4: Add sample documents
    print("\n4. Adding sample documents...")
    sample_documents = [
        {
            "title": "Machine Learning Basics",
            "description": "An introduction to machine learning concepts and algorithms",
            "category": "AI/ML"
        },
        {
            "title": "Python Programming",
            "description": "Learn Python programming from basics to advanced topics",
            "category": "Programming"
        },
        {
            "title": "Data Science with Python",
            "description": "Comprehensive guide to data science using Python libraries",
            "category": "Data Science"
        },
        {
            "title": "Web Development",
            "description": "Building modern web applications with HTML, CSS, and JavaScript",
            "category": "Web Development"
        },
        {
            "title": "Database Design",
            "description": "Principles of database design and SQL optimization",
            "category": "Database"
        }
    ]
    
    add_result = add_documents_to_weaviate(collection_name, sample_documents)
    print(f"   {add_result}")
    
    # Test 5: Search similar documents
    print("\n5. Testing vector search...")
    search_queries = [
        "artificial intelligence and algorithms",
        "web programming languages",
        "data analysis and statistics"
    ]
    
    for query in search_queries:
        print(f"\n   Query: '{query}'")
        search_result = search_similar_documents(collection_name, query, limit=2)
        print(f"   Results: {search_result[:200]}...")  # Truncate for readability
    
    # Test 6: Hybrid search
    print("\n6. Testing hybrid search...")
    hybrid_result = hybrid_search_documents(collection_name, "Python programming", limit=3)
    print(f"   Hybrid search results: {hybrid_result[:200]}...")
    
    # Test 7: Get collection info
    print("\n7. Getting collection information...")
    info_result = get_weaviate_collection_info(collection_name)
    print(f"   Collection info: {info_result}")
    
    print("\n✅ Weaviate tools test completed!")

if __name__ == "__main__":
    test_weaviate_tools()
