#!/usr/bin/env python3
"""
Simple agent server for LangGraph UI integration.
This file exposes the agent for use with the Deep Agents UI.
"""

import os
from dotenv import load_dotenv
from deepagents import simple_agent

# Load environment variables from .env file
load_dotenv()

# Use the agent from the new structure
agent = simple_agent
