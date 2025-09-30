# LangGraph Server UI Guide

Yes! The LangGraph server provides several UI interfaces for monitoring, debugging, and interacting with your agents.

## 🎨 Available UIs

### 1. LangGraph Studio (Primary UI)
**URL**: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

This is the main graphical interface for LangGraph that provides:
- **Agent Visualization**: See your agent's graph structure
- **Thread Management**: View and manage conversation threads
- **Real-time Monitoring**: Watch agent execution in real-time
- **Debugging Tools**: Step through agent execution
- **State Inspection**: View agent state at each step
- **Tool Execution**: Monitor tool calls and responses

### 2. API Documentation (Swagger UI)
**URL**: http://127.0.0.1:2024/docs

Interactive API documentation where you can:
- **Test API Endpoints**: Try out different API calls
- **View Request/Response Schemas**: Understand data structures
- **Authentication**: Test with different auth methods
- **Explore Available Agents**: See all registered agents

### 3. OpenAPI Specification
**URL**: http://127.0.0.1:2024/openapi.json

Raw OpenAPI specification for:
- **API Integration**: Use with other tools
- **Code Generation**: Generate client libraries
- **Documentation**: Reference for API structure

## 🚀 Accessing the UIs

### Method 1: Direct Links

**LangGraph Studio:**
```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

**API Documentation:**
```
http://127.0.0.1:2024/docs
```

### Method 2: From Server Logs

When you start the LangGraph server, it shows the available URLs:

```bash
cd /Users/jonathanferrell/deepAgent
langgraph dev --config server/langgraph.json --host 127.0.0.1 --port 2024 --no-browser
```

**Expected Output:**
```
Welcome to LangGraph
- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
```

## 🔧 LangGraph Studio Features

### Agent Management
- **View All Agents**: See all registered agents (simple_agent, research_agent, coding_agent)
- **Agent Details**: Inspect agent configuration and tools
- **Switch Between Agents**: Test different agents

### Thread Management
- **Create New Threads**: Start new conversations
- **View Thread History**: See past conversations
- **Thread State**: Inspect the current state of any thread
- **Resume Threads**: Continue existing conversations

### Real-time Monitoring
- **Live Execution**: Watch agents work in real-time
- **Step-by-step Debugging**: See each step of agent execution
- **Tool Calls**: Monitor when and how tools are called
- **Error Tracking**: See any errors or issues

### State Inspection
- **Current State**: View the current state of any thread
- **State History**: See how state changes over time
- **File System**: View virtual files created by agents
- **Todo Lists**: See agent planning and task management

## 🛠️ Using LangGraph Studio

### Step 1: Access Studio
1. Open your browser
2. Go to: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
3. You should see the LangGraph Studio interface

### Step 2: Select an Agent
1. Look for agent selection dropdown
2. Choose from: simple_agent, research_agent, or coding_agent
3. The interface will update to show that agent's capabilities

### Step 3: Start a Conversation
1. Click "New Thread" or similar button
2. Type a message to your agent
3. Watch the agent process your request in real-time

### Step 4: Monitor Execution
- **Graph View**: See the agent's decision flow
- **Tool Calls**: Watch tools being executed
- **State Changes**: See how the agent's state evolves
- **Sub-agents**: See when sub-agents are spawned

## 🔍 API Documentation Usage

### Testing Endpoints
1. Go to http://127.0.0.1:2024/docs
2. Expand any endpoint (e.g., `/threads`)
3. Click "Try it out"
4. Fill in parameters and click "Execute"

### Common Endpoints

**List Threads:**
```
GET /threads
```

**Create Thread:**
```
POST /threads
```

**Get Thread State:**
```
GET /threads/{thread_id}/state
```

**Stream Messages:**
```
POST /threads/{thread_id}/runs/stream
```

## 🆚 UI Comparison

| Feature | LangGraph Studio | Deep Agents UI | API Docs |
|---------|------------------|----------------|----------|
| **Purpose** | Agent debugging & monitoring | User interaction | API testing |
| **Agent Switching** | ✅ Yes | ✅ Yes | ❌ Manual |
| **Real-time Monitoring** | ✅ Yes | ✅ Yes | ❌ No |
| **Graph Visualization** | ✅ Yes | ❌ No | ❌ No |
| **State Inspection** | ✅ Yes | ✅ Yes | ❌ Manual |
| **User-friendly** | ✅ Yes | ✅ Yes | ⚠️ Technical |
| **Thread Management** | ✅ Yes | ✅ Yes | ✅ Yes |

## 🚀 Quick Start with Studio

1. **Start LangGraph Server:**
   ```bash
   cd /Users/jonathanferrell/deepAgent
   langgraph dev --config server/langgraph.json --host 127.0.0.1 --port 2024 --no-browser
   ```

2. **Open LangGraph Studio:**
   - Go to: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

3. **Select an Agent:**
   - Choose from the dropdown: simple_agent, research_agent, or coding_agent

4. **Start Testing:**
   - Create a new thread
   - Send a message
   - Watch the agent work!

## 🔧 Troubleshooting

### Studio Not Loading
- Ensure LangGraph server is running on port 2024
- Check that the URL includes the correct baseUrl parameter
- Try refreshing the page

### Agent Not Appearing
- Restart the LangGraph server after adding new agents
- Check that the agent is properly registered in server/langgraph.json
- Look at server logs for any errors

### Connection Issues
- Verify the server is accessible: `curl http://127.0.0.1:2024/health`
- Check firewall settings
- Ensure no other process is using port 2024

## 📊 Monitoring Your Agents

### Real-time Debugging
- Use Studio to watch agents execute step-by-step
- See exactly when and why tools are called
- Monitor sub-agent spawning and communication

### Performance Monitoring
- Track execution times
- Monitor memory usage
- Identify bottlenecks

### Error Tracking
- See detailed error messages
- Track failed tool calls
- Monitor agent recovery

## 🎯 Best Practices

1. **Use Studio for Development**: Debug and test agents during development
2. **Use Deep Agents UI for Users**: Provide the polished interface for end users
3. **Use API Docs for Integration**: Reference when building custom integrations
4. **Monitor in Production**: Use Studio to monitor agent performance

The LangGraph server provides powerful UI tools that complement the Deep Agents UI perfectly!
