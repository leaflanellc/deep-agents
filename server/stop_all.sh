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
