"""
File upload and processing tools for Deep Agents.

This module contains tools for handling file uploads and data processing.
"""

import os
import json
import csv
import io
from typing import List, Dict, Any, Union, Optional
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langchain.tools.tool_node import InjectedState
from typing import Annotated


@tool(description="Process uploaded file content and extract structured data")
def process_uploaded_file(
    file_content: str,
    file_name: str,
    file_type: str = "text",
    collection_name: Optional[str] = None
) -> str:
    """
    Process uploaded file content and extract structured data for Weaviate storage.
    
    Args:
        file_content: The content of the uploaded file
        file_name: Name of the uploaded file
        file_type: Type of file (text, json, csv, markdown)
        collection_name: Optional collection name for the data
    
    Returns:
        JSON string with processed data or error message
    """
    try:
        processed_data = []
        
        if file_type.lower() == "json":
            # Process JSON file
            try:
                data = json.loads(file_content)
                if isinstance(data, list):
                    for item in data:
                        processed_item = {
                            "title": item.get("title", f"Item from {file_name}"),
                            "content": str(item.get("content", item.get("description", str(item)))),
                            "topic": item.get("topic", "General"),
                            "source": file_name,
                            "difficulty": item.get("difficulty", "Beginner"),
                            "tags": item.get("tags", [file_type])
                        }
                        processed_data.append(processed_item)
                else:
                    processed_data.append({
                        "title": data.get("title", f"Document from {file_name}"),
                        "content": str(data.get("content", data.get("description", str(data)))),
                        "topic": data.get("topic", "General"),
                        "source": file_name,
                        "difficulty": data.get("difficulty", "Beginner"),
                        "tags": data.get("tags", [file_type])
                    })
            except json.JSONDecodeError:
                return f"Error: Invalid JSON format in file {file_name}"
                
        elif file_type.lower() == "csv":
            # Process CSV file
            try:
                csv_reader = csv.DictReader(io.StringIO(file_content))
                for row in csv_reader:
                    processed_item = {
                        "title": row.get("title", f"Row from {file_name}"),
                        "content": str(row.get("content", row.get("description", str(row)))),
                        "topic": row.get("topic", "General"),
                        "source": file_name,
                        "difficulty": row.get("difficulty", "Beginner"),
                        "tags": row.get("tags", [file_type]).split(",") if row.get("tags") else [file_type]
                    }
                    processed_data.append(processed_item)
            except Exception as e:
                return f"Error processing CSV file {file_name}: {str(e)}"
                
        elif file_type.lower() == "markdown":
            # Process Markdown file
            lines = file_content.split('\n')
            current_section = {"title": "", "content": "", "topic": "General", "source": file_name, "difficulty": "Beginner", "tags": [file_type]}
            
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    # Save previous section if it has content
                    if current_section["content"].strip():
                        processed_data.append(current_section.copy())
                    
                    # Start new section
                    current_section = {
                        "title": line.lstrip('#').strip(),
                        "content": "",
                        "topic": "General",
                        "source": file_name,
                        "difficulty": "Beginner",
                        "tags": [file_type]
                    }
                else:
                    current_section["content"] += line + "\n"
            
            # Add the last section
            if current_section["content"].strip():
                processed_data.append(current_section)
                
        else:
            # Process as plain text
            # Split into paragraphs or sections
            paragraphs = [p.strip() for p in file_content.split('\n\n') if p.strip()]
            
            for i, paragraph in enumerate(paragraphs):
                if len(paragraph) > 50:  # Only include substantial paragraphs
                    processed_data.append({
                        "title": f"Section {i+1} from {file_name}",
                        "content": paragraph,
                        "topic": "General",
                        "source": file_name,
                        "difficulty": "Beginner",
                        "tags": [file_type]
                    })
        
        if not processed_data:
            return f"No processable content found in file {file_name}"
        
        return json.dumps(processed_data, indent=2)
        
    except Exception as e:
        return f"Error processing file {file_name}: {str(e)}"


@tool(description="Extract text content from various file formats")
def extract_text_content(
    file_content: str,
    file_name: str,
    file_type: str = "text"
) -> str:
    """
    Extract plain text content from various file formats.
    
    Args:
        file_content: The content of the file
        file_name: Name of the file
        file_type: Type of file (text, json, csv, markdown, html)
    
    Returns:
        Extracted text content or error message
    """
    try:
        if file_type.lower() == "json":
            data = json.loads(file_content)
            return json.dumps(data, indent=2)
        elif file_type.lower() == "csv":
            return file_content  # CSV is already text
        elif file_type.lower() == "markdown":
            return file_content  # Markdown is already text
        elif file_type.lower() == "html":
            # Simple HTML tag removal (basic implementation)
            import re
            clean_text = re.sub(r'<[^>]+>', '', file_content)
            return clean_text
        else:
            return file_content
            
    except Exception as e:
        return f"Error extracting text from {file_name}: {str(e)}"


@tool(description="Parse structured data and create Weaviate documents")
def parse_structured_data(
    data: str,
    data_format: str = "json",
    collection_name: str = "UploadedData"
) -> str:
    """
    Parse structured data and create documents for Weaviate storage.
    
    Args:
        data: The structured data to parse
        data_format: Format of the data (json, csv, xml)
        collection_name: Name of the target collection
    
    Returns:
        JSON string with parsed documents or error message
    """
    try:
        documents = []
        
        if data_format.lower() == "json":
            try:
                parsed_data = json.loads(data)
                if isinstance(parsed_data, list):
                    for item in parsed_data:
                        doc = {
                            "title": item.get("title", item.get("name", "Untitled")),
                            "content": str(item.get("content", item.get("description", str(item)))),
                            "topic": item.get("topic", item.get("category", "General")),
                            "source": collection_name,
                            "difficulty": item.get("difficulty", "Beginner"),
                            "tags": item.get("tags", [data_format])
                        }
                        documents.append(doc)
                else:
                    documents.append({
                        "title": parsed_data.get("title", "Document"),
                        "content": str(parsed_data.get("content", str(parsed_data))),
                        "topic": parsed_data.get("topic", "General"),
                        "source": collection_name,
                        "difficulty": parsed_data.get("difficulty", "Beginner"),
                        "tags": parsed_data.get("tags", [data_format])
                    })
            except json.JSONDecodeError:
                return f"Error: Invalid JSON format in data"
                
        elif data_format.lower() == "csv":
            try:
                csv_reader = csv.DictReader(io.StringIO(data))
                for row in csv_reader:
                    doc = {
                        "title": row.get("title", row.get("name", "Untitled")),
                        "content": str(row.get("content", row.get("description", str(row)))),
                        "topic": row.get("topic", row.get("category", "General")),
                        "source": collection_name,
                        "difficulty": row.get("difficulty", "Beginner"),
                        "tags": row.get("tags", [data_format]).split(",") if row.get("tags") else [data_format]
                    }
                    documents.append(doc)
            except Exception as e:
                return f"Error processing CSV data: {str(e)}"
        
        if not documents:
            return f"No documents created from {data_format} data"
        
        return json.dumps(documents, indent=2)
        
    except Exception as e:
        return f"Error parsing {data_format} data: {str(e)}"


@tool(description="Create a collection specifically for uploaded data")
def create_upload_collection(
    collection_name: str,
    description: str = "Collection for uploaded data"
) -> str:
    """
    Create a Weaviate collection specifically designed for uploaded data.
    
    Args:
        collection_name: Name of the collection to create
        description: Description of the collection
    
    Returns:
        Success message or error
    """
    try:
        from .weaviate_tools import create_weaviate_collection
        
        properties = [
            {"name": "title", "data_type": "text"},
            {"name": "content", "data_type": "text"},
            {"name": "topic", "data_type": "text"},
            {"name": "source", "data_type": "text"},
            {"name": "difficulty", "data_type": "text"},
            {"name": "tags", "data_type": "text"},
            {"name": "upload_date", "data_type": "text"},
            {"name": "file_type", "data_type": "text"}
        ]
        
        result = create_weaviate_collection.invoke({"collection_name": collection_name, "properties": properties})
        return f"Collection '{collection_name}' created successfully for uploaded data"
        
    except Exception as e:
        return f"Error creating upload collection: {str(e)}"
