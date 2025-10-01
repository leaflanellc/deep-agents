"""
Evaluation tools for Deep Agents.

This module contains tools for performance evaluation, monitoring,
and triggering system improvements based on agent performance.
"""

import json
import time
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from .database_tools import get_database_client


@tool(description="Evaluate agent performance and determine if improvements are needed")
def evaluate_agent_performance(
    agent_name: str,
    evaluation_criteria: List[str] = None,
    time_window_hours: int = 24
) -> str:
    """
    Evaluate agent performance against defined criteria and determine if improvements are needed.
    
    Args:
        agent_name: Name of the agent to evaluate
        evaluation_criteria: List of criteria to evaluate against
        time_window_hours: Time window for evaluation (default: 24)
    
    Returns:
        JSON string with evaluation results and improvement recommendations
    """
    try:
        if evaluation_criteria is None:
            evaluation_criteria = ["success_rate", "response_quality", "efficiency", "error_handling"]
        
        # Simulate performance data collection and analysis
        performance_data = {
            "agent_name": agent_name,
            "evaluation_timestamp": "2024-01-15T10:30:00Z",
            "time_window_hours": time_window_hours,
            "metrics": {
                "total_tasks": 45,
                "successful_tasks": 42,
                "failed_tasks": 3,
                "average_response_time": 2.1,
                "user_satisfaction": 0.89,
                "error_rate": 0.067
            },
            "criteria_evaluation": {
                "success_rate": {
                    "score": 0.933,
                    "threshold": 0.9,
                    "status": "good",
                    "recommendation": "Maintain current performance"
                },
                "response_quality": {
                    "score": 0.87,
                    "threshold": 0.85,
                    "status": "good",
                    "recommendation": "Minor improvements possible"
                },
                "efficiency": {
                    "score": 0.78,
                    "threshold": 0.8,
                    "status": "needs_improvement",
                    "recommendation": "Optimize response generation"
                },
                "error_handling": {
                    "score": 0.82,
                    "threshold": 0.85,
                    "status": "needs_improvement",
                    "recommendation": "Improve error recovery mechanisms"
                }
            },
            "overall_score": 0.85,
            "improvement_needed": True,
            "priority_areas": ["efficiency", "error_handling"],
            "recommended_actions": [
                {
                    "action": "system_prompt_refinement",
                    "priority": "high",
                    "description": "Refine system prompt to improve efficiency and error handling",
                    "expected_impact": "medium"
                },
                {
                    "action": "tool_optimization",
                    "priority": "medium", 
                    "description": "Optimize tool usage patterns",
                    "expected_impact": "low"
                }
            ]
        }
        
        return json.dumps({
            "success": True,
            "evaluation": performance_data
        }, indent=2)
        
    except Exception as e:
        return f"Error evaluating agent performance: {str(e)}"


@tool(description="Check if system refinement should be triggered based on performance")
def should_trigger_system_refinement(
    agent_name: str,
    performance_threshold: float = 0.8,
    time_since_last_refinement_hours: int = 24
) -> str:
    """
    Check if system refinement should be triggered based on current performance.
    
    Args:
        agent_name: Name of the agent to check
        performance_threshold: Minimum performance score to avoid refinement (default: 0.8)
        time_since_last_refinement_hours: Hours since last refinement (default: 24)
    
    Returns:
        JSON string with trigger decision and reasoning
    """
    try:
        # Simulate performance data instead of calling evaluate_agent_performance
        # to avoid circular dependencies
        overall_score = 0.85  # Simulate current performance score
        
        # Check if performance is below threshold
        performance_below_threshold = overall_score < performance_threshold
        
        # Check if enough time has passed since last refinement
        try:
            client = get_database_client()
            
            # Check if system_overrides table exists
            table_check_sql = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='system_overrides'
            """
            
            table_exists = client.execute_query(table_check_sql)
            
            if table_exists:
                # Check last refinement time
                last_refinement_sql = """
                SELECT MAX(created_at) as last_refinement
                FROM system_overrides 
                WHERE agent_name = ? AND prompt_type = 'system'
                """
                
                results = client.execute_query(last_refinement_sql, (agent_name,))
                last_refinement = results[0]["last_refinement"] if results and results[0]["last_refinement"] else None
                
                # Calculate time since last refinement
                if last_refinement:
                    # Parse timestamp and calculate hours difference
                    time_since_last = 48  # Simulate 48 hours for demo
                else:
                    time_since_last = 999  # No previous refinement
            else:
                # Table doesn't exist, so no previous refinement
                time_since_last = 999
                
        except Exception as e:
            # If database query fails, assume no previous refinement
            print(f"Database query failed in should_trigger_system_refinement: {e}")
            time_since_last = 999
        
        sufficient_time_passed = time_since_last >= time_since_last_refinement_hours
        
        # Determine if refinement should be triggered
        should_trigger = performance_below_threshold or sufficient_time_passed
        
        trigger_reasons = []
        if performance_below_threshold:
            trigger_reasons.append(f"Performance score {overall_score:.2f} below threshold {performance_threshold}")
        if sufficient_time_passed:
            trigger_reasons.append(f"Sufficient time ({time_since_last}h) since last refinement")
        
        return json.dumps({
            "success": True,
            "should_trigger": should_trigger,
            "agent_name": agent_name,
            "overall_score": overall_score,
            "performance_threshold": performance_threshold,
            "time_since_last_refinement_hours": time_since_last,
            "trigger_reasons": trigger_reasons,
            "priority_areas": ["efficiency", "error_handling"],
            "recommended_actions": [
                {
                    "action": "system_prompt_refinement",
                    "priority": "high",
                    "description": "Refine system prompt to improve efficiency and error handling",
                    "expected_impact": "medium"
                }
            ]
        }, indent=2)
        
    except Exception as e:
        return f"Error checking refinement trigger: {str(e)}"


@tool(description="Add evaluation tasks to agent todo list")
def add_evaluation_tasks_to_todos(
    agent_name: str,
    evaluation_results: Dict[str, Any]
) -> str:
    """
    Add evaluation-based improvement tasks to the agent's todo list.
    
    Args:
        agent_name: Name of the agent to add tasks for
        evaluation_results: Results from performance evaluation
    
    Returns:
        Success message with added tasks
    """
    try:
        # This would typically add tasks to the agent's todo system
        # For now, we'll return the tasks that should be added
        
        tasks_to_add = []
        
        if evaluation_results.get("improvement_needed", False):
            priority_areas = evaluation_results.get("priority_areas", [])
            recommended_actions = evaluation_results.get("recommended_actions", [])
            
            for area in priority_areas:
                tasks_to_add.append({
                    "content": f"Improve {area} based on performance evaluation",
                    "status": "pending",
                    "priority": "high",
                    "category": "system_improvement"
                })
            
            for action in recommended_actions:
                if action["priority"] == "high":
                    tasks_to_add.append({
                        "content": action["description"],
                        "status": "pending", 
                        "priority": action["priority"],
                        "category": "system_improvement"
                    })
        
        # Add periodic evaluation task
        tasks_to_add.append({
            "content": "Conduct periodic system performance evaluation",
            "status": "pending",
            "priority": "medium",
            "category": "evaluation"
        })
        
        return json.dumps({
            "success": True,
            "message": f"Added {len(tasks_to_add)} evaluation tasks for {agent_name}",
            "tasks_added": tasks_to_add,
            "agent_name": agent_name
        }, indent=2)
        
    except Exception as e:
        return f"Error adding evaluation tasks: {str(e)}"


@tool(description="Schedule evaluation pause for comprehensive system assessment")
def schedule_evaluation_pause(
    agent_name: str,
    pause_duration_minutes: int = 30,
    evaluation_scope: str = "comprehensive"
) -> str:
    """
    Schedule an evaluation pause for comprehensive system assessment.
    
    Args:
        agent_name: Name of the agent to schedule pause for
        pause_duration_minutes: Duration of the evaluation pause (default: 30)
        evaluation_scope: Scope of evaluation (comprehensive, focused, quick)
    
    Returns:
        Success message with pause schedule details
    """
    try:
        # This would typically integrate with the agent's scheduling system
        # For now, we'll return the pause schedule
        
        pause_schedule = {
            "agent_name": agent_name,
            "pause_duration_minutes": pause_duration_minutes,
            "evaluation_scope": evaluation_scope,
            "scheduled_time": "2024-01-15T11:00:00Z",
            "evaluation_tasks": [
                "Analyze recent performance metrics",
                "Research latest best practices",
                "Generate system prompt improvements",
                "Test and validate improvements",
                "Apply approved changes"
            ],
            "expected_outcomes": [
                "Improved system performance",
                "Updated prompt templates",
                "Enhanced error handling",
                "Optimized tool usage"
            ]
        }
        
        return json.dumps({
            "success": True,
            "message": f"Evaluation pause scheduled for {agent_name}",
            "pause_schedule": pause_schedule
        }, indent=2)
        
    except Exception as e:
        return f"Error scheduling evaluation pause: {str(e)}"


@tool(description="Monitor system health and performance metrics")
def monitor_system_health(
    include_subagents: bool = True,
    alert_threshold: float = 0.7
) -> str:
    """
    Monitor overall system health and performance metrics.
    
    Args:
        include_subagents: Whether to include subagent metrics (default: True)
        alert_threshold: Threshold for triggering alerts (default: 0.7)
    
    Returns:
        JSON string with system health status and alerts
    """
    try:
        # Simulate system health monitoring
        health_status = {
            "monitoring_timestamp": "2024-01-15T10:30:00Z",
            "overall_health_score": 0.85,
            "system_status": "healthy",
            "components": {
                "main_agent": {
                    "status": "healthy",
                    "performance_score": 0.88,
                    "last_error": None
                },
                "research_subagent": {
                    "status": "healthy", 
                    "performance_score": 0.92,
                    "last_error": None
                },
                "database_subagent": {
                    "status": "healthy",
                    "performance_score": 0.81,
                    "last_error": None
                },
                "prompt_subagent": {
                    "status": "healthy",
                    "performance_score": 0.79,
                    "last_error": None
                }
            },
            "alerts": [],
            "recommendations": [
                {
                    "component": "prompt_subagent",
                    "issue": "Performance below optimal",
                    "recommendation": "Consider prompt optimization",
                    "priority": "medium"
                }
            ]
        }
        
        # Check for alerts
        for component, data in health_status["components"].items():
            if data["performance_score"] < alert_threshold:
                health_status["alerts"].append({
                    "component": component,
                    "type": "performance_degradation",
                    "severity": "warning",
                    "message": f"{component} performance below threshold"
                })
        
        return json.dumps({
            "success": True,
            "health_status": health_status
        }, indent=2)
        
    except Exception as e:
        return f"Error monitoring system health: {str(e)}"


@tool(description="Get performance trends and historical data")
def get_performance_trends(
    days: int = 7,
    metric: str = "overall_score"
) -> str:
    """
    Get performance trends and historical data for analysis.
    
    Args:
        days: Number of days to analyze (default: 7)
        metric: Specific metric to analyze (default: "overall_score")
    
    Returns:
        JSON string with performance trends and insights
    """
    try:
        # Simulate historical performance data
        trends_data = {
            "analysis_period_days": days,
            "metric_analyzed": metric,
            "trend_direction": "improving",
            "data_points": [
                {"date": "2024-01-08", "value": 0.78},
                {"date": "2024-01-09", "value": 0.81},
                {"date": "2024-01-10", "value": 0.79},
                {"date": "2024-01-11", "value": 0.83},
                {"date": "2024-01-12", "value": 0.85},
                {"date": "2024-01-13", "value": 0.87},
                {"date": "2024-01-14", "value": 0.85},
                {"date": "2024-01-15", "value": 0.88}
            ],
            "insights": [
                "Performance has improved by 12.8% over the period",
                "Most significant improvement occurred on 2024-01-12",
                "Current performance is above historical average"
            ],
            "recommendations": [
                "Continue current improvement strategies",
                "Investigate factors that led to 2024-01-12 improvement",
                "Monitor for potential performance plateaus"
            ]
        }
        
        return json.dumps({
            "success": True,
            "trends": trends_data
        }, indent=2)
        
    except Exception as e:
        return f"Error getting performance trends: {str(e)}"
