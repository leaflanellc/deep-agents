"""
Evaluation middleware for Deep Agents.

This middleware implements a hybrid triggering mechanism that combines
continuous monitoring with periodic evaluation pauses for system improvement.
"""

import json
import time
from typing import Dict, Any, Optional
from langchain.agents.middleware import AgentMiddleware, AgentState, ModelRequest


class EvaluationMiddleware(AgentMiddleware):
    """
    Middleware that implements hybrid evaluation triggering:
    - Continuous monitoring via todo list updates
    - Periodic evaluation pauses for comprehensive assessment
    """
    
    def __init__(
        self,
        evaluation_interval_hours: int = 24,
        performance_threshold: float = 0.8,
        auto_trigger_refinement: bool = True
    ):
        super().__init__()
        self.evaluation_interval_hours = evaluation_interval_hours
        self.performance_threshold = performance_threshold
        self.auto_trigger_refinement = auto_trigger_refinement
        self.last_evaluation_time = 0
        self.evaluation_count = 0
    
    def modify_model_request(self, request: ModelRequest, agent_state: AgentState) -> ModelRequest:
        """
        Modify the model request to include evaluation triggers when needed.
        """
        current_time = time.time()
        
        # Check if it's time for evaluation
        time_since_last_evaluation = (current_time - self.last_evaluation_time) / 3600  # Convert to hours
        
        should_evaluate = (
            time_since_last_evaluation >= self.evaluation_interval_hours or
            self._should_trigger_immediate_evaluation(agent_state)
        )
        
        if should_evaluate:
            # Add evaluation tasks to the system
            self._trigger_evaluation(agent_state)
            self.last_evaluation_time = current_time
            self.evaluation_count += 1
        
        return request
    
    def _should_trigger_immediate_evaluation(self, agent_state: AgentState) -> bool:
        """
        Check if immediate evaluation should be triggered based on current state.
        """
        # Check for error patterns or performance degradation
        messages = agent_state.get("messages", [])
        
        # Look for error indicators in recent messages
        recent_errors = 0
        for message in messages[-10:]:  # Check last 10 messages
            if hasattr(message, 'content') and isinstance(message.content, str):
                if any(error_indicator in message.content.lower() for error_indicator in 
                      ['error', 'failed', 'exception', 'timeout', 'unable to']):
                    recent_errors += 1
        
        # Trigger evaluation if too many recent errors
        if recent_errors >= 3:
            return True
        
        # Check if todos indicate system issues
        todos = agent_state.get("todos", [])
        system_issue_todos = [
            todo for todo in todos 
            if todo.get("content", "").lower().find("system") != -1 or
               todo.get("content", "").lower().find("improve") != -1 or
               todo.get("content", "").lower().find("refine") != -1
        ]
        
        # Trigger evaluation if there are system-related todos
        if len(system_issue_todos) >= 2:
            return True
        
        return False
    
    def _trigger_evaluation(self, agent_state: AgentState) -> None:
        """
        Trigger evaluation by adding tasks to the agent's todo list.
        """
        try:
            # Add evaluation tasks based on current state
            evaluation_tasks = []
            
            # Add periodic evaluation task
            evaluation_tasks.append({
                "content": "Conduct periodic system performance evaluation using evaluation-agent",
                "status": "pending",
                "priority": "medium",
                "category": "evaluation"
            })
            
            # Add system health monitoring task
            evaluation_tasks.append({
                "content": "Monitor system health and performance metrics using evaluation-agent",
                "status": "pending",
                "priority": "medium",
                "category": "evaluation"
            })
            
            # If auto-trigger is enabled, add refinement check task
            if self.auto_trigger_refinement:
                evaluation_tasks.append({
                    "content": "Check if system refinement is needed using evaluation-agent",
                    "status": "pending",
                    "priority": "medium",
                    "category": "evaluation"
                })
            
            # Add tasks to agent state
            current_todos = agent_state.get("todos", [])
            updated_todos = current_todos + evaluation_tasks
            agent_state["todos"] = updated_todos
        
        except Exception as e:
            # Log error but don't break the agent
            print(f"Error in evaluation middleware: {e}")


def create_evaluation_middleware(
    evaluation_interval_hours: int = 24,
    performance_threshold: float = 0.8,
    auto_trigger_refinement: bool = True
) -> EvaluationMiddleware:
    """
    Create an evaluation middleware with specified configuration.
    
    Args:
        evaluation_interval_hours: Hours between automatic evaluations (default: 24)
        performance_threshold: Performance threshold for triggering improvements (default: 0.8)
        auto_trigger_refinement: Whether to automatically trigger refinement (default: True)
    
    Returns:
        Configured EvaluationMiddleware instance
    """
    return EvaluationMiddleware(
        evaluation_interval_hours=evaluation_interval_hours,
        performance_threshold=performance_threshold,
        auto_trigger_refinement=auto_trigger_refinement
    )
