"""
Local database tools for Deep Agents.

This module contains tools for SQLite database operations including
table creation, data insertion, querying, and schema management.
"""

import sqlite3
import json
import os
from typing import List, Dict, Any, Optional, Union
from langchain_core.tools import tool
from datetime import datetime
import re


class DatabaseClient:
    """SQLite client wrapper for managing database connections and operations."""
    
    def __init__(self, db_path: str = "research_database.db"):
        """Initialize SQLite client with database path."""
        self.db_path = db_path
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Ensure the database file exists and is accessible."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("SELECT 1")
        except sqlite3.Error as e:
            raise ValueError(f"Database error: {str(e)}")
    
    def get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dictionaries."""
        try:
            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            raise ValueError(f"Query execution error: {str(e)}")
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows count."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            raise ValueError(f"Update execution error: {str(e)}")
    
    def is_safe_query(self, query: str) -> bool:
        """Check if a query is safe to execute (basic SQL injection prevention)."""
        # Convert to lowercase for checking
        query_lower = query.lower().strip()
        
        # Allow only specific operations
        allowed_operations = ['select', 'insert', 'update', 'delete', 'create', 'drop']
        first_word = query_lower.split()[0] if query_lower.split() else ""
        
        if first_word not in allowed_operations:
            return False
        
        # Block dangerous patterns
        dangerous_patterns = [
            'drop table',
            'drop database',
            'truncate',
            'alter table',
            'grant',
            'revoke',
            'exec',
            'execute',
            'sp_',
            'xp_',
            '--',
            '/*',
            '*/',
            'union',
            'information_schema',
            'sqlite_master'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in query_lower:
                return False
        
        return True


# Global database client instance
_db_client = None

def get_database_client() -> DatabaseClient:
    """Get or create the global database client."""
    global _db_client
    if _db_client is None:
        _db_client = DatabaseClient()
    return _db_client


@tool(description="Create a new table in the local SQLite database")
def create_database_table(
    table_name: str,
    columns: List[Dict[str, str]],
    primary_key: str = "id"
) -> str:
    """
    Create a new table in the SQLite database with specified columns.
    
    Args:
        table_name: Name of the table to create
        columns: List of column definitions, each with 'name' and 'type' keys
        primary_key: Name of the primary key column (default: 'id')
    
    Returns:
        Success or error message
    """
    try:
        client = get_database_client()
        
        # Validate table name (alphanumeric and underscores only)
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
            return "Error: Table name must contain only letters, numbers, and underscores, and start with a letter or underscore"
        
        # Build CREATE TABLE SQL
        column_definitions = [f"{primary_key} INTEGER PRIMARY KEY AUTOINCREMENT"]
        
        for col in columns:
            col_name = col["name"]
            col_type = col["type"].upper()
            
            # Validate column name
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', col_name):
                return f"Error: Invalid column name '{col_name}'. Must contain only letters, numbers, and underscores"
            
            # Map common types to SQLite types
            type_mapping = {
                "TEXT": "TEXT",
                "STRING": "TEXT", 
                "VARCHAR": "TEXT",
                "INTEGER": "INTEGER",
                "INT": "INTEGER",
                "REAL": "REAL",
                "FLOAT": "REAL",
                "DOUBLE": "REAL",
                "BOOLEAN": "INTEGER",
                "BOOL": "INTEGER",
                "DATE": "TEXT",
                "DATETIME": "TEXT",
                "TIMESTAMP": "TEXT",
                "JSON": "TEXT",
                "BLOB": "BLOB"
            }
            
            sqlite_type = type_mapping.get(col_type, "TEXT")
            column_definitions.append(f"{col_name} {sqlite_type}")
        
        # Add created_at timestamp
        column_definitions.append("created_at TEXT DEFAULT CURRENT_TIMESTAMP")
        
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(column_definitions)}
        );
        """
        
        client.execute_update(create_sql)
        
        return json.dumps({
            "success": True,
            "message": f"Table '{table_name}' created successfully",
            "columns": [primary_key] + [col["name"] for col in columns] + ["created_at"],
            "sql": create_sql
        }, indent=2)
        
    except Exception as e:
        return f"Error creating table: {str(e)}"


@tool(description="Insert data into a database table")
def insert_database_data(
    table_name: str,
    data: List[Dict[str, Any]]
) -> str:
    """
    Insert data into a database table.
    
    Args:
        table_name: Name of the table to insert data into
        data: List of dictionaries with column names as keys and values as data
    
    Returns:
        Success or error message with count of inserted rows
    """
    try:
        client = get_database_client()
        
        if not data:
            return "Error: No data provided to insert"
        
        # Get column names from first data item
        columns = list(data[0].keys())
        
        # Build INSERT SQL
        placeholders = ', '.join(['?' for _ in columns])
        insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        
        # Prepare data for insertion
        insert_data = []
        for item in data:
            row_data = []
            for col in columns:
                value = item.get(col)
                # Convert None to NULL, convert other types to strings for SQLite
                if value is None:
                    row_data.append(None)
                elif isinstance(value, (dict, list)):
                    row_data.append(json.dumps(value))
                else:
                    row_data.append(str(value))
            insert_data.append(tuple(row_data))
        
        # Execute insertions
        with client.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_sql, insert_data)
            conn.commit()
            inserted_count = cursor.rowcount
        
        return json.dumps({
            "success": True,
            "message": f"Successfully inserted {inserted_count} rows into '{table_name}'",
            "count": inserted_count,
            "columns": columns
        }, indent=2)
        
    except Exception as e:
        return f"Error inserting data: {str(e)}"


@tool(description="Query data from a database table")
def query_database(
    query: str,
    limit: int = 100
) -> str:
    """
    Execute a SELECT query on the database.
    
    Args:
        query: SQL SELECT query to execute
        limit: Maximum number of results to return (default: 100)
    
    Returns:
        JSON string with query results or error message
    """
    try:
        client = get_database_client()
        
        # Basic safety check
        if not client.is_safe_query(query):
            return "Error: Query contains potentially dangerous operations. Only SELECT, INSERT, UPDATE, DELETE, and CREATE operations are allowed."
        
        # Add LIMIT if not present and query is a SELECT
        if query.strip().upper().startswith('SELECT') and 'LIMIT' not in query.upper():
            query = f"{query.rstrip(';')} LIMIT {limit}"
        
        results = client.execute_query(query)
        
        return json.dumps({
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        }, indent=2)
        
    except Exception as e:
        return f"Error executing query: {str(e)}"


@tool(description="List all tables in the database")
def list_database_tables() -> str:
    """
    List all tables in the SQLite database.
    
    Returns:
        JSON string with list of table names and basic info
    """
    try:
        client = get_database_client()
        
        # Query SQLite system tables
        tables_query = """
        SELECT name, sql 
        FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
        """
        
        results = client.execute_query(tables_query)
        
        table_info = []
        for table in results:
            table_info.append({
                "name": table["name"],
                "has_schema": bool(table["sql"])
            })
        
        return json.dumps({
            "success": True,
            "tables": table_info,
            "count": len(table_info)
        }, indent=2)
        
    except Exception as e:
        return f"Error listing tables: {str(e)}"


@tool(description="Get schema information for a specific table")
def get_table_schema(table_name: str) -> str:
    """
    Get detailed schema information for a table.
    
    Args:
        table_name: Name of the table to get schema for
    
    Returns:
        JSON string with table schema information
    """
    try:
        client = get_database_client()
        
        # Get column information
        schema_query = f"PRAGMA table_info({table_name})"
        columns = client.execute_query(schema_query)
        
        if not columns:
            return f"Error: Table '{table_name}' not found"
        
        # Get table creation SQL
        create_sql_query = f"""
        SELECT sql 
        FROM sqlite_master 
        WHERE type='table' AND name='{table_name}'
        """
        create_result = client.execute_query(create_sql_query)
        create_sql = create_result[0]["sql"] if create_result else None
        
        return json.dumps({
            "success": True,
            "table_name": table_name,
            "columns": columns,
            "create_sql": create_sql,
            "column_count": len(columns)
        }, indent=2)
        
    except Exception as e:
        return f"Error getting table schema: {str(e)}"


@tool(description="Execute arbitrary SQL with safety checks")
def execute_database_sql(
    sql: str,
    limit: int = 100
) -> str:
    """
    Execute arbitrary SQL with basic safety checks.
    
    Args:
        sql: SQL statement to execute
        limit: Maximum number of results for SELECT queries (default: 100)
    
    Returns:
        JSON string with execution results or error message
    """
    try:
        client = get_database_client()
        
        # Safety check
        if not client.is_safe_query(sql):
            return "Error: SQL contains potentially dangerous operations. Only basic CRUD operations are allowed."
        
        sql_upper = sql.strip().upper()
        
        if sql_upper.startswith('SELECT'):
            # It's a SELECT query
            if 'LIMIT' not in sql_upper:
                sql = f"{sql.rstrip(';')} LIMIT {limit}"
            results = client.execute_query(sql)
            return json.dumps({
                "success": True,
                "query_type": "SELECT",
                "sql": sql,
                "results": results,
                "count": len(results)
            }, indent=2)
        else:
            # It's an INSERT/UPDATE/DELETE/CREATE query
            affected_rows = client.execute_update(sql)
            return json.dumps({
                "success": True,
                "query_type": sql_upper.split()[0],
                "sql": sql,
                "affected_rows": affected_rows
            }, indent=2)
        
    except Exception as e:
        return f"Error executing SQL: {str(e)}"


@tool(description="Check database connection and get basic info")
def check_database_connection() -> str:
    """
    Check if the database is accessible and get basic information.
    
    Returns:
        Connection status and database info
    """
    try:
        client = get_database_client()
        
        # Test basic connection
        test_query = "SELECT 1 as test, datetime('now') as current_time"
        result = client.execute_query(test_query)
        
        # Get database file info
        db_path = client.db_path
        db_exists = os.path.exists(db_path)
        db_size = os.path.getsize(db_path) if db_exists else 0
        
        return json.dumps({
            "success": True,
            "message": "✅ Database connection successful",
            "database_path": db_path,
            "database_exists": db_exists,
            "database_size_bytes": db_size,
            "current_time": result[0]["current_time"] if result else None
        }, indent=2)
        
    except Exception as e:
        return f"❌ Database connection error: {str(e)}"
