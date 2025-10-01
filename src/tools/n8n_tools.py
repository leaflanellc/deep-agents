"""
n8n workflow management tools for listing, creating, editing, executing, and testing workflows.
"""

import os
import requests
from typing import Dict, List, Optional, Any
import json

# Get n8n configuration from environment
N8N_API_KEY = os.getenv('N8N_API_KEY')
N8N_BASE_URL = os.getenv('N8N_BASE_URL', 'https://leaflane.app.n8n.cloud/api/v1')


def _get_headers() -> Dict[str, str]:
    """Get headers for n8n API requests."""
    if not N8N_API_KEY:
        raise ValueError("N8N_API_KEY not found in environment variables")
    return {
        'X-N8N-API-KEY': N8N_API_KEY,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def _handle_response(response: requests.Response) -> Dict[str, Any]:
    """Handle API response and errors."""
    try:
        response.raise_for_status()
        return response.json() if response.content else {}
    except requests.exceptions.HTTPError as e:
        error_detail = ""
        try:
            error_detail = response.json()
        except:
            error_detail = response.text
        raise Exception(f"n8n API Error: {response.status_code} - {error_detail}")
    except Exception as e:
        raise Exception(f"Error processing n8n API response: {str(e)}")


def list_workflows(active: Optional[bool] = None, tags: Optional[List[str]] = None) -> str:
    """
    List all workflows from n8n cloud.
    
    Args:
        active: If True, only return active workflows. If False, only inactive. If None, return all.
        tags: Optional list of tag names to filter workflows by.
    
    Returns:
        JSON string containing list of workflows with their id, name, active status, and tags.
    """
    try:
        url = f"{N8N_BASE_URL}/workflows"
        params = {}
        if active is not None:
            params['active'] = str(active).lower()
        if tags:
            params['tags'] = ','.join(tags)
            
        response = requests.get(url, headers=_get_headers(), params=params)
        data = _handle_response(response)
        
        # Format the output to be more readable
        workflows = data.get('data', []) if isinstance(data, dict) else data
        summary = []
        for wf in workflows:
            summary.append({
                'id': wf.get('id'),
                'name': wf.get('name'),
                'active': wf.get('active'),
                'tags': wf.get('tags', []),
                'createdAt': wf.get('createdAt'),
                'updatedAt': wf.get('updatedAt'),
                'nodes': len(wf.get('nodes', [])) if 'nodes' in wf else 'N/A'
            })
        
        return json.dumps(summary, indent=2)
    except Exception as e:
        return f"Error listing workflows: {str(e)}"


def get_workflow(workflow_id: str) -> str:
    """
    Get detailed information about a specific workflow including its nodes and connections.
    
    Args:
        workflow_id: The ID of the workflow to retrieve.
    
    Returns:
        JSON string containing the complete workflow definition.
    """
    try:
        url = f"{N8N_BASE_URL}/workflows/{workflow_id}"
        response = requests.get(url, headers=_get_headers())
        data = _handle_response(response)
        
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error getting workflow {workflow_id}: {str(e)}"


def create_workflow(name: str, nodes: List[Dict], connections: Dict, settings: Optional[Dict] = None, 
                   active: bool = False, tags: Optional[List[str]] = None) -> str:
    """
    Create a new workflow in n8n.
    
    Args:
        name: Name of the workflow.
        nodes: List of node definitions. Each node should have: name, type, parameters, position.
        connections: Dictionary defining connections between nodes.
        settings: Optional workflow settings (timezone, saveExecutionProgress, etc).
        active: Whether to activate the workflow immediately.
        tags: Optional list of tag names to assign to the workflow.
    
    Returns:
        JSON string containing the created workflow details including its ID.
    """
    try:
        url = f"{N8N_BASE_URL}/workflows"
        
        workflow_data = {
            'name': name,
            'nodes': nodes,
            'connections': connections,
            'active': active,
            'settings': settings or {},
        }
        
        if tags:
            workflow_data['tags'] = tags
        
        response = requests.post(url, headers=_get_headers(), json=workflow_data)
        data = _handle_response(response)
        
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error creating workflow: {str(e)}"


def update_workflow(workflow_id: str, name: Optional[str] = None, nodes: Optional[List[Dict]] = None,
                   connections: Optional[Dict] = None, settings: Optional[Dict] = None,
                   active: Optional[bool] = None, tags: Optional[List[str]] = None) -> str:
    """
    Update an existing workflow. Only provided fields will be updated.
    
    Args:
        workflow_id: The ID of the workflow to update.
        name: New name for the workflow.
        nodes: Updated list of node definitions.
        connections: Updated connections dictionary.
        settings: Updated workflow settings.
        active: Whether the workflow should be active.
        tags: Updated list of tag names.
    
    Returns:
        JSON string containing the updated workflow details.
    """
    try:
        # First get the current workflow
        current_workflow = json.loads(get_workflow(workflow_id))
        
        # Build update data
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if nodes is not None:
            update_data['nodes'] = nodes
        if connections is not None:
            update_data['connections'] = connections
        if settings is not None:
            update_data['settings'] = settings
        if active is not None:
            update_data['active'] = active
        if tags is not None:
            update_data['tags'] = tags
        
        # Merge with current data to ensure all required fields are present
        workflow_data = {
            'name': update_data.get('name', current_workflow.get('name')),
            'nodes': update_data.get('nodes', current_workflow.get('nodes')),
            'connections': update_data.get('connections', current_workflow.get('connections')),
            'settings': update_data.get('settings', current_workflow.get('settings', {})),
            'active': update_data.get('active', current_workflow.get('active', False)),
        }
        
        if 'tags' in update_data or 'tags' in current_workflow:
            workflow_data['tags'] = update_data.get('tags', current_workflow.get('tags', []))
        
        url = f"{N8N_BASE_URL}/workflows/{workflow_id}"
        response = requests.put(url, headers=_get_headers(), json=workflow_data)
        data = _handle_response(response)
        
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error updating workflow {workflow_id}: {str(e)}"


def delete_workflow(workflow_id: str) -> str:
    """
    Delete a workflow from n8n.
    
    Args:
        workflow_id: The ID of the workflow to delete.
    
    Returns:
        Success message or error.
    """
    try:
        url = f"{N8N_BASE_URL}/workflows/{workflow_id}"
        response = requests.delete(url, headers=_get_headers())
        _handle_response(response)
        
        return f"Successfully deleted workflow {workflow_id}"
    except Exception as e:
        return f"Error deleting workflow {workflow_id}: {str(e)}"


def activate_workflow(workflow_id: str, active: bool = True) -> str:
    """
    Activate or deactivate a workflow.
    
    Args:
        workflow_id: The ID of the workflow.
        active: True to activate, False to deactivate.
    
    Returns:
        JSON string with updated workflow status.
    """
    try:
        # Use the update endpoint to change active status
        return update_workflow(workflow_id, active=active)
    except Exception as e:
        return f"Error {'activating' if active else 'deactivating'} workflow {workflow_id}: {str(e)}"


def execute_workflow(workflow_id: str, data: Optional[Dict] = None) -> str:
    """
    Manually execute a workflow.
    
    Args:
        workflow_id: The ID of the workflow to execute.
        data: Optional input data to pass to the workflow.
    
    Returns:
        JSON string containing execution information including execution ID.
    """
    try:
        url = f"{N8N_BASE_URL}/workflows/{workflow_id}/execute"
        payload = {}
        if data:
            payload['data'] = data
            
        response = requests.post(url, headers=_get_headers(), json=payload)
        result = _handle_response(response)
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error executing workflow {workflow_id}: {str(e)}"


def get_executions(workflow_id: Optional[str] = None, status: Optional[str] = None, 
                  limit: int = 20) -> str:
    """
    Get workflow execution history.
    
    Args:
        workflow_id: Optional workflow ID to filter executions.
        status: Optional status filter ('success', 'error', 'waiting', 'running').
        limit: Maximum number of executions to return (default 20, max 250).
    
    Returns:
        JSON string containing list of executions with their status, start time, and basic info.
    """
    try:
        url = f"{N8N_BASE_URL}/executions"
        params = {'limit': min(limit, 250)}
        
        if workflow_id:
            params['workflowId'] = workflow_id
        if status:
            params['status'] = status
            
        response = requests.get(url, headers=_get_headers(), params=params)
        data = _handle_response(response)
        
        # Format the output
        executions = data.get('data', []) if isinstance(data, dict) else data
        summary = []
        for exe in executions:
            summary.append({
                'id': exe.get('id'),
                'workflowId': exe.get('workflowId'),
                'workflowName': exe.get('workflowData', {}).get('name', 'N/A'),
                'status': exe.get('status') or exe.get('finished') and 'success' or 'error',
                'startedAt': exe.get('startedAt'),
                'stoppedAt': exe.get('stoppedAt'),
                'mode': exe.get('mode')
            })
        
        return json.dumps(summary, indent=2)
    except Exception as e:
        return f"Error getting executions: {str(e)}"


def get_execution_details(execution_id: str) -> str:
    """
    Get detailed information about a specific execution including all node data.
    
    Args:
        execution_id: The ID of the execution to retrieve.
    
    Returns:
        JSON string containing complete execution details including data from each node.
    """
    try:
        url = f"{N8N_BASE_URL}/executions/{execution_id}"
        response = requests.get(url, headers=_get_headers())
        data = _handle_response(response)
        
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error getting execution details for {execution_id}: {str(e)}"


def get_credentials() -> str:
    """
    List available credentials (for planning workflows that need authentication).
    Note: This returns credential metadata only, not actual credential values.
    
    Returns:
        JSON string containing list of available credentials with their types and names.
    """
    try:
        url = f"{N8N_BASE_URL}/credentials"
        response = requests.get(url, headers=_get_headers())
        data = _handle_response(response)
        
        # Format the output
        credentials = data.get('data', []) if isinstance(data, dict) else data
        summary = []
        for cred in credentials:
            summary.append({
                'id': cred.get('id'),
                'name': cred.get('name'),
                'type': cred.get('type'),
                'createdAt': cred.get('createdAt'),
                'updatedAt': cred.get('updatedAt')
            })
        
        return json.dumps(summary, indent=2)
    except Exception as e:
        return f"Error getting credentials: {str(e)}"


def search_node_types(query: str) -> str:
    """
    Search for available n8n node types to use in workflows.
    This helps when planning/designing workflows to know what nodes are available.
    
    Args:
        query: Search term (e.g., 'slack', 'http', 'database', 'ai').
    
    Returns:
        Information about common node types matching the query.
    """
    # Common n8n node types organized by category
    node_types = {
        'trigger': [
            'n8n-nodes-base.webhook', 'n8n-nodes-base.scheduleTrigger',
            'n8n-nodes-base.emailReadImap', 'n8n-nodes-base.manualTrigger'
        ],
        'data': [
            'n8n-nodes-base.httpRequest', 'n8n-nodes-base.postgres',
            'n8n-nodes-base.mysql', 'n8n-nodes-base.mongodb',
            'n8n-nodes-base.redis', 'n8n-nodes-base.googleSheets'
        ],
        'logic': [
            'n8n-nodes-base.if', 'n8n-nodes-base.switch',
            'n8n-nodes-base.merge', 'n8n-nodes-base.splitInBatches',
            'n8n-nodes-base.code', 'n8n-nodes-base.set'
        ],
        'communication': [
            'n8n-nodes-base.slack', 'n8n-nodes-base.email',
            'n8n-nodes-base.discord', 'n8n-nodes-base.telegram'
        ],
        'ai': [
            'n8n-nodes-base.openAi', '@n8n/n8n-nodes-langchain.agent',
            '@n8n/n8n-nodes-langchain.chatOpenAi', '@n8n/n8n-nodes-langchain.chainLlm'
        ],
        'transformation': [
            'n8n-nodes-base.itemLists', 'n8n-nodes-base.aggregate',
            'n8n-nodes-base.removeDuplicates', 'n8n-nodes-base.sort'
        ]
    }
    
    query_lower = query.lower()
    results = []
    
    # Search in node types
    for category, nodes in node_types.items():
        for node in nodes:
            if query_lower in node.lower() or query_lower in category.lower():
                results.append({
                    'category': category,
                    'type': node,
                    'name': node.split('.')[-1]
                })
    
    if not results:
        results.append({
            'message': f"No exact matches found for '{query}'",
            'suggestion': "Try searching for: trigger, http, database, ai, slack, webhook, code, etc."
        })
    
    return json.dumps(results, indent=2)


# Export all tools
__all__ = [
    'list_workflows',
    'get_workflow',
    'create_workflow',
    'update_workflow',
    'delete_workflow',
    'activate_workflow',
    'execute_workflow',
    'get_executions',
    'get_execution_details',
    'get_credentials',
    'search_node_types'
]

