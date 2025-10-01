# n8n Agent Implementation Plan

## Overview
Create a specialized agent for managing, designing, and testing n8n workflows programmatically using the n8n API.

## Goals
- ✅ List and browse n8n workflows
- ✅ Design and plan workflow structures
- ✅ Edit and update workflows
- ✅ Execute workflows and test them
- ✅ View and interpret execution results
- ✅ Provide n8n expertise and best practices

## Components

### 1. n8n Tools (`src/tools/n8n_tools.py`)
- ✅ `list_workflows` - List all workflows from n8n cloud
- ✅ `get_workflow` - Get detailed workflow configuration
- ✅ `create_workflow` - Create a new workflow
- ✅ `update_workflow` - Update an existing workflow
- ✅ `delete_workflow` - Delete a workflow
- ✅ `activate_workflow` - Activate/deactivate a workflow
- ✅ `execute_workflow` - Manually execute a workflow
- ✅ `get_executions` - Get workflow execution history
- ✅ `get_execution_details` - Get detailed execution data
- ✅ `get_credentials` - List available credentials (for planning)

### 2. n8n Agent (`src/agents/n8n_agent.py`)
- Specialized agent with n8n domain knowledge
- Access to all n8n tools
- Ability to reason about workflow design
- Understanding of n8n best practices
- Can interpret execution results and debug issues

### 3. Integration
- ✅ Register tools in `src/tools/__init__.py`
- ✅ Update server configuration to support n8n agent
- ✅ Ensure .env has N8N_API_KEY configured

## Implementation Progress

### Phase 1: Research & Setup ✅
- ✅ Research n8n API documentation
- ✅ Understand API endpoints and authentication
- ✅ Set up environment variables

### Phase 2: Tool Development ✅
- ✅ Create n8n_tools.py with API wrapper functions
- ✅ Implement all CRUD operations for workflows
- ✅ Implement execution and testing capabilities
- ✅ Handle error cases and API responses
- ✅ Register tools in src/tools/__init__.py

### Phase 3: Agent Development ✅
- ✅ Create n8n_agent.py with specialized prompts
- ✅ Integrate tools with agent
- ✅ Add domain knowledge about n8n
- ✅ Register agent in src/agents/__init__.py
- ✅ Add agent to server/langgraph.json

### Phase 4: UI Integration ✅
- ✅ Add n8n_agent to AgentSwitcher component
- ✅ Add weaviate_agent to AgentSwitcher component
- ✅ Set n8n_agent as default agent
- ✅ Update agentThreadIds to include all agents

### Phase 5: Enhancements ✅
- ✅ Fixed `active` field read-only error in create_workflow
- ✅ Increased recursion limit from 25 to 100
- ✅ Added AI Agent workflow guidance to system prompt
- ✅ Set default model to gpt-4o-mini with "openai account" credentials
- ✅ Provided example AI Agent workflow structure
- ✅ **CRITICAL FIX**: Discovered correct AI model connection pattern
  - Node type: `@n8n/n8n-nodes-langchain.lmChatOpenAi` (not chatOpenAi)
  - Connection type: `"ai_languageModel"` (special connection, NOT "main")
  - Model parameter structure uses `__rl`, `mode`, `value` format
- ✅ Added clear instructions to NEVER auto-activate workflows
- ✅ Added guidance to test workflows manually in n8n UI
- ✅ Updated example to show correct ai_languageModel connection pattern

### Phase 6: Testing & Validation ⏳
- Test listing workflows
- Test workflow creation and updates
- Test execution and result interpretation
- Validate agent responses
- Test AI Agent workflow creation

## Technical Details

### n8n API Base URL
`https://leaflane.app.n8n.cloud/api/v1`

### Authentication
- Header: `X-N8N-API-KEY: {N8N_API_KEY}`

### Key API Endpoints
- GET `/workflows` - List workflows
- GET `/workflows/{id}` - Get workflow details
- POST `/workflows` - Create workflow
- PUT `/workflows/{id}` - Update workflow
- DELETE `/workflows/{id}` - Delete workflow
- POST `/workflows/{id}/activate` - Activate workflow
- POST `/workflows/{id}/execute` - Execute workflow
- GET `/executions` - List executions
- GET `/executions/{id}` - Get execution details
- GET `/credentials` - List credentials

## Notes
- n8n workflows are JSON-based with nodes and connections
- Each node has a type, parameters, and position
- Connections link nodes together
- Credentials are referenced by ID in nodes
- Executions contain full data flow through workflow

