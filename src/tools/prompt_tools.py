"""
Prompt management tools for Deep Agents.

This module contains tools for managing stored prompts including
creating, reading, updating, and deleting prompts in the database.
"""

import json
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from .database_tools import get_database_client


@tool(description="Create a new prompt template in the database")
def create_prompt_template(
    name: str,
    description: str,
    content: str,
    category: str = "general",
    tags: Optional[List[str]] = None
) -> str:
    """
    Create a new prompt template in the database.
    
    Args:
        name: Name of the prompt template
        description: Description of what the prompt is for
        content: The actual prompt content
        category: Category for organizing prompts (default: "general")
        tags: Optional list of tags for the prompt
    
    Returns:
        Success or error message
    """
    try:
        client = get_database_client()
        
        # Ensure prompts table exists
        create_prompts_table_sql = """
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            tags TEXT, -- JSON array of tags
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
        client.execute_update(create_prompts_table_sql)
        
        # Prepare tags as JSON string
        tags_json = json.dumps(tags or [])
        
        # Insert the new prompt
        insert_sql = """
        INSERT INTO prompts (name, description, content, category, tags)
        VALUES (?, ?, ?, ?, ?)
        """
        
        affected_rows = client.execute_update(
            insert_sql, 
            (name, description, content, category, tags_json)
        )
        
        if affected_rows > 0:
            return json.dumps({
                "success": True,
                "message": f"Prompt template '{name}' created successfully",
                "prompt_id": client.execute_query("SELECT last_insert_rowid() as id")[0]["id"]
            }, indent=2)
        else:
            return "Error: Failed to create prompt template"
        
    except Exception as e:
        return f"Error creating prompt template: {str(e)}"


@tool(description="Get a specific prompt template by name")
def get_prompt_template(name: str) -> str:
    """
    Retrieve a specific prompt template by name.
    
    Args:
        name: Name of the prompt template to retrieve
    
    Returns:
        JSON string with prompt template data or error message
    """
    try:
        client = get_database_client()
        
        query_sql = "SELECT * FROM prompts WHERE name = ?"
        results = client.execute_query(query_sql, (name,))
        
        if results:
            prompt = results[0]
            # Parse tags from JSON
            prompt["tags"] = json.loads(prompt["tags"] or "[]")
            return json.dumps({
                "success": True,
                "prompt": prompt
            }, indent=2)
        else:
            return json.dumps({
                "success": False,
                "message": f"Prompt template '{name}' not found"
            }, indent=2)
        
    except Exception as e:
        return f"Error retrieving prompt template: {str(e)}"


@tool(description="List all prompt templates with optional filtering")
def list_prompt_templates(
    category: Optional[str] = None,
    limit: int = 50
) -> str:
    """
    List all prompt templates with optional category filtering.
    
    Args:
        category: Optional category to filter by
        limit: Maximum number of results to return (default: 50)
    
    Returns:
        JSON string with list of prompt templates
    """
    try:
        client = get_database_client()
        
        if category:
            query_sql = "SELECT * FROM prompts WHERE category = ? ORDER BY updated_at DESC LIMIT ?"
            params = (category, limit)
        else:
            query_sql = "SELECT * FROM prompts ORDER BY updated_at DESC LIMIT ?"
            params = (limit,)
        
        results = client.execute_query(query_sql, params)
        
        # Parse tags from JSON for each prompt
        for prompt in results:
            prompt["tags"] = json.loads(prompt["tags"] or "[]")
        
        return json.dumps({
            "success": True,
            "prompts": results,
            "count": len(results)
        }, indent=2)
        
    except Exception as e:
        return f"Error listing prompt templates: {str(e)}"


@tool(description="Update an existing prompt template")
def update_prompt_template(
    name: str,
    description: Optional[str] = None,
    content: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> str:
    """
    Update an existing prompt template.
    
    Args:
        name: Name of the prompt template to update
        description: New description (optional)
        content: New content (optional)
        category: New category (optional)
        tags: New tags (optional)
    
    Returns:
        Success or error message
    """
    try:
        client = get_database_client()
        
        # Build dynamic UPDATE query
        update_fields = []
        params = []
        
        if description is not None:
            update_fields.append("description = ?")
            params.append(description)
        
        if content is not None:
            update_fields.append("content = ?")
            params.append(content)
        
        if category is not None:
            update_fields.append("category = ?")
            params.append(category)
        
        if tags is not None:
            update_fields.append("tags = ?")
            params.append(json.dumps(tags))
        
        if not update_fields:
            return "Error: No fields to update"
        
        # Add updated_at timestamp
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        update_sql = f"UPDATE prompts SET {', '.join(update_fields)} WHERE name = ?"
        params.append(name)
        
        affected_rows = client.execute_update(update_sql, tuple(params))
        
        if affected_rows > 0:
            return json.dumps({
                "success": True,
                "message": f"Prompt template '{name}' updated successfully"
            }, indent=2)
        else:
            return json.dumps({
                "success": False,
                "message": f"Prompt template '{name}' not found"
            }, indent=2)
        
    except Exception as e:
        return f"Error updating prompt template: {str(e)}"


@tool(description="Delete a prompt template")
def delete_prompt_template(name: str) -> str:
    """
    Delete a prompt template by name.
    
    Args:
        name: Name of the prompt template to delete
    
    Returns:
        Success or error message
    """
    try:
        client = get_database_client()
        
        delete_sql = "DELETE FROM prompts WHERE name = ?"
        affected_rows = client.execute_update(delete_sql, (name,))
        
        if affected_rows > 0:
            return json.dumps({
                "success": True,
                "message": f"Prompt template '{name}' deleted successfully"
            }, indent=2)
        else:
            return json.dumps({
                "success": False,
                "message": f"Prompt template '{name}' not found"
            }, indent=2)
        
    except Exception as e:
        return f"Error deleting prompt template: {str(e)}"


@tool(description="Search prompt templates by content or tags")
def search_prompt_templates(
    query: str,
    limit: int = 20
) -> str:
    """
    Search prompt templates by content or tags.
    
    Args:
        query: Search query to match against content, description, or tags
        limit: Maximum number of results to return (default: 20)
    
    Returns:
        JSON string with matching prompt templates
    """
    try:
        client = get_database_client()
        
        search_sql = """
        SELECT * FROM prompts 
        WHERE name LIKE ? 
           OR description LIKE ? 
           OR content LIKE ? 
           OR tags LIKE ?
        ORDER BY updated_at DESC 
        LIMIT ?
        """
        
        search_term = f"%{query}%"
        results = client.execute_query(
            search_sql, 
            (search_term, search_term, search_term, search_term, limit)
        )
        
        # Parse tags from JSON for each prompt
        for prompt in results:
            prompt["tags"] = json.loads(prompt["tags"] or "[]")
        
        return json.dumps({
            "success": True,
            "query": query,
            "prompts": results,
            "count": len(results)
        }, indent=2)
        
    except Exception as e:
        return f"Error searching prompt templates: {str(e)}"


@tool(description="Get all available prompt categories")
def get_prompt_categories() -> str:
    """
    Get all unique categories from stored prompts.
    
    Returns:
        JSON string with list of categories
    """
    try:
        client = get_database_client()
        
        categories_sql = "SELECT DISTINCT category FROM prompts ORDER BY category"
        results = client.execute_query(categories_sql)
        
        categories = [row["category"] for row in results if row["category"]]
        
        return json.dumps({
            "success": True,
            "categories": categories,
            "count": len(categories)
        }, indent=2)
        
    except Exception as e:
        return f"Error getting prompt categories: {str(e)}"


@tool(description="Use a stored prompt template with variable substitution")
def use_prompt_template(
    name: str,
    variables: Optional[Dict[str, str]] = None
) -> str:
    """
    Use a stored prompt template with variable substitution.
    
    Args:
        name: Name of the prompt template to use
        variables: Dictionary of variables to substitute in the prompt
    
    Returns:
        The processed prompt with variables substituted
    """
    try:
        client = get_database_client()
        
        # Get the prompt template
        get_sql = "SELECT content FROM prompts WHERE name = ?"
        results = client.execute_query(get_sql, (name,))
        
        if not results:
            return f"Error: Prompt template '{name}' not found"
        
        content = results[0]["content"]
        
        # Perform variable substitution if variables provided
        if variables:
            for key, value in variables.items():
                content = content.replace(f"{{{key}}}", str(value))
        
        return json.dumps({
            "success": True,
            "prompt_name": name,
            "processed_content": content,
            "variables_used": list(variables.keys()) if variables else []
        }, indent=2)
        
    except Exception as e:
        return f"Error using prompt template: {str(e)}"
