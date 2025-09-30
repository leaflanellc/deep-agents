"""
Weaviate tools for Deep Agents.

This module contains tools for vector search and data management using Weaviate.
"""

import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
from typing import List, Dict, Any, Optional, Union
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langchain.tools.tool_node import InjectedState
from typing import Annotated
import json


class WeaviateClient:
    """Weaviate client wrapper for managing connections and operations."""
    
    def __init__(self):
        """Initialize Weaviate client with credentials from environment."""
        self.weaviate_url = os.getenv("WEAVIATE_URL")
        self.weaviate_key = os.getenv("WEAVIATE_API_KEY")
        
        if not self.weaviate_url or not self.weaviate_key:
            raise ValueError(
                "WEAVIATE_URL and WEAVIATE_API_KEY must be set in environment variables"
            )
        
        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=self.weaviate_url,
            auth_credentials=Auth.api_key(self.weaviate_key),
        )
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'client'):
            self.client.close()
    
    def is_ready(self) -> bool:
        """Check if Weaviate client is ready."""
        try:
            return self.client.is_ready()
        except Exception:
            return False
    
    def create_collection(
        self, 
        collection_name: str, 
        properties: List[Dict[str, Any]], 
        model: str = "Snowflake/snowflake-arctic-embed-l-v2.0",
        dimensions: Optional[int] = None
    ) -> bool:
        """Create a new collection with vectorization."""
        try:
            # Convert properties to Weaviate format
            weaviate_properties = []
            for prop in properties:
                weaviate_properties.append(
                    Property(
                        name=prop["name"],
                        data_type=getattr(DataType, prop["data_type"].upper())
                    )
                )
            
            # Create collection with Weaviate Embeddings vectorization
            if model and model != "none":
                # Use Weaviate's native embedding service with Snowflake models
                # Note: Using vectorizer_config as vector_config format is not working correctly
                collection = self.client.collections.create(
                    name=collection_name,
                    properties=weaviate_properties,
                    vectorizer_config=Configure.Vectorizer.text2vec_weaviate(
                        model=model,
                        vectorize_collection_name=False
                    )
                )
            else:
                collection = self.client.collections.create(
                    name=collection_name,
                    properties=weaviate_properties
                )
            return True
        except Exception as e:
            print(f"Error creating collection: {e}")
            return False
    
    def add_documents(
        self, 
        collection_name: str, 
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Add documents to a collection."""
        try:
            collection = self.client.collections.use(collection_name)
            
            # Batch insert documents
            with collection.batch.dynamic() as batch:
                for doc in documents:
                    batch.add_object(properties=doc)
            
            return {"success": True, "count": len(documents)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_similar(
        self, 
        collection_name: str, 
        query: str, 
        limit: int = 5,
        properties: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Search for similar documents using vector similarity."""
        try:
            collection = self.client.collections.use(collection_name)
            
            # Perform vector search
            response = collection.query.near_text(
                query=query,
                limit=limit,
                return_metadata=MetadataQuery(distance=True, score=True)
            )
            
            results = []
            for obj in response.objects:
                result = {
                    "properties": obj.properties,
                    "metadata": {
                        "distance": obj.metadata.distance,
                        "score": obj.metadata.score
                    }
                }
                results.append(result)
            
            return {"success": True, "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def hybrid_search(
        self, 
        collection_name: str, 
        query: str, 
        limit: int = 5,
        alpha: float = 0.5
    ) -> Dict[str, Any]:
        """Perform hybrid search combining vector and keyword search."""
        try:
            collection = self.client.collections.use(collection_name)
            
            # Perform hybrid search
            response = collection.query.hybrid(
                query=query,
                limit=limit,
                alpha=alpha,
                return_metadata=MetadataQuery(distance=True, score=True)
            )
            
            results = []
            for obj in response.objects:
                result = {
                    "properties": obj.properties,
                    "metadata": {
                        "distance": obj.metadata.distance,
                        "score": obj.metadata.score
                    }
                }
                results.append(result)
            
            return {"success": True, "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """Get information about a collection."""
        try:
            collection = self.client.collections.use(collection_name)
            config = collection.config.get()
            
            return {
                "success": True,
                "name": config.name,
                "properties": [prop.name for prop in config.properties],
                "vectorizer": config.vectorizer_config if hasattr(config, 'vectorizer_config') else None
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_collections(self) -> Dict[str, Any]:
        """List all collections in the database."""
        try:
            collections = self.client.collections.list_all()
            collection_names = [col.name for col in collections]
            return {"success": True, "collections": collection_names}
        except Exception as e:
            return {"success": False, "error": str(e)}


@tool(description="Create a new Weaviate collection with vectorization capabilities")
def create_weaviate_collection(
    collection_name: str,
    properties: List[Dict[str, str]],
    model: str = "Snowflake/snowflake-arctic-embed-l-v2.0",
    dimensions: Optional[int] = None
) -> str:
    """
    Create a new Weaviate collection with specified properties and vectorization model.
    
    Args:
        collection_name: Name of the collection to create
        properties: List of property definitions, each with 'name' and 'data_type' keys
        model: Vectorization model to use (default: Snowflake/snowflake-arctic-embed-l-v2.0)
        dimensions: Optional number of dimensions for the vector (if not using default)
    
    Returns:
        Success or error message
    """
    try:
        with WeaviateClient() as client:
            if not client.is_ready():
                return "Error: Weaviate client is not ready. Check your connection."
            
            success = client.create_collection(collection_name, properties, model, dimensions)
            if success:
                return f"Successfully created collection '{collection_name}' with {len(properties)} properties"
            else:
                return f"Failed to create collection '{collection_name}'"
    except Exception as e:
        return f"Error creating collection: {str(e)}"


@tool(description="Add documents to a Weaviate collection")
def add_documents_to_weaviate(
    collection_name: str,
    documents: List[Dict[str, Any]]
) -> str:
    """
    Add documents to a Weaviate collection for vectorization and search.
    
    Args:
        collection_name: Name of the collection to add documents to
        documents: List of documents, each as a dictionary with property names as keys
    
    Returns:
        Success or error message with count of added documents
    """
    try:
        with WeaviateClient() as client:
            if not client.is_ready():
                return "Error: Weaviate client is not ready. Check your connection."
            
            result = client.add_documents(collection_name, documents)
            if result["success"]:
                return f"Successfully added {result['count']} documents to collection '{collection_name}'"
            else:
                return f"Error adding documents: {result['error']}"
    except Exception as e:
        return f"Error adding documents: {str(e)}"


@tool(description="Search for similar documents using vector similarity")
def search_similar_documents(
    collection_name: str,
    query: str,
    limit: int = 5,
    properties: Optional[List[str]] = None
) -> str:
    """
    Search for documents similar to the query using vector similarity.
    
    Args:
        collection_name: Name of the collection to search in
        query: Text query to search for similar documents
        limit: Maximum number of results to return (default: 5)
        properties: Optional list of specific properties to return
    
    Returns:
        JSON string with search results or error message
    """
    try:
        with WeaviateClient() as client:
            if not client.is_ready():
                return "Error: Weaviate client is not ready. Check your connection."
            
            result = client.search_similar(collection_name, query, limit, properties)
            if result["success"]:
                return json.dumps(result["results"], indent=2)
            else:
                return f"Error searching documents: {result['error']}"
    except Exception as e:
        return f"Error searching documents: {str(e)}"


@tool(description="Perform hybrid search combining vector similarity and keyword matching")
def hybrid_search_documents(
    collection_name: str,
    query: str,
    limit: int = 5,
    alpha: float = 0.5
) -> str:
    """
    Perform hybrid search that combines vector similarity with keyword matching.
    
    Args:
        collection_name: Name of the collection to search in
        query: Text query to search for
        limit: Maximum number of results to return (default: 5)
        alpha: Balance between vector search (1.0) and keyword search (0.0), default: 0.5
    
    Returns:
        JSON string with search results or error message
    """
    try:
        with WeaviateClient() as client:
            if not client.is_ready():
                return "Error: Weaviate client is not ready. Check your connection."
            
            result = client.hybrid_search(collection_name, query, limit, alpha)
            if result["success"]:
                return json.dumps(result["results"], indent=2)
            else:
                return f"Error performing hybrid search: {result['error']}"
    except Exception as e:
        return f"Error performing hybrid search: {str(e)}"


@tool(description="Get information about a Weaviate collection")
def get_weaviate_collection_info(collection_name: str) -> str:
    """
    Get detailed information about a Weaviate collection.
    
    Args:
        collection_name: Name of the collection to get info for
    
    Returns:
        JSON string with collection information or error message
    """
    try:
        with WeaviateClient() as client:
            if not client.is_ready():
                return "Error: Weaviate client is not ready. Check your connection."
            
            result = client.get_collection_info(collection_name)
            if result["success"]:
                return json.dumps(result, indent=2)
            else:
                return f"Error getting collection info: {result['error']}"
    except Exception as e:
        return f"Error getting collection info: {str(e)}"


@tool(description="List all collections in the Weaviate database")
def list_weaviate_collections() -> str:
    """
    List all collections available in the Weaviate database.
    
    Returns:
        JSON string with list of collection names or error message
    """
    try:
        with WeaviateClient() as client:
            if not client.is_ready():
                return "Error: Weaviate client is not ready. Check your connection."
            
            result = client.list_collections()
            if result["success"]:
                return json.dumps(result, indent=2)
            else:
                return f"Error listing collections: {result['error']}"
    except Exception as e:
        return f"Error listing collections: {str(e)}"


@tool(description="Check Weaviate connection status")
def check_weaviate_connection() -> str:
    """
    Check if the Weaviate client can connect successfully.
    
    Returns:
        Connection status message
    """
    try:
        with WeaviateClient() as client:
            if client.is_ready():
                return "✅ Weaviate connection successful"
            else:
                return "❌ Weaviate connection failed"
    except Exception as e:
        return f"❌ Weaviate connection error: {str(e)}"
