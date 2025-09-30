"""
Tools module for Deep Agents.

This module contains various tool implementations that can be used
by agents in the Deep Agents framework.
"""

from .filesystem_tools import (
    write_todos,
    ls,
    read_file,
    write_file,
    edit_file,
)
from .research_tools import internet_search
from .coding_tools import (
    write_code,
    run_tests,
    debug_code,
    code_review,
    generate_documentation,
)
from .example_tools import (
    calculate_area,
    get_weather,
)
from .weaviate_tools import (
    create_weaviate_collection,
    add_documents_to_weaviate,
    search_similar_documents,
    hybrid_search_documents,
    get_weaviate_collection_info,
    list_weaviate_collections,
    check_weaviate_connection,
)
from .supabase_tools import (
    create_supabase_collection,
    add_documents_to_supabase,
    search_similar_supabase_documents,
    get_supabase_collection_info,
    list_supabase_collections,
    check_supabase_connection,
)
from .upload_tools import (
    process_uploaded_file,
    extract_text_content,
    parse_structured_data,
    create_upload_collection,
)

__all__ = [
    # Filesystem tools
    "write_todos",
    "ls", 
    "read_file",
    "write_file",
    "edit_file",
    # Research tools
    "internet_search",
    # Coding tools
    "write_code",
    "run_tests", 
    "debug_code",
    "code_review",
    "generate_documentation",
    # Example tools
    "calculate_area",
    "get_weather",
    # Weaviate tools
    "create_weaviate_collection",
    "add_documents_to_weaviate",
    "search_similar_documents",
    "hybrid_search_documents",
    "get_weaviate_collection_info",
    "list_weaviate_collections",
    "check_weaviate_connection",
    # Supabase tools
    "create_supabase_collection",
    "add_documents_to_supabase",
    "search_similar_supabase_documents",
    "get_supabase_collection_info",
    "list_supabase_collections",
    "check_supabase_connection",
    # Upload tools
    "process_uploaded_file",
    "extract_text_content",
    "parse_structured_data",
    "create_upload_collection",
]
