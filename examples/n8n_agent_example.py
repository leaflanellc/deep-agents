#!/usr/bin/env python3
"""
Example demonstrating the n8n Agent for workflow management.

This example shows how to use the n8n agent to:
- List existing workflows
- Get workflow details
- Create new workflows
- Execute and test workflows
- View execution results

Make sure to set N8N_API_KEY in your .env file before running this example.
"""

import os
import asyncio
from dotenv import load_dotenv
from src.agents.n8n_agent import create_n8n_agent
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()


async def main():
    """Main function demonstrating n8n agent usage."""
    
    print("🔧 n8n Agent Example")
    print("=" * 50)
    
    # Check if API key is set
    n8n_api_key = os.getenv("N8N_API_KEY")
    n8n_base_url = os.getenv("N8N_BASE_URL", "https://leaflane.app.n8n.cloud/api/v1")
    
    if not n8n_api_key or n8n_api_key == "your_n8n_api_key_here":
        print("\n⚠️  Please set your N8N_API_KEY in the .env file:")
        print("   1. Open the .env file in this directory")
        print("   2. Add: N8N_API_KEY=your_actual_n8n_api_key")
        print(f"   3. Optional: N8N_BASE_URL={n8n_base_url}")
        print("\n   Get your API key from: https://docs.n8n.io/api/authentication/")
        return
    
    print(f"✅ N8N_API_KEY loaded")
    print(f"✅ N8N_BASE_URL: {n8n_base_url}")
    print()
    
    # Create the n8n agent
    agent = create_n8n_agent()
    
    # Example 1: List all workflows
    print("📋 Example 1: Listing all workflows")
    print("-" * 50)
    
    result = await agent.ainvoke({
        "messages": [
            HumanMessage(content="List all my n8n workflows and give me a summary of what each one does.")
        ]
    })
    
    print(f"Agent: {result['messages'][-1].content}\n")
    
    # Example 2: Get details of a specific workflow
    print("🔍 Example 2: Get workflow details")
    print("-" * 50)
    
    result = await agent.ainvoke({
        "messages": [
            HumanMessage(content="Get the details of the first workflow, including its nodes and structure.")
        ]
    })
    
    print(f"Agent: {result['messages'][-1].content}\n")
    
    # Example 3: View recent executions
    print("📊 Example 3: View execution history")
    print("-" * 50)
    
    result = await agent.ainvoke({
        "messages": [
            HumanMessage(content="Show me the recent execution history and let me know if there are any errors.")
        ]
    })
    
    print(f"Agent: {result['messages'][-1].content}\n")
    
    # Example 4: Design a new workflow (conceptual)
    print("🎨 Example 4: Design workflow assistance")
    print("-" * 50)
    
    result = await agent.ainvoke({
        "messages": [
            HumanMessage(content="""I want to create a workflow that:
            1. Triggers when a webhook is called
            2. Extracts data from the webhook payload
            3. Sends a Slack message with the data
            
            Can you help me design this workflow and explain what nodes I would need?""")
        ]
    })
    
    print(f"Agent: {result['messages'][-1].content}\n")
    
    print("✅ n8n Agent examples completed!")
    print("\nThe n8n agent can help you with:")
    print("  • Listing and browsing workflows")
    print("  • Understanding workflow structure and logic")
    print("  • Creating and editing workflows")
    print("  • Testing and debugging executions")
    print("  • Planning new automation workflows")
    print("  • Providing n8n best practices")


if __name__ == "__main__":
    asyncio.run(main())

