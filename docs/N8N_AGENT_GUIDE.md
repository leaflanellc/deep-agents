# n8n Agent Guide

## Overview

The n8n Agent is a specialized agent designed to help you manage, design, test, and optimize n8n workflows programmatically. It has deep understanding of n8n's architecture, node types, and best practices for workflow automation.

## Features

### Core Capabilities
- 📋 **List & Browse**: View all workflows with their status, tags, and metadata
- 🔍 **Inspect**: Get detailed workflow configurations including nodes and connections
- ✨ **Create**: Design and create new workflows from scratch
- ✏️ **Edit**: Update existing workflows with new nodes or logic
- 🗑️ **Delete**: Remove workflows that are no longer needed
- ▶️ **Execute**: Manually trigger workflow executions for testing
- 📊 **Monitor**: View execution history and results
- 🐛 **Debug**: Analyze execution data to troubleshoot issues
- 💡 **Advise**: Provide n8n best practices and design guidance

### n8n Expertise
The agent has built-in knowledge of:
- 300+ n8n node types and integrations
- Workflow design patterns and best practices
- Error handling and reliability strategies
- Data transformation and logic patterns
- API integration techniques
- AI/LangChain workflow capabilities
- Trigger types and use cases

## Setup

### 1. Environment Configuration

Add the following to your `.env` file:

```bash
# n8n Configuration
N8N_API_KEY=your_n8n_api_key_here
N8N_BASE_URL=https://leaflane.app.n8n.cloud/api/v1  # Optional, defaults to this
```

### 2. Get Your API Key

1. Log into your n8n Cloud instance at https://leaflane.app.n8n.cloud/
2. Go to Settings → API
3. Create a new API key
4. Copy the key to your `.env` file

For more details: https://docs.n8n.io/api/authentication/

### 3. Verify Setup

Run the example script to verify everything is configured:

```bash
python examples/n8n_agent_example.py
```

## Usage

### Using the n8n Agent in Code

```python
import asyncio
from src.agents.n8n_agent import create_n8n_agent
from langchain_core.messages import HumanMessage

async def main():
    agent = create_n8n_agent()
    
    result = await agent.ainvoke({
        "messages": [
            HumanMessage(content="List all my workflows")
        ]
    })
    
    print(result['messages'][-1].content)

asyncio.run(main())
```

### Using via LangGraph UI

1. Start the LangGraph server:
   ```bash
   cd server
   ./start_all.sh
   ```

2. Open the UI at http://localhost:3000

3. Select "n8n_agent" from the agent dropdown

4. Start chatting with the agent!

## Common Use Cases

### 1. List All Workflows

```
"Show me all my workflows and their current status"
```

The agent will list all workflows with details like:
- Workflow ID and name
- Active/inactive status
- Number of nodes
- Tags
- Last updated time

### 2. Inspect a Workflow

```
"Get the details of workflow ID 123 and explain what it does"
```

The agent will:
- Retrieve the complete workflow definition
- Explain the purpose and logic
- Describe each node and its role
- Show how nodes are connected

### 3. Design a New Workflow

```
"I need a workflow that monitors my email, extracts attachments, 
and saves them to Google Drive. Can you help me design this?"
```

The agent will:
- Suggest appropriate trigger nodes (Email Trigger)
- Recommend processing nodes
- Identify required credentials
- Provide node configuration examples
- Offer best practices

### 4. Create a Workflow

```
"Create a simple workflow that:
1. Triggers on a webhook
2. Logs the data to console
3. Responds with a success message"
```

The agent will:
- Construct the workflow JSON structure
- Create appropriate nodes with correct types
- Set up connections between nodes
- Configure parameters
- Create the workflow via API
- Return the new workflow ID

### 5. Test a Workflow

```
"Execute workflow ID 456 with test data and show me the results"
```

The agent will:
- Trigger the workflow execution
- Monitor the execution
- Retrieve execution details
- Show data flow through each node
- Identify any errors or issues

### 6. Debug Execution Issues

```
"My workflow ID 789 failed. Can you check the recent executions 
and tell me what went wrong?"
```

The agent will:
- Get recent execution history
- Find failed executions
- Examine error messages
- Analyze data at failure points
- Suggest fixes or improvements

### 7. Update a Workflow

```
"Add an IF condition to workflow 123 that checks if the email 
subject contains 'urgent' before proceeding"
```

The agent will:
- Get current workflow structure
- Add new IF node
- Configure the condition
- Update connections appropriately
- Update the workflow via API

### 8. Search for Node Types

```
"What nodes can I use to work with databases?"
```

The agent will list relevant nodes like:
- Postgres
- MySQL
- MongoDB
- Redis
- Supabase
And explain their capabilities

## Available Tools

The n8n agent has access to these tools:

### Workflow Management
- `list_workflows` - List all workflows (with filters)
- `get_workflow` - Get complete workflow details
- `create_workflow` - Create a new workflow
- `update_workflow` - Update existing workflow
- `delete_workflow` - Delete a workflow
- `activate_workflow` - Activate/deactivate workflows

### Execution & Testing
- `execute_workflow` - Manually execute a workflow
- `get_executions` - Get execution history
- `get_execution_details` - Get detailed execution data

### Planning & Research
- `get_credentials` - List available credentials
- `search_node_types` - Find suitable node types

## n8n Workflow Structure

### Workflow JSON Format

```json
{
  "name": "My Workflow",
  "active": true,
  "nodes": [
    {
      "name": "When clicking 'Test workflow'",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 300],
      "parameters": {}
    },
    {
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300],
      "parameters": {
        "method": "GET",
        "url": "https://api.example.com/data"
      }
    }
  ],
  "connections": {
    "When clicking 'Test workflow'": {
      "main": [[
        {
          "node": "HTTP Request",
          "type": "main",
          "index": 0
        }
      ]]
    }
  },
  "settings": {}
}
```

### Node Positioning

Nodes are positioned on a canvas:
- X-axis: horizontal position (typically in multiples of 200)
- Y-axis: vertical position (typically in multiples of 100)
- Standard spacing: 200 pixels between nodes

### Connections

Connections define data flow:
- `main`: Standard data flow
- `main[0]`: First output (most nodes have one output)
- `main[1]`: Second output (IF nodes, Switch nodes)

## Best Practices

### Workflow Design
1. **Start Simple**: Begin with basic trigger → action patterns
2. **Modular Design**: Break complex workflows into smaller, reusable pieces
3. **Clear Naming**: Use descriptive node names that explain purpose
4. **Error Handling**: Add error workflows for production systems
5. **Test Thoroughly**: Always test with sample data before activating

### Performance
1. **Batch Processing**: Use Split in Batches for large datasets
2. **Efficient Queries**: Optimize database queries and API calls
3. **Conditional Logic**: Skip unnecessary processing with IF nodes
4. **Wait Nodes**: Add waits for rate-limited APIs

### Maintenance
1. **Documentation**: Use Sticky Notes to document complex logic
2. **Version Control**: Export workflows regularly as backup
3. **Monitoring**: Check execution history regularly
4. **Credentials**: Keep credentials updated and secure

### Security
1. **API Keys**: Never hardcode credentials in parameters
2. **Webhook URLs**: Keep webhook URLs private
3. **Data Validation**: Validate input data from external sources
4. **Access Control**: Use n8n's role-based permissions

## Common Node Types

### Triggers
- **Manual Trigger**: Test workflows manually
- **Webhook**: HTTP endpoint trigger
- **Schedule Trigger**: Time-based automation
- **Email Trigger**: Monitor email inbox

### Data Processing
- **HTTP Request**: Call external APIs
- **Code**: Custom JavaScript/Python logic
- **Set**: Transform and structure data
- **Item Lists**: Work with arrays

### Logic & Control
- **IF**: Conditional branching
- **Switch**: Multiple conditions
- **Merge**: Combine multiple flows
- **Split in Batches**: Process large datasets

### AI & LangChain
- **OpenAI**: AI text generation
- **AI Agent**: Autonomous AI agents
- **Chat Model**: Conversational AI
- **Vector Store**: Semantic search

### Communication
- **Slack**: Send Slack messages
- **Email**: Send emails
- **Discord**: Discord integration
- **Telegram**: Telegram bot

### Databases
- **Postgres**: PostgreSQL operations
- **MySQL**: MySQL operations
- **MongoDB**: MongoDB operations
- **Google Sheets**: Spreadsheet operations

## Examples

### Example 1: Simple Webhook to Slack

```python
workflow = {
    "name": "Webhook to Slack",
    "nodes": [
        {
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "position": [250, 300],
            "parameters": {
                "path": "incoming",
                "responseMode": "responseNode"
            }
        },
        {
            "name": "Slack",
            "type": "n8n-nodes-base.slack",
            "position": [450, 300],
            "parameters": {
                "channel": "#general",
                "text": "={{ $json.message }}"
            },
            "credentials": {
                "slackApi": {"id": "1", "name": "Slack account"}
            }
        },
        {
            "name": "Respond",
            "type": "n8n-nodes-base.respondToWebhook",
            "position": [650, 300],
            "parameters": {
                "respondWith": "json",
                "responseBody": "{\"status\": \"success\"}"
            }
        }
    ],
    "connections": {
        "Webhook": {"main": [[{"node": "Slack", "type": "main", "index": 0}]]},
        "Slack": {"main": [[{"node": "Respond", "type": "main", "index": 0}]]}
    }
}
```

### Example 2: Scheduled Data Processing

The agent can help you create scheduled workflows that:
- Run on a cron schedule
- Fetch data from APIs
- Transform the data
- Store in databases or send notifications

### Example 3: AI-Powered Workflows

Use AI nodes to create intelligent automation:
- Sentiment analysis on customer feedback
- Automated content generation
- Smart routing based on AI decisions
- RAG (Retrieval Augmented Generation) pipelines

## Troubleshooting

### API Connection Issues

**Problem**: "N8N_API_KEY not found in environment variables"

**Solution**: 
1. Check `.env` file exists in project root
2. Verify `N8N_API_KEY` is set
3. Restart the server after updating `.env`

### Authentication Errors

**Problem**: "401 Unauthorized"

**Solution**:
1. Verify your API key is valid
2. Check if API key has expired
3. Regenerate API key in n8n settings

### Workflow Execution Fails

**Problem**: Workflow executes but fails at a specific node

**Solution**:
1. Ask agent to get execution details
2. Review error messages from failed node
3. Check node parameters and credentials
4. Test external APIs independently

### Can't Find Workflows

**Problem**: Agent returns empty workflow list

**Solution**:
1. Verify API key has correct permissions
2. Check if workflows exist in your n8n instance
3. Try listing workflows with different filters

## Tips & Tricks

### 1. Use the Agent for Learning
Ask questions like:
- "How do I implement error handling in n8n?"
- "What's the best way to process large datasets?"
- "Show me examples of AI agent workflows"

### 2. Iterative Development
1. Start with agent designing the workflow
2. Create a basic version
3. Test it
4. Ask agent to refine and improve

### 3. Code Generation
The agent can generate:
- JavaScript code for Code nodes
- JSON schemas for data validation
- Regular expressions for text processing
- API request configurations

### 4. Workflow Templates
Ask the agent to create templates for:
- Data synchronization
- Notification systems
- Form processing
- Report generation
- Social media automation

## Additional Resources

- **n8n Documentation**: https://docs.n8n.io/
- **n8n API Docs**: https://docs.n8n.io/api/
- **n8n Community**: https://community.n8n.io/
- **Node Library**: https://n8n.io/integrations/
- **n8n Workflows**: https://n8n.io/workflows/ (community templates)

## Support

If you encounter issues:
1. Check the error messages from the agent
2. Review n8n logs in your instance
3. Verify API credentials and permissions
4. Check n8n service status
5. Refer to n8n documentation

The n8n agent is designed to be your workflow automation expert - don't hesitate to ask it for help, explanations, or best practices!

