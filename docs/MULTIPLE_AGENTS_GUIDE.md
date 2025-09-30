# Multiple Agents in Deep Agents UI

## Current Setup

You currently have **2 agents** configured in your `server/langgraph.json`:

1. **`simple_agent`** - Basic math and weather assistant
2. **`research_agent`** - Advanced research agent with web search

## How to Switch Between Agents

### Method 1: Change Environment Variable

The UI uses the `NEXT_PUBLIC_AGENT_ID` environment variable to determine which agent to connect to.

**To use the Simple Agent:**
```bash
# Edit ui/.env.local
echo 'NEXT_PUBLIC_DEPLOYMENT_URL="http://127.0.0.1:2024"
NEXT_PUBLIC_AGENT_ID="simple_agent"' > ui/.env.local

# Restart the UI
cd ui
npm run dev
```

**To use the Research Agent:**
```bash
# Edit ui/.env.local
echo 'NEXT_PUBLIC_DEPLOYMENT_URL="http://127.0.0.1:2024"
NEXT_PUBLIC_AGENT_ID="research_agent"' > ui/.env.local

# Restart the UI
cd ui
npm run dev
```

### Method 2: Create Multiple UI Instances

You can run multiple UI instances on different ports, each connected to a different agent:

**Terminal 1 - Simple Agent UI:**
```bash
cd /Users/jonathanferrell/deepAgent/ui
echo 'NEXT_PUBLIC_DEPLOYMENT_URL="http://127.0.0.1:2024"
NEXT_PUBLIC_AGENT_ID="simple_agent"' > .env.local
PORT=3000 npm run dev
```

**Terminal 2 - Research Agent UI:**
```bash
cd /Users/jonathanferrell/deepAgent/ui
echo 'NEXT_PUBLIC_DEPLOYMENT_URL="http://127.0.0.1:2024"
NEXT_PUBLIC_AGENT_ID="research_agent"' > .env.local
PORT=3001 npm run dev
```

**Access:**
- Simple Agent: http://localhost:3000
- Research Agent: http://localhost:3001

## Adding More Agents

### Step 1: Create New Agent File

Create a new agent file, for example `coding_agent.py`:

```python
#!/usr/bin/env python3
"""
Coding assistant agent for LangGraph UI integration.
"""

import os
from dotenv import load_dotenv
from deepagents import create_deep_agent

# Load environment variables from .env file
load_dotenv()

def write_code(filename: str, code: str) -> str:
    """Write code to a file"""
    return f"Code written to {filename}:\n```\n{code}\n```"

def run_tests() -> str:
    """Run tests for the current project"""
    return "Running tests... All tests passed! ✅"

def debug_code(code: str, error: str) -> str:
    """Debug code and suggest fixes"""
    return f"Debugging suggestion for error '{error}':\n- Check syntax\n- Verify imports\n- Add error handling"

# Create coding agent
agent = create_deep_agent(
    tools=[write_code, run_tests, debug_code],
    instructions="""You are a helpful coding assistant that can:
    1. Write and organize code
    2. Run tests and check for issues
    3. Debug code and suggest fixes
    4. Help with code reviews and best practices
    
    Always provide clear, well-commented code and explain your reasoning.""",
)
```

### Step 2: Update server/langgraph.json

Add the new agent to your configuration:

```json
{
  "dependencies": ["."],
  "graphs": {
    "simple_agent": "./server/simple_agent_server.py:agent",
    "research_agent": "./src/agents/research_agent.py:agent",
    "coding_agent": "./src/agents/coding_agent.py:agent"
  },
  "env": ".env"
}
```

### Step 3: Restart LangGraph Server

```bash
# Stop current server (Ctrl+C)
# Restart with new configuration
langgraph dev --config server/langgraph.json --host 127.0.0.1 --port 2024 --no-browser
```

### Step 4: Use the New Agent

```bash
# Update UI to use coding agent
echo 'NEXT_PUBLIC_DEPLOYMENT_URL="http://127.0.0.1:2024"
NEXT_PUBLIC_AGENT_ID="coding_agent"' > ui/.env.local

# Restart UI
cd ui
npm run dev
```

## Agent Comparison

| Agent | Purpose | Tools | Best For |
|-------|---------|-------|----------|
| `simple_agent` | Basic assistance | Math, weather | Simple tasks, testing |
| `research_agent` | Research & analysis | Web search, file management | Deep research, reports |
| `coding_agent` | Code assistance | Code writing, testing, debugging | Development tasks |

## Advanced: Agent Selector UI

For a more sophisticated setup, you could modify the UI to include an agent selector. Here's a basic implementation:

### Create Agent Selector Component

Create `ui/src/app/components/AgentSelector/AgentSelector.tsx`:

```tsx
"use client";

import React, { useState } from "react";
import styles from "./AgentSelector.module.scss";

interface Agent {
  id: string;
  name: string;
  description: string;
}

const agents: Agent[] = [
  {
    id: "simple_agent",
    name: "Simple Assistant",
    description: "Basic math and weather assistance"
  },
  {
    id: "research_agent", 
    name: "Research Agent",
    description: "Advanced research with web search"
  },
  {
    id: "coding_agent",
    name: "Coding Assistant", 
    description: "Code writing, testing, and debugging"
  }
];

interface AgentSelectorProps {
  currentAgent: string;
  onAgentChange: (agentId: string) => void;
}

export function AgentSelector({ currentAgent, onAgentChange }: AgentSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  const handleAgentSelect = (agentId: string) => {
    onAgentChange(agentId);
    setIsOpen(false);
  };

  const currentAgentInfo = agents.find(a => a.id === currentAgent);

  return (
    <div className={styles.agentSelector}>
      <button 
        className={styles.selectorButton}
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className={styles.agentName}>
          {currentAgentInfo?.name || "Select Agent"}
        </span>
        <span className={styles.arrow}>▼</span>
      </button>
      
      {isOpen && (
        <div className={styles.dropdown}>
          {agents.map(agent => (
            <div
              key={agent.id}
              className={`${styles.agentOption} ${
                agent.id === currentAgent ? styles.selected : ""
              }`}
              onClick={() => handleAgentSelect(agent.id)}
            >
              <div className={styles.agentName}>{agent.name}</div>
              <div className={styles.agentDescription}>{agent.description}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Quick Agent Switching Script

Create `switch_agent.sh`:

```bash
#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: ./switch_agent.sh <agent_id>"
    echo "Available agents:"
    echo "  simple_agent    - Basic math and weather"
    echo "  research_agent  - Research with web search"
    echo "  coding_agent    - Code assistance"
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
```

Make it executable:
```bash
chmod +x switch_agent.sh
```

Usage:
```bash
./switch_agent.sh simple_agent
./switch_agent.sh research_agent
./switch_agent.sh coding_agent
```

## Summary

- ✅ You can have multiple agents running simultaneously
- ✅ Switch between agents by changing the `NEXT_PUBLIC_AGENT_ID` environment variable
- ✅ Each agent runs independently with its own tools and capabilities
- ✅ You can run multiple UI instances for different agents
- ✅ Easy to add new agents by creating new files and updating the configuration

The current setup gives you full flexibility to work with multiple specialized agents!
