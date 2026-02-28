"""
Base Agent Class - Abstract foundation for all specialized agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, Field
from loguru import logger


class Message(BaseModel):
    """Structured message format for inter-agent communication"""
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    sender: str
    receiver: str
    message_type: str
    priority: str = "medium"  # low, medium, high, critical
    payload: Dict[str, Any]
    context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2024-01-15T10:30:00Z",
                "sender": "researcher",
                "receiver": "planner",
                "message_type": "research_complete",
                "priority": "high",
                "payload": {
                    "findings": ["fact1", "fact2"],
                    "confidence": 0.85
                },
                "context": {"task_id": "task-123"},
                "metadata": {"tokens_used": 1500}
            }
        }


class AgentState(BaseModel):
    """Agent internal state"""
    agent_id: str
    agent_type: str
    status: str = "idle"  # idle, thinking, acting, waiting
    current_task: Optional[str] = None
    working_memory: List[Dict[str, Any]] = Field(default_factory=list)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)
    last_updated: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the multi-agent AGI system.
    
    Each agent must implement:
    - process_message: Handle incoming messages
    - execute_task: Perform agent-specific tasks
    - self_evaluate: Assess own performance
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        self.state = AgentState(
            agent_id=agent_id,
            agent_type=agent_type
        )
        
        self.message_queue: List[Message] = []
        self.sent_messages: List[Message] = []
        self.received_messages: List[Message] = []
        
        logger.info(f"Initialized {agent_type} agent: {agent_id}")
    
    @abstractmethod
    def process_message(self, message: Message) -> Optional[Message]:
        """
        Process incoming message and optionally return a response.
        
        Args:
            message: Incoming message from another agent
            
        Returns:
            Optional response message
        """
        pass
    
    @abstractmethod
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent-specific task.
        
        Args:
            task: Task specification with parameters
            
        Returns:
            Task execution result
        """
        pass
    
    @abstractmethod
    def self_evaluate(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate own performance on completed task.
        
        Args:
            result: Task execution result
            
        Returns:
            Self-evaluation metrics and insights
        """
        pass
    
    def send_message(
        self,
        receiver: str,
        message_type: str,
        payload: Dict[str, Any],
        priority: str = "medium",
        context: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Send message to another agent.
        
        Args:
            receiver: Target agent ID
            message_type: Type of message
            payload: Message content
            priority: Message priority level
            context: Additional context information
            
        Returns:
            Sent message object
        """
        message = Message(
            sender=self.agent_id,
            receiver=receiver,
            message_type=message_type,
            priority=priority,
            payload=payload,
            context=context or {}
        )
        
        self.sent_messages.append(message)
        logger.debug(f"{self.agent_id} → {receiver}: {message_type}")
        
        return message
    
    def receive_message(self, message: Message) -> None:
        """
        Receive and queue incoming message.
        
        Args:
            message: Incoming message
        """
        self.received_messages.append(message)
        self.message_queue.append(message)
        logger.debug(f"{self.agent_id} ← {message.sender}: {message.message_type}")
    
    def process_queue(self) -> List[Message]:
        """
        Process all messages in queue.
        
        Returns:
            List of response messages
        """
        responses = []
        
        while self.message_queue:
            message = self.message_queue.pop(0)
            response = self.process_message(message)
            
            if response:
                responses.append(response)
        
        return responses
    
    def update_state(
        self,
        status: Optional[str] = None,
        current_task: Optional[str] = None,
        metrics: Optional[Dict[str, float]] = None
    ) -> None:
        """
        Update agent internal state.
        
        Args:
            status: New status
            current_task: Current task ID
            metrics: Performance metrics to update
        """
        if status:
            self.state.status = status
        
        if current_task:
            self.state.current_task = current_task
        
        if metrics:
            self.state.performance_metrics.update(metrics)
        
        self.state.last_updated = datetime.utcnow().isoformat()
    
    def add_to_working_memory(self, item: Dict[str, Any]) -> None:
        """
        Add item to working memory with timestamp.
        
        Args:
            item: Memory item to store
        """
        memory_item = {
            "timestamp": datetime.utcnow().isoformat(),
            "content": item
        }
        self.state.working_memory.append(memory_item)
        
        # Keep working memory bounded (last 100 items)
        if len(self.state.working_memory) > 100:
            self.state.working_memory = self.state.working_memory[-100:]
    
    def get_working_memory(self, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve items from working memory.
        
        Args:
            last_n: Number of recent items to retrieve
            
        Returns:
            List of memory items
        """
        if last_n:
            return self.state.working_memory[-last_n:]
        return self.state.working_memory
    
    def get_state(self) -> AgentState:
        """Get current agent state"""
        return self.state
    
    def reset(self) -> None:
        """Reset agent to initial state"""
        self.state = AgentState(
            agent_id=self.agent_id,
            agent_type=self.agent_type
        )
        self.message_queue.clear()
        logger.info(f"Reset agent: {self.agent_id}")
    
    def __repr__(self) -> str:
        return f"{self.agent_type}(id={self.agent_id}, status={self.state.status})"
