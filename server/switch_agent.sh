#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: ./switch_agent.sh <agent_id>"
    echo "Available agents:"
    echo "  simple_agent    - Basic math and weather"
    echo "  research_agent  - Research with web search"
    echo "  coding_agent    - Code assistance (if added)"
    exit 1
fi

AGENT_ID=$1

echo "🔄 Switching to agent: $AGENT_ID"

# Update UI configuration
echo "NEXT_PUBLIC_DEPLOYMENT_URL=\"http://127.0.0.1:2024\"
NEXT_PUBLIC_AGENT_ID=\"$AGENT_ID\"" > ui/.env.local

echo "✅ Agent switched to: $AGENT_ID"
echo "🔄 Please restart the UI:"
echo "   cd ui && npm run dev"
