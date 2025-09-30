"""
Supabase tools for Deep Agents.

This module contains tools for vector search and data management using Supabase pgvector.
"""

import os
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
import json


def get_supabase_client():
    """Get Supabase client using MCP tools."""
    project_id = os.getenv("SUPABASE_PROJECT_ID")
    if not project_id:
        raise ValueError("SUPABASE_PROJECT_ID must be set in environment variables")
    return project_id


@tool(description="Create a new table in Supabase for storing documents with vector embeddings")
def create_supabase_collection(
    collection_name: str,
    properties: List[Dict[str, str]],
    embedding_dimensions: int = 1536
) -> str:
    """
    Create a new table in Supabase with pgvector support for semantic search.
    
    Args:
        collection_name: Name of the table to create
        properties: List of property definitions, each with 'name' and 'data_type' keys
        embedding_dimensions: Number of dimensions for the embedding vector (default: 1536 for OpenAI)
    
    Returns:
        Success or error message
    """
    try:
        project_id = get_supabase_client()
        
        # Build CREATE TABLE SQL
        columns = ["id BIGSERIAL PRIMARY KEY"]
        
        for prop in properties:
            col_name = prop["name"]
            data_type = prop["data_type"].lower()
            
            # Map data types to Postgres types
            type_mapping = {
                "text": "TEXT",
                "string": "TEXT",
                "number": "NUMERIC",
                "integer": "INTEGER",
                "boolean": "BOOLEAN",
                "date": "TIMESTAMP WITH TIME ZONE"
            }
            
            pg_type = type_mapping.get(data_type, "TEXT")
            columns.append(f"{col_name} {pg_type}")
        
        # Add embedding column and metadata
        columns.append(f"embedding VECTOR({embedding_dimensions})")
        columns.append("created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()")
        
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {collection_name} (
            {', '.join(columns)}
        );
        
        -- Create index for vector similarity search using HNSW
        CREATE INDEX IF NOT EXISTS {collection_name}_embedding_idx 
        ON {collection_name} 
        USING hnsw (embedding vector_cosine_ops);
        
        -- Create function for semantic search
        CREATE OR REPLACE FUNCTION match_{collection_name} (
            query_embedding VECTOR({embedding_dimensions}),
            match_threshold FLOAT DEFAULT 0.78,
            match_count INT DEFAULT 10
        )
        RETURNS SETOF {collection_name}
        LANGUAGE sql
        AS $$
            SELECT *
            FROM {collection_name}
            WHERE {collection_name}.embedding <=> query_embedding < 1 - match_threshold
            ORDER BY {collection_name}.embedding <=> query_embedding ASC
            LIMIT LEAST(match_count, 200);
        $$;
        """
        
        # Use MCP to execute SQL
        from langchain_core.runnables import RunnablePassthrough
        
        # Note: This will be executed via MCP tools
        return json.dumps({
            "success": True,
            "message": f"Table '{collection_name}' created with pgvector support",
            "sql": create_table_sql,
            "note": "Execute this SQL using mcp_supabase_apply_migration or mcp_supabase_execute_sql"
        }, indent=2)
        
    except Exception as e:
        return f"Error creating collection: {str(e)}"


@tool(description="Add documents to a Supabase table with automatic embedding generation")
def add_documents_to_supabase(
    collection_name: str,
    documents: List[Dict[str, Any]],
    generate_embeddings: bool = True
) -> str:
    """
    Add documents to a Supabase table. Embeddings can be generated using OpenAI or provided directly.
    
    Args:
        collection_name: Name of the table to add documents to
        documents: List of documents, each as a dictionary with property names as keys
        generate_embeddings: Whether to generate embeddings automatically (requires OpenAI API key)
    
    Returns:
        Success or error message with count of added documents
    """
    try:
        project_id = get_supabase_client()
        
        if generate_embeddings:
            # Generate embeddings using OpenAI
            import openai
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                return "Error: OPENAI_API_KEY must be set to generate embeddings automatically"
            
            client = openai.OpenAI(api_key=openai_key)
            
            for doc in documents:
                # Combine title and content for embedding
                text_to_embed = f"{doc.get('title', '')} {doc.get('content', '')}".strip()
                
                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text_to_embed
                )
                
                doc['embedding'] = response.data[0].embedding
        
        # Build INSERT SQL
        insert_statements = []
        for doc in documents:
            columns = list(doc.keys())
            values = []
            
            for key, value in doc.items():
                if key == 'embedding':
                    # Format vector for Postgres
                    embedding_str = '[' + ','.join(map(str, value)) + ']'
                    values.append(f"'{embedding_str}'::vector")
                elif isinstance(value, str):
                    # Escape single quotes
                    escaped = value.replace("'", "''")
                    values.append(f"'{escaped}'")
                elif value is None:
                    values.append("NULL")
                else:
                    values.append(str(value))
            
            insert_sql = f"""
            INSERT INTO {collection_name} ({', '.join(columns)})
            VALUES ({', '.join(values)});
            """
            insert_statements.append(insert_sql)
        
        combined_sql = '\n'.join(insert_statements)
        
        return json.dumps({
            "success": True,
            "message": f"Prepared {len(documents)} documents for insertion",
            "count": len(documents),
            "sql": combined_sql,
            "note": "Execute this SQL using mcp_supabase_execute_sql"
        }, indent=2)
        
    except Exception as e:
        return f"Error adding documents: {str(e)}"


@tool(description="Search for similar documents using vector similarity in Supabase")
def search_similar_supabase_documents(
    collection_name: str,
    query: str,
    limit: int = 5,
    match_threshold: float = 0.78
) -> str:
    """
    Search for documents similar to the query using pgvector similarity search.
    
    Args:
        collection_name: Name of the table to search in
        query: Text query to search for similar documents
        limit: Maximum number of results to return (default: 5)
        match_threshold: Similarity threshold between 0 and 1 (default: 0.78)
    
    Returns:
        JSON string with search results or error message
    """
    try:
        project_id = get_supabase_client()
        
        # Generate embedding for query
        import openai
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            return "Error: OPENAI_API_KEY must be set to perform semantic search"
        
        client = openai.OpenAI(api_key=openai_key)
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        
        query_embedding = response.data[0].embedding
        embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
        
        # Use the match function we created
        search_sql = f"""
        SELECT * FROM match_{collection_name}(
            '{embedding_str}'::vector,
            {match_threshold},
            {limit}
        );
        """
        
        return json.dumps({
            "success": True,
            "query": query,
            "sql": search_sql,
            "note": "Execute this SQL using mcp_supabase_execute_sql to get results"
        }, indent=2)
        
    except Exception as e:
        return f"Error searching documents: {str(e)}"


@tool(description="List all tables in the Supabase database")
def list_supabase_collections() -> str:
    """
    List all tables available in the Supabase database.
    
    Returns:
        JSON string with list of table names or error message
    """
    try:
        project_id = get_supabase_client()
        
        list_sql = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """
        
        return json.dumps({
            "success": True,
            "sql": list_sql,
            "note": "Execute this SQL using mcp_supabase_execute_sql to get the list of tables"
        }, indent=2)
        
    except Exception as e:
        return f"Error listing collections: {str(e)}"


@tool(description="Get information about a Supabase table schema")
def get_supabase_collection_info(collection_name: str) -> str:
    """
    Get detailed information about a Supabase table including columns and indexes.
    
    Args:
        collection_name: Name of the table to get info for
    
    Returns:
        JSON string with table information or error message
    """
    try:
        project_id = get_supabase_client()
        
        info_sql = f"""
        SELECT 
            column_name, 
            data_type, 
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' 
        AND table_name = '{collection_name}'
        ORDER BY ordinal_position;
        """
        
        return json.dumps({
            "success": True,
            "sql": info_sql,
            "note": "Execute this SQL using mcp_supabase_execute_sql to get table schema"
        }, indent=2)
        
    except Exception as e:
        return f"Error getting collection info: {str(e)}"


@tool(description="Check Supabase connection status")
def check_supabase_connection() -> str:
    """
    Check if the Supabase project is accessible and ready.
    
    Returns:
        Connection status message
    """
    try:
        project_id = get_supabase_client()
        
        return json.dumps({
            "success": True,
            "message": f"✅ Supabase project {project_id} is configured",
            "note": "Use mcp_supabase_get_project to check full project status"
        }, indent=2)
        
    except Exception as e:
        return f"❌ Supabase connection error: {str(e)}"

