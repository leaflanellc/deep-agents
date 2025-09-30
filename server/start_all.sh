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
