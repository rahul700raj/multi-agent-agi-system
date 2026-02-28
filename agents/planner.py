"""
Planner Agent - Strategic planning and goal decomposition
"""

from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent, Message
from loguru import logger
from enum import Enum


class PlanStatus(Enum):
    """Plan execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class Task(Dict):
    """Task representation"""
    pass


class PlannerAgent(BaseAgent):
    """
    Agent 2: Planner
    
    Responsibilities:
    - Hierarchical goal decomposition
    - Task scheduling and prioritization
    - Resource allocation
    - Contingency planning
    - Plan optimization
    """
    
    def __init__(
        self,
        agent_id: str = "planner",
        model_name: str = "gpt-4",
        planning_horizon: int = 10,
        optimization_method: str = "beam_search",
        beam_width: int = 5
    ):
        super().__init__(
            agent_id=agent_id,
            agent_type="planner",
            model_name=model_name
        )
        
        self.planning_horizon = planning_horizon
        self.optimization_method = optimization_method
        self.beam_width = beam_width
        
        self.active_plans: Dict[str, Dict[str, Any]] = {}
        self.plan_history: List[Dict[str, Any]] = []
    
    def process_message(self, message: Message) -> Optional[Message]:
        """
        Process planning requests.
        
        Handles:
        - create_plan: Generate new execution plan
        - update_plan: Modify existing plan
        - evaluate_plan: Assess plan feasibility
        """
        logger.info(f"Planner processing: {message.message_type}")
        
        if message.message_type == "create_plan":
            return self._handle_create_plan(message)
        
        elif message.message_type == "update_plan":
            return self._handle_update_plan(message)
        
        elif message.message_type == "evaluate_plan":
            return self._handle_evaluate_plan(message)
        
        elif message.message_type == "research_complete":
            return self._handle_research_results(message)
        
        return None
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create execution plan for goal.
        
        Args:
            task: {
                "goal": str,
                "constraints": Dict,
                "resources": List,
                "deadline": Optional[str]
            }
        
        Returns:
            Execution plan with task hierarchy
        """
        self.update_state(status="planning", current_task=task.get("task_id"))
        
        goal = task.get("goal", "")
        constraints = task.get("constraints", {})
        resources = task.get("resources", [])
        
        logger.info(f"Planning for goal: {goal}")
        
        # Step 1: Decompose goal hierarchically
        task_hierarchy = self._decompose_goal(goal, constraints)
        
        # Step 2: Schedule tasks
        schedule = self._schedule_tasks(task_hierarchy, constraints)
        
        # Step 3: Allocate resources
        resource_allocation = self._allocate_resources(schedule, resources)
        
        # Step 4: Create contingency plans
        contingencies = self._create_contingencies(schedule)
        
        # Step 5: Optimize plan
        optimized_plan = self._optimize_plan(schedule, resource_allocation)
        
        plan = {
            "plan_id": task.get("task_id"),
            "goal": goal,
            "task_hierarchy": task_hierarchy,
            "schedule": optimized_plan,
            "resource_allocation": resource_allocation,
            "contingencies": contingencies,
            "estimated_duration": self._estimate_duration(optimized_plan),
            "confidence": self._calculate_plan_confidence(optimized_plan),
            "status": PlanStatus.PENDING.value
        }
        
        self.active_plans[plan["plan_id"]] = plan
        self.add_to_working_memory(plan)
        
        self.update_state(status="idle")
        
        return plan
    
    def self_evaluate(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate planning quality.
        
        Metrics:
        - Plan completeness
        - Task granularity
        - Resource efficiency
        - Contingency coverage
        """
        task_hierarchy = result.get("task_hierarchy", {})
        schedule = result.get("schedule", [])
        contingencies = result.get("contingencies", [])
        
        evaluation = {
            "completeness": self._assess_completeness(task_hierarchy),
            "granularity": len(schedule) / max(len(task_hierarchy.get("subtasks", [])), 1),
            "resource_efficiency": self._assess_resource_efficiency(result),
            "contingency_coverage": len(contingencies) / max(len(schedule), 1),
            "quality_score": 0.0
        }
        
        evaluation["quality_score"] = (
            evaluation["completeness"] * 0.4 +
            evaluation["resource_efficiency"] * 0.3 +
            evaluation["contingency_coverage"] * 0.3
        )
        
        logger.info(f"Plan quality: {evaluation['quality_score']:.2f}")
        
        return evaluation
    
    def _handle_create_plan(self, message: Message) -> Message:
        """Handle plan creation request"""
        goal = message.payload.get("goal")
        constraints = message.payload.get("constraints", {})
        resources = message.payload.get("resources", [])
        
        task = {
            "task_id": message.message_id,
            "goal": goal,
            "constraints": constraints,
            "resources": resources
        }
        
        plan = self.execute_task(task)
        
        return self.send_message(
            receiver="executor",
            message_type="plan_created",
            payload=plan,
            priority="high",
            context=message.context
        )
    
    def _handle_update_plan(self, message: Message) -> Message:
        """Update existing plan based on feedback"""
        plan_id = message.payload.get("plan_id")
        updates = message.payload.get("updates", {})
        
        if plan_id in self.active_plans:
            plan = self.active_plans[plan_id]
            
            # Apply updates
            for key, value in updates.items():
                if key in plan:
                    plan[key] = value
            
            # Re-optimize
            plan["schedule"] = self._optimize_plan(
                plan["schedule"],
                plan["resource_allocation"]
            )
            
            return self.send_message(
                receiver=message.sender,
                message_type="plan_updated",
                payload=plan,
                context=message.context
            )
        
        return self.send_message(
            receiver=message.sender,
            message_type="error",
            payload={"error": "Plan not found"},
            context=message.context
        )
    
    def _handle_evaluate_plan(self, message: Message) -> Message:
        """Evaluate plan feasibility"""
        plan = message.payload.get("plan")
        
        evaluation = {
            "feasible": self._check_feasibility(plan),
            "estimated_success_rate": self._estimate_success_rate(plan),
            "risks": self._identify_risks(plan),
            "recommendations": self._generate_recommendations(plan)
        }
        
        return self.send_message(
            receiver=message.sender,
            message_type="plan_evaluation",
            payload=evaluation,
            context=message.context
        )
    
    def _handle_research_results(self, message: Message) -> Message:
        """Incorporate research results into planning"""
        findings = message.payload.get("findings", [])
        
        # Update knowledge base for planning
        self.add_to_working_memory({
            "type": "research_findings",
            "findings": findings
        })
        
        return self.send_message(
            receiver=message.sender,
            message_type="research_acknowledged",
            payload={"status": "incorporated"},
            context=message.context
        )
    
    def _decompose_goal(
        self,
        goal: str,
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Hierarchical Task Network (HTN) decomposition.
        
        Decomposes high-level goal into executable subtasks.
        """
        # Placeholder - use LLM for actual decomposition
        hierarchy = {
            "goal": goal,
            "subtasks": [
                {
                    "task_id": f"task_1",
                    "description": f"Research {goal}",
                    "type": "research",
                    "dependencies": [],
                    "estimated_duration": 5
                },
                {
                    "task_id": f"task_2",
                    "description": f"Analyze findings",
                    "type": "analysis",
                    "dependencies": ["task_1"],
                    "estimated_duration": 3
                },
                {
                    "task_id": f"task_3",
                    "description": f"Execute solution",
                    "type": "execution",
                    "dependencies": ["task_2"],
                    "estimated_duration": 7
                }
            ],
            "depth": 1
        }
        
        return hierarchy
    
    def _schedule_tasks(
        self,
        task_hierarchy: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Schedule tasks considering dependencies and constraints.
        
        Uses topological sorting for dependency resolution.
        """
        subtasks = task_hierarchy.get("subtasks", [])
        
        # Topological sort based on dependencies
        scheduled = []
        completed = set()
        
        while len(scheduled) < len(subtasks):
            for task in subtasks:
                if task["task_id"] not in completed:
                    deps = task.get("dependencies", [])
                    if all(dep in completed for dep in deps):
                        scheduled.append(task)
                        completed.add(task["task_id"])
        
        return scheduled
    
    def _allocate_resources(
        self,
        schedule: List[Dict[str, Any]],
        available_resources: List[str]
    ) -> Dict[str, List[str]]:
        """Allocate resources to tasks"""
        allocation = {}
        
        for task in schedule:
            task_id = task["task_id"]
            task_type = task.get("type", "general")
            
            # Simple allocation strategy
            if task_type == "research":
                allocation[task_id] = ["web_search", "knowledge_base"]
            elif task_type == "analysis":
                allocation[task_id] = ["reasoning_engine"]
            elif task_type == "execution":
                allocation[task_id] = ["code_executor", "api_caller"]
            else:
                allocation[task_id] = available_resources[:1]
        
        return allocation
    
    def _create_contingencies(
        self,
        schedule: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create contingency plans for potential failures"""
        contingencies = []
        
        for task in schedule:
            contingency = {
                "task_id": task["task_id"],
                "failure_scenarios": [
                    "timeout",
                    "resource_unavailable",
                    "invalid_result"
                ],
                "fallback_actions": [
                    "retry_with_different_parameters",
                    "use_alternative_tool",
                    "request_human_intervention"
                ]
            }
            contingencies.append(contingency)
        
        return contingencies
    
    def _optimize_plan(
        self,
        schedule: List[Dict[str, Any]],
        resource_allocation: Dict[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """
        Optimize plan using specified method.
        
        Methods:
        - beam_search: Explore multiple plan variations
        - greedy: Optimize locally
        - dynamic_programming: Global optimization
        """
        if self.optimization_method == "beam_search":
            return self._beam_search_optimize(schedule, resource_allocation)
        
        # Default: return original schedule
        return schedule
    
    def _beam_search_optimize(
        self,
        schedule: List[Dict[str, Any]],
        resource_allocation: Dict[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """Beam search optimization"""
        # Placeholder - implement actual beam search
        return schedule
    
    def _estimate_duration(self, schedule: List[Dict[str, Any]]) -> float:
        """Estimate total plan duration"""
        return sum(task.get("estimated_duration", 0) for task in schedule)
    
    def _calculate_plan_confidence(self, schedule: List[Dict[str, Any]]) -> float:
        """Calculate confidence in plan success"""
        # Placeholder - use historical success rates
        return 0.75
    
    def _assess_completeness(self, task_hierarchy: Dict[str, Any]) -> float:
        """Assess if plan covers all aspects of goal"""
        subtasks = task_hierarchy.get("subtasks", [])
        return min(len(subtasks) / 3, 1.0)  # Expect at least 3 subtasks
    
    def _assess_resource_efficiency(self, plan: Dict[str, Any]) -> float:
        """Assess resource utilization efficiency"""
        allocation = plan.get("resource_allocation", {})
        total_resources = sum(len(resources) for resources in allocation.values())
        tasks = len(plan.get("schedule", []))
        
        return min(tasks / max(total_resources, 1), 1.0)
    
    def _check_feasibility(self, plan: Dict[str, Any]) -> bool:
        """Check if plan is feasible"""
        # Check for circular dependencies, resource conflicts, etc.
        return True  # Placeholder
    
    def _estimate_success_rate(self, plan: Dict[str, Any]) -> float:
        """Estimate probability of plan success"""
        return plan.get("confidence", 0.5)
    
    def _identify_risks(self, plan: Dict[str, Any]) -> List[str]:
        """Identify potential risks in plan"""
        return [
            "Task dependencies may cause delays",
            "Resource availability not guaranteed",
            "External API failures possible"
        ]
    
    def _generate_recommendations(self, plan: Dict[str, Any]) -> List[str]:
        """Generate recommendations for plan improvement"""
        return [
            "Add more contingency plans",
            "Parallelize independent tasks",
            "Allocate backup resources"
        ]
