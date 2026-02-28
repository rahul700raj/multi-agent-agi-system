"""
Cognitive Loop - Main orchestration system for multi-agent AGI
"""

from typing import Dict, Any, List, Optional
from loguru import logger
from datetime import datetime
import asyncio

from agents.researcher import ResearcherAgent
from agents.planner import PlannerAgent
from agents.base_agent import Message


class CognitiveSystem:
    """
    Main cognitive processing system implementing the OBSERVE-THINK-PLAN-ACT-REFLECT-LEARN loop.
    
    Architecture:
    1. OBSERVE - Perceive environment and user input
    2. THINK - Reason about observations using working memory
    3. PLAN - Decompose goals into actionable tasks
    4. ACT - Execute planned actions using tools
    5. REFLECT - Self-critique and evaluate outcomes
    6. LEARN - Update knowledge base and improve
    """
    
    def __init__(
        self,
        researcher: Optional[ResearcherAgent] = None,
        planner: Optional[PlannerAgent] = None,
        max_iterations: int = 10,
        convergence_threshold: float = 0.9
    ):
        # Initialize agents
        self.researcher = researcher or ResearcherAgent()
        self.planner = planner or PlannerAgent()
        
        # System configuration
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        
        # System state
        self.iteration_count = 0
        self.task_history: List[Dict[str, Any]] = []
        self.performance_metrics: Dict[str, float] = {
            "success_rate": 0.0,
            "avg_iterations": 0.0,
            "avg_confidence": 0.0
        }
        
        logger.info("Cognitive System initialized")
    
    def solve_task(
        self,
        goal: str,
        context: Optional[Dict[str, Any]] = None,
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for autonomous task solving.
        
        Args:
            goal: High-level objective to achieve
            context: Additional context information
            constraints: Task constraints and requirements
            
        Returns:
            Task result with execution trace and metrics
        """
        logger.info(f"Starting task: {goal}")
        
        task_id = f"task_{datetime.utcnow().timestamp()}"
        self.iteration_count = 0
        
        # Initialize task state
        task_state = {
            "task_id": task_id,
            "goal": goal,
            "context": context or {},
            "constraints": constraints or {},
            "status": "in_progress",
            "iterations": [],
            "final_result": None,
            "confidence": 0.0
        }
        
        # Execute cognitive loop
        while self.iteration_count < self.max_iterations:
            self.iteration_count += 1
            logger.info(f"Iteration {self.iteration_count}/{self.max_iterations}")
            
            # Run one iteration of cognitive loop
            iteration_result = self._cognitive_iteration(task_state)
            task_state["iterations"].append(iteration_result)
            
            # Check convergence
            if self._check_convergence(iteration_result):
                logger.info("Task converged successfully")
                task_state["status"] = "completed"
                task_state["final_result"] = iteration_result.get("result")
                task_state["confidence"] = iteration_result.get("confidence", 0.0)
                break
            
            # Check for failure
            if iteration_result.get("status") == "failed":
                logger.warning("Task failed")
                task_state["status"] = "failed"
                break
        
        # If max iterations reached without convergence
        if task_state["status"] == "in_progress":
            logger.warning("Max iterations reached")
            task_state["status"] = "incomplete"
            task_state["final_result"] = task_state["iterations"][-1].get("result")
            task_state["confidence"] = task_state["iterations"][-1].get("confidence", 0.0)
        
        # Store in history
        self.task_history.append(task_state)
        
        # Update metrics
        self._update_metrics(task_state)
        
        return self._format_result(task_state)
    
    def _cognitive_iteration(self, task_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute one iteration of the cognitive loop.
        
        Steps:
        1. OBSERVE - Gather current state
        2. THINK - Reason about state
        3. PLAN - Create action plan
        4. ACT - Execute plan
        5. REFLECT - Evaluate results
        6. LEARN - Update knowledge
        """
        iteration_result = {
            "iteration": self.iteration_count,
            "timestamp": datetime.utcnow().isoformat(),
            "steps": {}
        }
        
        try:
            # 1. OBSERVE
            observation = self._observe(task_state)
            iteration_result["steps"]["observe"] = observation
            
            # 2. THINK
            thoughts = self._think(observation, task_state)
            iteration_result["steps"]["think"] = thoughts
            
            # 3. PLAN
            plan = self._plan(thoughts, task_state)
            iteration_result["steps"]["plan"] = plan
            
            # 4. ACT
            action_result = self._act(plan, task_state)
            iteration_result["steps"]["act"] = action_result
            
            # 5. REFLECT
            reflection = self._reflect(action_result, task_state)
            iteration_result["steps"]["reflect"] = reflection
            
            # 6. LEARN
            learning = self._learn(reflection, task_state)
            iteration_result["steps"]["learn"] = learning
            
            # Aggregate results
            iteration_result["result"] = action_result
            iteration_result["confidence"] = reflection.get("confidence", 0.0)
            iteration_result["status"] = "success"
            
        except Exception as e:
            logger.error(f"Iteration failed: {str(e)}")
            iteration_result["status"] = "failed"
            iteration_result["error"] = str(e)
        
        return iteration_result
    
    def _observe(self, task_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        STEP 1: OBSERVE
        
        Perceive current environment state and gather relevant information.
        """
        logger.debug("OBSERVE: Gathering information")
        
        observation = {
            "goal": task_state["goal"],
            "iteration": self.iteration_count,
            "previous_results": [
                it.get("result") for it in task_state.get("iterations", [])
            ],
            "context": task_state.get("context", {}),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return observation
    
    def _think(
        self,
        observation: Dict[str, Any],
        task_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        STEP 2: THINK
        
        Reason about observations using working memory and past experiences.
        Implements chain-of-thought reasoning.
        """
        logger.debug("THINK: Reasoning about observations")
        
        # Analyze what we know
        goal = observation["goal"]
        previous_attempts = observation.get("previous_results", [])
        
        thoughts = {
            "goal_analysis": f"Need to achieve: {goal}",
            "current_understanding": "Analyzing requirements",
            "previous_attempts": len(previous_attempts),
            "reasoning_chain": [
                "1. Understand the goal",
                "2. Identify required information",
                "3. Determine necessary actions",
                "4. Consider potential obstacles"
            ],
            "next_action": "research" if self.iteration_count == 1 else "refine"
        }
        
        return thoughts
    
    def _plan(
        self,
        thoughts: Dict[str, Any],
        task_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        STEP 3: PLAN
        
        Create execution plan based on reasoning.
        Uses Planner agent for hierarchical task decomposition.
        """
        logger.debug("PLAN: Creating execution plan")
        
        # Request plan from Planner agent
        plan_request = Message(
            sender="cognitive_system",
            receiver="planner",
            message_type="create_plan",
            payload={
                "goal": task_state["goal"],
                "constraints": task_state.get("constraints", {}),
                "resources": ["web_search", "code_executor", "calculator"],
                "context": thoughts
            }
        )
        
        self.planner.receive_message(plan_request)
        responses = self.planner.process_queue()
        
        if responses:
            plan = responses[0].payload
        else:
            # Fallback simple plan
            plan = {
                "plan_id": f"plan_{self.iteration_count}",
                "goal": task_state["goal"],
                "schedule": [
                    {
                        "task_id": "research",
                        "description": f"Research {task_state['goal']}",
                        "type": "research"
                    }
                ]
            }
        
        return plan
    
    def _act(
        self,
        plan: Dict[str, Any],
        task_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        STEP 4: ACT
        
        Execute planned actions using appropriate tools and agents.
        """
        logger.debug("ACT: Executing plan")
        
        results = []
        schedule = plan.get("schedule", [])
        
        for task in schedule:
            task_type = task.get("type", "general")
            
            if task_type == "research":
                # Use Researcher agent
                research_request = Message(
                    sender="cognitive_system",
                    receiver="researcher",
                    message_type="research_request",
                    payload={
                        "query": task_state["goal"],
                        "depth": 3
                    }
                )
                
                self.researcher.receive_message(research_request)
                responses = self.researcher.process_queue()
                
                if responses:
                    results.append(responses[0].payload)
            
            # Add more task types (execution, analysis, etc.)
        
        action_result = {
            "plan_id": plan.get("plan_id"),
            "executed_tasks": len(results),
            "results": results,
            "status": "completed" if results else "failed"
        }
        
        return action_result
    
    def _reflect(
        self,
        action_result: Dict[str, Any],
        task_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        STEP 5: REFLECT
        
        Self-critique and evaluate action outcomes.
        Uses Critic agent for quality assessment.
        """
        logger.debug("REFLECT: Evaluating results")
        
        results = action_result.get("results", [])
        
        # Self-evaluation
        reflection = {
            "success": action_result.get("status") == "completed",
            "quality_assessment": {
                "completeness": len(results) > 0,
                "relevance": True,  # Placeholder
                "accuracy": True    # Placeholder
            },
            "confidence": 0.0,
            "improvements_needed": [],
            "lessons_learned": []
        }
        
        # Calculate confidence
        if results:
            avg_confidence = sum(
                r.get("confidence", 0.5) for r in results
            ) / len(results)
            reflection["confidence"] = avg_confidence
        
        # Identify improvements
        if reflection["confidence"] < self.convergence_threshold:
            reflection["improvements_needed"] = [
                "Need more information",
                "Refine search query",
                "Verify sources"
            ]
        
        return reflection
    
    def _learn(
        self,
        reflection: Dict[str, Any],
        task_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        STEP 6: LEARN
        
        Update knowledge base and improve future performance.
        Uses Memory Manager for persistent storage.
        """
        logger.debug("LEARN: Updating knowledge base")
        
        learning = {
            "knowledge_updated": True,
            "patterns_identified": [],
            "skills_improved": [],
            "memory_stored": True
        }
        
        # Store experience in memory (placeholder)
        # In production: use Memory Manager agent
        
        # Identify patterns
        if reflection.get("success"):
            learning["patterns_identified"].append("Successful research strategy")
        
        return learning
    
    def _check_convergence(self, iteration_result: Dict[str, Any]) -> bool:
        """Check if task has converged to satisfactory solution"""
        confidence = iteration_result.get("confidence", 0.0)
        status = iteration_result.get("status", "failed")
        
        return status == "success" and confidence >= self.convergence_threshold
    
    def _update_metrics(self, task_state: Dict[str, Any]) -> None:
        """Update system performance metrics"""
        success = task_state["status"] == "completed"
        iterations = len(task_state["iterations"])
        confidence = task_state.get("confidence", 0.0)
        
        # Update running averages
        n = len(self.task_history)
        self.performance_metrics["success_rate"] = (
            (self.performance_metrics["success_rate"] * (n - 1) + (1 if success else 0)) / n
        )
        self.performance_metrics["avg_iterations"] = (
            (self.performance_metrics["avg_iterations"] * (n - 1) + iterations) / n
        )
        self.performance_metrics["avg_confidence"] = (
            (self.performance_metrics["avg_confidence"] * (n - 1) + confidence) / n
        )
    
    def _format_result(self, task_state: Dict[str, Any]) -> Dict[str, Any]:
        """Format final result for user"""
        return {
            "task_id": task_state["task_id"],
            "goal": task_state["goal"],
            "status": task_state["status"],
            "result": task_state.get("final_result"),
            "confidence": task_state.get("confidence", 0.0),
            "iterations": len(task_state["iterations"]),
            "execution_trace": task_state["iterations"],
            "summary": self._generate_summary(task_state)
        }
    
    def _generate_summary(self, task_state: Dict[str, Any]) -> str:
        """Generate human-readable summary"""
        status = task_state["status"]
        iterations = len(task_state["iterations"])
        confidence = task_state.get("confidence", 0.0)
        
        summary = f"Task {status} after {iterations} iterations "
        summary += f"with {confidence:.1%} confidence."
        
        return summary
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        return {
            "total_tasks": len(self.task_history),
            "metrics": self.performance_metrics,
            "recent_tasks": self.task_history[-5:] if self.task_history else []
        }
