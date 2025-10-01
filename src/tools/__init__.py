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
from .database_tools import (
    create_database_table,
    insert_database_data,
    query_database,
    list_database_tables,
    get_table_schema,
    execute_database_sql,
    check_database_connection,
)
from .prompt_tools import (
    create_prompt_template,
    get_prompt_template,
    list_prompt_templates,
    update_prompt_template,
    delete_prompt_template,
    search_prompt_templates,
    get_prompt_categories,
    use_prompt_template,
)
from .system_refinement_tools import (
    analyze_system_performance,
    research_agent_best_practices,
    generate_improved_system_prompt,
    save_system_prompt_override,
    get_system_prompt_override,
    list_system_prompt_overrides,
    remove_system_prompt_override,
)
from .evaluation_tools import (
    evaluate_agent_performance,
    should_trigger_system_refinement,
    add_evaluation_tasks_to_todos,
    schedule_evaluation_pause,
    monitor_system_health,
    get_performance_trends,
)
from .n8n_tools import (
    list_workflows,
    get_workflow,
    create_workflow,
    update_workflow,
    delete_workflow,
    activate_workflow,
    execute_workflow,
    get_executions,
    get_execution_details,
    get_credentials,
    search_node_types,
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
    # Database tools
    "create_database_table",
    "insert_database_data",
    "query_database",
    "list_database_tables",
    "get_table_schema",
    "execute_database_sql",
    "check_database_connection",
    # Prompt tools
    "create_prompt_template",
    "get_prompt_template",
    "list_prompt_templates",
    "update_prompt_template",
    "delete_prompt_template",
    "search_prompt_templates",
    "get_prompt_categories",
    "use_prompt_template",
    # System refinement tools
    "analyze_system_performance",
    "research_agent_best_practices",
    "generate_improved_system_prompt",
    "save_system_prompt_override",
    "get_system_prompt_override",
    "list_system_prompt_overrides",
    "remove_system_prompt_override",
    # Evaluation tools
    "evaluate_agent_performance",
    "should_trigger_system_refinement",
    "add_evaluation_tasks_to_todos",
    "schedule_evaluation_pause",
    "monitor_system_health",
    "get_performance_trends",
    # n8n tools
    "list_workflows",
    "get_workflow",
    "create_workflow",
    "update_workflow",
    "delete_workflow",
    "activate_workflow",
    "execute_workflow",
    "get_executions",
    "get_execution_details",
    "get_credentials",
    "search_node_types",
]
