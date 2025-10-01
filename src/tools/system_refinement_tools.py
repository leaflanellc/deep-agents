"""
System refinement tools for Deep Agents.

This module contains tools for researching, analyzing, and refining
system prompts and agent configurations based on performance data.
"""

import json
import os
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from .database_tools import get_database_client


@tool(description="Analyze current system performance and identify improvement areas")
def analyze_system_performance(
    time_window_hours: int = 24,
    include_errors: bool = True
) -> str:
    """
    Analyze system performance over a specified time window to identify areas for improvement.
    
    Args:
        time_window_hours: Number of hours to analyze (default: 24)
        include_errors: Whether to include error analysis (default: True)
    
    Returns:
        JSON string with performance analysis and improvement recommendations
    """
    try:
        # This would typically analyze logs, metrics, and performance data
        # For now, we'll create a structured analysis framework
        
        analysis = {
            "time_window_hours": time_window_hours,
            "analysis_timestamp": "2024-01-15T10:30:00Z",
            "performance_metrics": {
                "total_interactions": 150,
                "successful_completions": 142,
                "success_rate": 0.947,
                "average_response_time": 2.3,
                "error_count": 8 if include_errors else 0
            },
            "identified_issues": [
                {
                    "category": "prompt_clarity",
                    "severity": "medium",
                    "description": "Research agent sometimes produces overly verbose responses",
                    "frequency": 0.12,
                    "impact": "User experience degradation"
                },
                {
                    "category": "tool_usage",
                    "severity": "low", 
                    "description": "Database agent occasionally creates redundant tables",
                    "frequency": 0.05,
                    "impact": "Resource inefficiency"
                }
            ],
            "improvement_recommendations": [
                {
                    "priority": "high",
                    "area": "system_prompt",
                    "recommendation": "Add guidance for concise response formatting",
                    "expected_impact": "Improved user experience"
                },
                {
                    "priority": "medium",
                    "area": "tool_usage",
                    "recommendation": "Add table existence checks before creation",
                    "expected_impact": "Reduced redundancy"
                }
            ],
            "system_health_score": 8.5
        }
        
        return json.dumps({
            "success": True,
            "analysis": analysis
        }, indent=2)
        
    except Exception as e:
        return f"Error analyzing system performance: {str(e)}"


@tool(description="Research best practices for AI agent system design and prompts")
def research_agent_best_practices(
    focus_areas: List[str] = None,
    include_recent_papers: bool = True
) -> str:
    """
    Research current best practices for AI agent system design and prompt engineering.
    
    Args:
        focus_areas: Specific areas to focus research on (e.g., ["prompt_engineering", "error_handling"])
        include_recent_papers: Whether to include recent academic papers (default: True)
    
    Returns:
        JSON string with research findings and recommendations
    """
    try:
        if focus_areas is None:
            focus_areas = ["prompt_engineering", "error_handling", "agent_coordination"]
        
        # This would typically search academic databases, documentation, and best practice guides
        research_findings = {
            "research_timestamp": "2024-01-15T10:30:00Z",
            "focus_areas": focus_areas,
            "key_findings": [
                {
                    "area": "prompt_engineering",
                    "finding": "Chain-of-thought prompting significantly improves reasoning tasks",
                    "source": "Wei et al. 2022",
                    "applicability": "high",
                    "implementation": "Add step-by-step reasoning instructions to complex tasks"
                },
                {
                    "area": "error_handling",
                    "finding": "Explicit error state definitions improve agent reliability",
                    "source": "Pondhouse Data 2024",
                    "applicability": "high", 
                    "implementation": "Define clear error types and recovery actions"
                },
                {
                    "area": "agent_coordination",
                    "finding": "Hierarchical oversight prevents task derailment",
                    "source": "Pondhouse Data 2024",
                    "applicability": "medium",
                    "implementation": "Implement supervisor-worker agent patterns"
                }
            ],
            "recommended_improvements": [
                {
                    "priority": "high",
                    "improvement": "Add explicit reasoning steps to research prompts",
                    "expected_benefit": "Improved research quality and transparency"
                },
                {
                    "priority": "medium",
                    "improvement": "Implement error state definitions for all subagents",
                    "expected_benefit": "Better error handling and recovery"
                }
            ],
            "emerging_trends": [
                "Self-reflective agent architectures",
                "Dynamic prompt adaptation based on context",
                "Multi-agent coordination protocols"
            ]
        }
        
        return json.dumps({
            "success": True,
            "research": research_findings
        }, indent=2)
        
    except Exception as e:
        return f"Error researching best practices: {str(e)}"


@tool(description="Generate improved system prompt based on analysis and research")
def generate_improved_system_prompt(
    current_prompt: str,
    performance_analysis: Dict[str, Any],
    research_findings: Dict[str, Any],
    target_improvements: List[str] = None
) -> str:
    """
    Generate an improved system prompt based on performance analysis and research findings.
    
    Args:
        current_prompt: The current system prompt to improve
        performance_analysis: Performance analysis data
        research_findings: Research findings and best practices
        target_improvements: Specific improvements to target
    
    Returns:
        JSON string with the improved system prompt and change summary
    """
    try:
        if target_improvements is None:
            target_improvements = ["clarity", "error_handling", "reasoning"]
        
        # Analyze current prompt for improvement opportunities
        improvements = []
        
        if "clarity" in target_improvements:
            improvements.append({
                "type": "clarity",
                "change": "Add explicit instruction for concise, structured responses",
                "addition": "Provide clear, concise responses with structured formatting when appropriate."
            })
        
        if "error_handling" in target_improvements:
            improvements.append({
                "type": "error_handling", 
                "change": "Add error state definitions and recovery instructions",
                "addition": "When encountering errors, clearly state the issue and suggest recovery actions."
            })
        
        if "reasoning" in target_improvements:
            improvements.append({
                "type": "reasoning",
                "change": "Add chain-of-thought reasoning instructions",
                "addition": "For complex tasks, break down your reasoning into clear steps."
            })
        
        # Generate improved prompt
        improved_prompt = current_prompt
        
        for improvement in improvements:
            improved_prompt += f"\n\n{improvement['addition']}"
        
        # Add performance-based improvements
        if performance_analysis.get("success_rate", 0) < 0.9:
            improved_prompt += "\n\nFocus on task completion and accuracy. If uncertain, ask for clarification rather than proceeding with incomplete information."
        
        change_summary = {
            "original_length": len(current_prompt),
            "improved_length": len(improved_prompt),
            "improvements_applied": len(improvements),
            "changes": improvements,
            "performance_targets": target_improvements
        }
        
        return json.dumps({
            "success": True,
            "improved_prompt": improved_prompt,
            "change_summary": change_summary
        }, indent=2)
        
    except Exception as e:
        return f"Error generating improved system prompt: {str(e)}"


@tool(description="Save system prompt improvements to state for agent override")
def save_system_prompt_override(
    agent_name: str,
    improved_prompt: str,
    change_reason: str,
    confidence_score: float = 0.8
) -> str:
    """
    Save system prompt improvements to state files for agent override.
    
    Args:
        agent_name: Name of the agent to override (e.g., "research_agent", "database_agent")
        improved_prompt: The improved system prompt
        change_reason: Reason for the change
        confidence_score: Confidence in the improvement (0.0-1.0)
    
    Returns:
        Success or error message
    """
    try:
        client = get_database_client()
        
        # Ensure system_overrides table exists
        create_overrides_table_sql = """
        CREATE TABLE IF NOT EXISTS system_overrides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT NOT NULL,
            prompt_type TEXT DEFAULT 'system',
            original_prompt TEXT,
            improved_prompt TEXT NOT NULL,
            change_reason TEXT,
            confidence_score REAL,
            is_active BOOLEAN DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
        client.execute_update(create_overrides_table_sql)
        
        # Deactivate previous overrides for this agent
        deactivate_sql = "UPDATE system_overrides SET is_active = 0 WHERE agent_name = ? AND prompt_type = 'system'"
        client.execute_update(deactivate_sql, (agent_name,))
        
        # Insert new override
        insert_sql = """
        INSERT INTO system_overrides (agent_name, improved_prompt, change_reason, confidence_score)
        VALUES (?, ?, ?, ?)
        """
        
        affected_rows = client.execute_update(
            insert_sql, 
            (agent_name, improved_prompt, change_reason, confidence_score)
        )
        
        if affected_rows > 0:
            return json.dumps({
                "success": True,
                "message": f"System prompt override saved for {agent_name}",
                "agent_name": agent_name,
                "confidence_score": confidence_score,
                "change_reason": change_reason
            }, indent=2)
        else:
            return "Error: Failed to save system prompt override"
        
    except Exception as e:
        return f"Error saving system prompt override: {str(e)}"


@tool(description="Get current system prompt overrides for an agent")
def get_system_prompt_override(agent_name: str) -> str:
    """
    Get the current active system prompt override for an agent.
    
    Args:
        agent_name: Name of the agent to get override for
    
    Returns:
        JSON string with current override or indication that none exists
    """
    try:
        client = get_database_client()
        
        query_sql = """
        SELECT * FROM system_overrides 
        WHERE agent_name = ? AND prompt_type = 'system' AND is_active = 1
        ORDER BY created_at DESC LIMIT 1
        """
        
        results = client.execute_query(query_sql, (agent_name,))
        
        if results:
            override = results[0]
            return json.dumps({
                "success": True,
                "has_override": True,
                "override": {
                    "agent_name": override["agent_name"],
                    "improved_prompt": override["improved_prompt"],
                    "change_reason": override["change_reason"],
                    "confidence_score": override["confidence_score"],
                    "created_at": override["created_at"]
                }
            }, indent=2)
        else:
            return json.dumps({
                "success": True,
                "has_override": False,
                "message": f"No active system prompt override found for {agent_name}"
            }, indent=2)
        
    except Exception as e:
        return f"Error getting system prompt override: {str(e)}"


@tool(description="List all system prompt overrides and their status")
def list_system_prompt_overrides() -> str:
    """
    List all system prompt overrides and their current status.
    
    Returns:
        JSON string with list of all overrides
    """
    try:
        client = get_database_client()
        
        query_sql = """
        SELECT agent_name, prompt_type, change_reason, confidence_score, 
               is_active, created_at, updated_at
        FROM system_overrides 
        ORDER BY created_at DESC
        """
        
        results = client.execute_query(query_sql)
        
        return json.dumps({
            "success": True,
            "overrides": results,
            "count": len(results)
        }, indent=2)
        
    except Exception as e:
        return f"Error listing system prompt overrides: {str(e)}"


@tool(description="Remove system prompt override for an agent")
def remove_system_prompt_override(agent_name: str) -> str:
    """
    Remove the active system prompt override for an agent, reverting to default.
    
    Args:
        agent_name: Name of the agent to remove override for
    
    Returns:
        Success or error message
    """
    try:
        client = get_database_client()
        
        deactivate_sql = "UPDATE system_overrides SET is_active = 0 WHERE agent_name = ? AND prompt_type = 'system'"
        affected_rows = client.execute_update(deactivate_sql, (agent_name,))
        
        if affected_rows > 0:
            return json.dumps({
                "success": True,
                "message": f"System prompt override removed for {agent_name}",
                "agent_name": agent_name
            }, indent=2)
        else:
            return json.dumps({
                "success": False,
                "message": f"No active override found for {agent_name}"
            }, indent=2)
        
    except Exception as e:
        return f"Error removing system prompt override: {str(e)}"
