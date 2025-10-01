# Deep Agents Quick Reference

## 🚀 Quick Start

```bash
# Start everything
./server/start_all.sh

# Stop everything
./server/stop_all.sh
```

## 🔧 Manual Commands

### Start LangGraph Server
```bash
cd /Users/jonathanferrell/deepAgent
langgraph dev --config server/langgraph.json --host 127.0.0.1 --port 2024 --no-browser
```

### Start UI
```bash
cd /Users/jonathanferrell/deepAgent/ui
npm run dev
```

## 🌐 Access Points

- **UI**: http://localhost:3000
- **API**: http://127.0.0.1:2024
- **API Docs**: http://127.0.0.1:2024/docs

## 🛑 Stop Commands

```bash
# Stop by port
lsof -ti:2024 | xargs kill -9  # LangGraph
lsof -ti:3000 | xargs kill -9  # UI

# Stop by process
pkill -f "langgraph dev"
pkill -f "npm run dev"
```

## 🔍 Health Checks

```bash
# Check servers
curl http://127.0.0.1:2024/health
curl http://localhost:3000

# Check agents
curl http://127.0.0.1:2024/assistants
```

## 📁 Key Files

- `.env` - API keys configuration
- `server/langgraph.json` - Server configuration
- `ui/.env.local` - UI configuration
- `server/start_all.sh` - Start everything script
- `server/stop_all.sh` - Stop everything script

## 🤖 Available Agents

- **simple_agent** - General purpose agent
- **research_agent** - Research and information gathering
- **coding_agent** - Code generation and debugging
- **weaviate_agent** - Weaviate vector database management
- **n8n_agent** - n8n workflow automation management

## 🔑 Required Environment Variables

### Core
- `ANTHROPIC_API_KEY` - Required for all agents
- `TAVILY_API_KEY` - Required for research agent

### Databases
- `WEAVIATE_URL` - Weaviate cloud URL
- `WEAVIATE_API_KEY` - Weaviate API key
- `OPENAI_API_KEY` - Required for embeddings

### n8n Integration
- `N8N_API_KEY` - n8n API key (required for n8n agent)
- `N8N_BASE_URL` - n8n instance URL (default: https://leaflane.app.n8n.cloud/api/v1)
