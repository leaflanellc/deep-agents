#!/bin/bash

echo "🌐 Opening LangGraph UIs..."

# Check if server is running
if ! curl -s http://127.0.0.1:2024/health > /dev/null 2>&1; then
    echo "❌ LangGraph server is not running!"
    echo "   Please start it first:"
    echo "   langgraph dev --config langgraph.json --host 127.0.0.1 --port 2024 --no-browser"
    exit 1
fi

echo "✅ LangGraph server is running"

# Open LangGraph Studio
echo "🎨 Opening LangGraph Studio..."
open "https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024"

# Open API Documentation
echo "📚 Opening API Documentation..."
open "http://127.0.0.1:2024/docs"

echo ""
echo "🌐 UIs opened:"
echo "   🎨 LangGraph Studio: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024"
echo "   📚 API Docs: http://127.0.0.1:2024/docs"
echo ""
echo "💡 Tips:"
echo "   - Use Studio for debugging and monitoring agents"
echo "   - Use API Docs for testing endpoints"
echo "   - Switch between agents in Studio using the dropdown"
