# Deep Agents Startup Guide

This guide shows how to start and stop all components of the Deep Agents system.

## 🏗️ System Architecture

The Deep Agents system consists of three main components:

1. **LangGraph Server** - Backend API server running on port 2024
2. **Deep Agents UI** - Frontend web interface running on port 3000
3. **Environment Configuration** - API keys and settings

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Python 3.12+ installed
- ✅ Node.js 18+ installed
- ✅ Valid Anthropic API key
- ✅ All dependencies installed (see setup steps below)

## 🚀 Starting All Components

### Step 1: Update API Keys

First, update your `.env` file with your actual API keys:

```bash
# Edit the .env file
nano .env

# Replace the placeholder values:
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
TAVILY_API_KEY=tvly-your-actual-key-here  # Optional, for research agent
```

### Step 2: Start LangGraph Server

Open a terminal and start the LangGraph server:

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

### Step 3: Start Deep Agents UI

Open a **second terminal** and start the UI:

```bash
cd /Users/jonathanferrell/deepAgent/ui
npm run dev
```

**Expected Output:**
```
- Local:        http://localhost:3000
- Network:      http://192.168.x.x:3000
```

### Step 4: Access the System

- **Main UI**: http://localhost:3000
- **API Documentation**: http://127.0.0.1:2024/docs
- **LangGraph Studio**: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

## 🛑 Stopping All Components

### Method 1: Graceful Shutdown

**Stop UI Server:**
- In the UI terminal, press `Ctrl+C`
- Wait for the process to stop

**Stop LangGraph Server:**
- In the LangGraph terminal, press `Ctrl+C`
- Wait for the process to stop

### Method 2: Force Kill (if needed)

If processes don't stop gracefully:

```bash
# Find and kill LangGraph server
ps aux | grep langgraph
kill -9 <process_id>

# Find and kill Node.js processes
ps aux | grep node
kill -9 <process_id>

# Or kill all processes on specific ports
lsof -ti:2024 | xargs kill -9  # LangGraph server
lsof -ti:3000 | xargs kill -9  # UI server
```

## 🔧 Quick Start Scripts

### Start Everything (Bash Script)

Create `start_all.sh`:

```bash
#!/bin/bash
echo "🚀 Starting Deep Agents System..."

# Start LangGraph server in background
echo "Starting LangGraph server..."
cd /Users/jonathanferrell/deepAgent
langgraph dev --config server/langgraph.json --host 127.0.0.1 --port 2024 --no-browser &
LANGGRAPH_PID=$!

# Wait for server to start
sleep 5

# Start UI server
echo "Starting Deep Agents UI..."
cd /Users/jonathanferrell/deepAgent/ui
npm run dev &
UI_PID=$!

echo "✅ System started!"
echo "🌐 UI: http://localhost:3000"
echo "🔧 API: http://127.0.0.1:2024"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo 'Stopping services...'; kill $LANGGRAPH_PID $UI_PID; exit" INT
wait
```

Make it executable and run:
```bash
chmod +x start_all.sh
./server/start_all.sh
```

### Stop Everything (Bash Script)

Create `stop_all.sh`:

```bash
#!/bin/bash
echo "🛑 Stopping Deep Agents System..."

# Kill processes on specific ports
lsof -ti:2024 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Kill any remaining langgraph processes
pkill -f "langgraph dev" 2>/dev/null

# Kill any remaining node processes (be careful with this)
pkill -f "npm run dev" 2>/dev/null

echo "✅ All services stopped"
```

Make it executable and run:
```bash
chmod +x stop_all.sh
./server/stop_all.sh
```

## 🔍 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using the ports
lsof -i:2024
lsof -i:3000

# Kill processes using those ports
lsof -ti:2024 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

**2. API Key Not Working**
- Verify your API key is correct in `.env`
- Restart the LangGraph server after changing API keys
- Check the server logs for authentication errors

**3. UI Not Connecting to Server**
- Ensure LangGraph server is running on port 2024
- Check `.env.local` in the UI directory has correct settings
- Verify no firewall is blocking localhost connections

**4. Dependencies Missing**
```bash
# Reinstall Python dependencies
cd /Users/jonathanferrell/deepAgent
pip install -e .

# Reinstall Node.js dependencies
cd /Users/jonathanferrell/deepAgent/ui
npm install
```

### Health Checks

**Check LangGraph Server:**
```bash
curl http://127.0.0.1:2024/health
```

**Check UI Server:**
```bash
curl http://localhost:3000
```

**Check Available Agents:**
```bash
curl http://127.0.0.1:2024/assistants
```

## 📊 Monitoring

### View Logs

**LangGraph Server Logs:**
- Logs appear in the terminal where you started the server
- Look for errors, warnings, and request information

**UI Server Logs:**
- Logs appear in the terminal where you started the UI
- Look for compilation errors and build issues

### Process Monitoring

```bash
# Check running processes
ps aux | grep -E "(langgraph|node)" | grep -v grep

# Check port usage
netstat -an | grep -E "(2024|3000)"

# Monitor resource usage
top -p $(pgrep -f "langgraph\|node")
```

## 🔄 Restarting Components

### Restart LangGraph Server Only
```bash
# Stop current server (Ctrl+C)
# Then restart:
cd /Users/jonathanferrell/deepAgent
langgraph dev --config server/langgraph.json --host 127.0.0.1 --port 2024 --no-browser
```

### Restart UI Only
```bash
# Stop current UI (Ctrl+C)
# Then restart:
cd /Users/jonathanferrell/deepAgent/ui
npm run dev
```

### Restart Everything
```bash
# Use the stop script
./server/stop_all.sh

# Wait a moment
sleep 2

# Use the start script
./server/start_all.sh
```

## 📝 Notes

- **Development Mode**: Both servers run in development mode with hot reloading
- **File Watching**: Changes to agent code will automatically reload the LangGraph server
- **Memory Usage**: The in-memory server is designed for development, not production
- **API Keys**: Keep your API keys secure and never commit them to version control

## 🆘 Getting Help

If you encounter issues:

1. Check the logs in both terminals
2. Verify all prerequisites are met
3. Try restarting the components
4. Check the troubleshooting section above
5. Review the [Deep Agents documentation](https://github.com/langchain-ai/deepagents)
6. Review the [UI documentation](https://github.com/langchain-ai/deep-agents-ui)

---

**Happy coding with Deep Agents! 🤖✨**
