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
