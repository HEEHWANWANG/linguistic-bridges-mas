"""
Base Agent class for Linguistic Bridges Multi-Agent System
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import json


class BaseAgent(ABC):
    """Abstract base class for all agents in the system"""
    
    def __init__(
        self,
        name: str,
        agent_id: str,
        config: Dict[str, Any],
        shared_memory: Any,  # Vector DB instance
        logger: Optional[logging.Logger] = None
    ):
        self.name = name
        self.agent_id = agent_id
        self.config = config
        self.shared_memory = shared_memory
        self.logger = logger or self._setup_logger()
        self.state = "initialized"
        self.created_at = datetime.now()
        self.task_history: List[Dict[str, Any]] = []
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for this agent"""
        logger = logging.getLogger(f"Agent.{self.name}")
        logger.setLevel(logging.INFO)
        return logger
    
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task assigned to this agent
        
        Args:
            task: Dictionary containing task details
            
        Returns:
            Dictionary containing execution results
        """
        pass
    
    def log_task(self, task: Dict[str, Any], result: Dict[str, Any]):
        """Log task execution to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "result": result,
            "agent_state": self.state
        }
        self.task_history.append(entry)
        self.logger.info(f"Task completed: {task.get('type', 'unknown')}")
    
    async def store_in_memory(
        self,
        content: str,
        metadata: Dict[str, Any],
        collection: str = "default"
    ):
        """Store content in shared vector database"""
        try:
            await self.shared_memory.add(
                documents=[content],
                metadatas=[{
                    **metadata,
                    "agent_id": self.agent_id,
                    "agent_name": self.name,
                    "timestamp": datetime.now().isoformat()
                }],
                collection_name=collection
            )
            self.logger.debug(f"Stored content in memory: {collection}")
        except Exception as e:
            self.logger.error(f"Failed to store in memory: {e}")
    
    async def retrieve_from_memory(
        self,
        query: str,
        n_results: int = 5,
        collection: str = "default",
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant content from shared vector database"""
        try:
            results = await self.shared_memory.query(
                query_texts=[query],
                n_results=n_results,
                collection_name=collection,
                where=filter_metadata
            )
            self.logger.debug(f"Retrieved {len(results['documents'][0])} results from memory")
            return results
        except Exception as e:
            self.logger.error(f"Failed to retrieve from memory: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "name": self.name,
            "agent_id": self.agent_id,
            "state": self.state,
            "tasks_completed": len(self.task_history),
            "uptime": (datetime.now() - self.created_at).total_seconds(),
            "last_task": self.task_history[-1] if self.task_history else None
        }
    
    async def request_human_approval(
        self,
        decision: str,
        context: Dict[str, Any],
        timeout: int = 3600
    ) -> bool:
        """Request human approval for critical decisions"""
        self.logger.warning(f"Human approval requested: {decision}")
        print(f"\n{'='*60}")
        print(f"🔔 HUMAN APPROVAL REQUIRED")
        print(f"Agent: {self.name}")
        print(f"Decision: {decision}")
        print(f"Context: {json.dumps(context, indent=2)}")
        print(f"{'='*60}")
        
        # In production, this would integrate with a UI or notification system
        response = input("Approve? (y/n): ").strip().lower()
        return response == 'y'
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', state='{self.state}')>"
