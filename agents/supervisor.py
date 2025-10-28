"""
Supervisor Agent - Orchestrates all guilds and manages project workflow
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
from agents.base_agent import BaseAgent


class SupervisorAgent(BaseAgent):
    """
    Top-level orchestrator that coordinates Research, Forge, and Chroniclers guilds
    """
    
    def __init__(self, name: str, agent_id: str, config: Dict[str, Any], shared_memory: Any, mcp_manager: Any):
        super().__init__(name, agent_id, config, shared_memory)
        self.mcp_manager = mcp_manager
        self.guilds: Dict[str, Any] = {}
        self.project_state = {
            "phase": "initialization",  # initialization, research, implementation, documentation, complete
            "progress": {},
            "blockers": [],
            "resource_allocation": {}
        }
        self.max_iterations = config.get("max_iterations", 100)
        self.progress_check_interval = config.get("progress_check_interval", 300)
        self.last_progress_check = datetime.now()
    
    def register_guild(self, guild_name: str, guild_instance: Any):
        """Register a guild with the supervisor"""
        self.guilds[guild_name] = guild_instance
        self.logger.info(f"Registered guild: {guild_name}")
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute supervisor task"""
        task_type = task.get("type", "unknown")
        
        if task_type == "orchestrate_project":
            return await self.orchestrate_project(task)
        elif task_type == "monitor_progress":
            return await self.monitor_progress()
        elif task_type == "resolve_conflict":
            return await self.resolve_conflict(task.get("conflict", {}))
        else:
            self.logger.warning(f"Unknown task type: {task_type}")
            return {"status": "error", "message": f"Unknown task type: {task_type}"}
    
    async def orchestrate_project(self, project_goal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main orchestration loop for the entire Linguistic Bridges project
        """
        self.logger.info("🚀 Starting project orchestration: Linguistic Bridges")
        
        try:
            # Phase 1: Research & Hypothesis Development
            self.project_state["phase"] = "research"
            research_result = await self._coordinate_research_phase()
            
            if not research_result.get("success"):
                return {"status": "failed", "phase": "research", "error": research_result.get("error")}
            
            # Phase 2: Implementation & Experimentation
            self.project_state["phase"] = "implementation"
            implementation_result = await self._coordinate_implementation_phase(research_result)
            
            if not implementation_result.get("success"):
                return {"status": "failed", "phase": "implementation", "error": implementation_result.get("error")}
            
            # Phase 3: Documentation & Report Writing
            self.project_state["phase"] = "documentation"
            documentation_result = await self._coordinate_documentation_phase(
                research_result, implementation_result
            )
            
            self.project_state["phase"] = "complete"
            
            return {
                "status": "success",
                "research": research_result,
                "implementation": implementation_result,
                "documentation": documentation_result
            }
            
        except Exception as e:
            self.logger.error(f"Project orchestration failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _coordinate_research_phase(self) -> Dict[str, Any]:
        """Coordinate Research Guild to develop hypotheses"""
        self.logger.info("📚 Phase 1: Research & Hypothesis Development")
        
        if "research" not in self.guilds:
            return {"success": False, "error": "Research guild not registered"}
        
        research_guild = self.guilds["research"]
        
        # Task 1: Generate initial hypotheses
        hypothesis_task = {
            "type": "generate_hypotheses",
            "topic": "music and visual art alignment through language",
            "focus_areas": ["disentanglement", "mediator_function", "generation"],
            "num_hypotheses": 5
        }
        
        hypothesis_result = await research_guild.execute_task(hypothesis_task)
        
        # Task 2: Evolve hypotheses through Generate-Debate-Evolve loop
        evolution_task = {
            "type": "evolve_hypotheses",
            "initial_hypotheses": hypothesis_result.get("hypotheses", []),
            "num_rounds": 3
        }
        
        evolution_result = await research_guild.execute_task(evolution_task)
        
        # Task 3: Get final hypothesis approval
        final_hypotheses = evolution_result.get("final_hypotheses", [])
        
        if self.config.get("human_approval", {}).get("required_for", []):
            if "finalize_hypothesis" in self.config["human_approval"]["required_for"]:
                approved = await self.request_human_approval(
                    decision="Finalize Research Hypotheses",
                    context={
                        "top_hypotheses": final_hypotheses[:3],
                        "evolution_rounds": evolution_result.get("rounds_completed", 0)
                    }
                )
                
                if not approved:
                    return {"success": False, "error": "Human rejected hypothesis approval"}
        
        # Store finalized hypotheses in shared memory
        await self.store_in_memory(
            content=json.dumps(final_hypotheses, indent=2),
            metadata={
                "type": "finalized_hypotheses",
                "phase": "research",
                "timestamp": datetime.now().isoformat()
            },
            collection="project_artifacts"
        )
        
        return {
            "success": True,
            "hypotheses": final_hypotheses,
            "evolution_rounds": evolution_result.get("rounds_completed", 0)
        }
    
    async def _coordinate_implementation_phase(self, research_result: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate Forge Guild to implement and experiment"""
        self.logger.info("💻 Phase 2: Implementation & Experimentation")
        
        if "forge" not in self.guilds:
            return {"success": False, "error": "Forge guild not registered"}
        
        forge_guild = self.guilds["forge"]
        
        # Task 1: Setup data pipeline
        data_task = {
            "type": "setup_data_pipeline",
            "datasets": ["artemis", "sdd"]
        }
        
        data_result = await forge_guild.execute_task(data_task)
        
        # Task 2: Implement Track 1 (Disentanglement)
        track1_task = {
            "type": "implement_track",
            "track_id": 1,
            "track_name": "disentangled_representation_learning",
            "hypothesis": research_result["hypotheses"][0] if research_result["hypotheses"] else {}
        }
        
        track1_result = await forge_guild.execute_task(track1_task)
        
        # Task 3: Implement Track 2 (Mediator Function)
        track2_task = {
            "type": "implement_track",
            "track_id": 2,
            "track_name": "mediator_function_learning",
            "hypothesis": research_result["hypotheses"][1] if len(research_result["hypotheses"]) > 1 else {}
        }
        
        track2_result = await forge_guild.execute_task(track2_task)
        
        # Task 4: Implement Track 3 (Blueprint-Driven Generation)
        track3_task = {
            "type": "implement_track",
            "track_id": 3,
            "track_name": "blueprint_driven_generation",
            "hypothesis": research_result["hypotheses"][2] if len(research_result["hypotheses"]) > 2 else {}
        }
        
        track3_result = await forge_guild.execute_task(track3_task)
        
        # Task 5: Run evaluation
        eval_task = {
            "type": "run_evaluation",
            "tracks": [1, 2, 3]
        }
        
        eval_result = await forge_guild.execute_task(eval_task)
        
        return {
            "success": True,
            "data_pipeline": data_result,
            "track1": track1_result,
            "track2": track2_result,
            "track3": track3_result,
            "evaluation": eval_result
        }
    
    async def _coordinate_documentation_phase(
        self,
        research_result: Dict[str, Any],
        implementation_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Coordinate Chroniclers Guild to write final report"""
        self.logger.info("📝 Phase 3: Documentation & Report Writing")
        
        if "chroniclers" not in self.guilds:
            return {"success": False, "error": "Chroniclers guild not registered"}
        
        chroniclers_guild = self.guilds["chroniclers"]
        
        # Task 1: Draft report sections
        draft_task = {
            "type": "draft_report",
            "sections": ["introduction", "methodology", "results", "conclusion"],
            "research_data": research_result,
            "implementation_data": implementation_result
        }
        
        draft_result = await chroniclers_guild.execute_task(draft_task)
        
        # Task 2: Edit and format
        edit_task = {
            "type": "edit_and_format",
            "draft": draft_result.get("draft", ""),
            "format": self.config.get("output_format", "latex")
        }
        
        edit_result = await chroniclers_guild.execute_task(edit_task)
        
        return {
            "success": True,
            "draft": draft_result,
            "final_report": edit_result
        }
    
    async def monitor_progress(self) -> Dict[str, Any]:
        """Monitor progress of all guilds and detect bottlenecks"""
        current_time = datetime.now()
        
        if (current_time - self.last_progress_check).total_seconds() < self.progress_check_interval:
            return {"status": "skipped", "reason": "too_soon"}
        
        self.last_progress_check = current_time
        
        progress = {}
        bottlenecks = []
        
        for guild_name, guild in self.guilds.items():
            guild_status = guild.get_status()
            progress[guild_name] = guild_status
            
            # Detect bottlenecks: agents stuck for > 30 minutes
            if guild_status.get("state") == "executing":
                last_task_time = guild_status.get("last_task", {}).get("timestamp")
                if last_task_time:
                    last_task_dt = datetime.fromisoformat(last_task_time)
                    if (current_time - last_task_dt).total_seconds() > 1800:  # 30 minutes
                        bottlenecks.append({
                            "guild": guild_name,
                            "issue": "agent_stuck",
                            "duration_seconds": (current_time - last_task_dt).total_seconds()
                        })
        
        self.project_state["progress"] = progress
        self.project_state["blockers"] = bottlenecks
        
        if bottlenecks:
            self.logger.warning(f"⚠️ Detected {len(bottlenecks)} bottlenecks")
            # Auto-resolution could be triggered here
        
        return {
            "status": "completed",
            "progress": progress,
            "bottlenecks": bottlenecks
        }
    
    async def resolve_conflict(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflicts between guilds"""
        self.logger.info(f"⚖️ Resolving conflict: {conflict.get('type', 'unknown')}")
        
        conflict_type = conflict.get("type")
        parties = conflict.get("parties", [])
        
        # Use LLM to mediate
        llm = self.mcp_manager.get_mcp("llm_anthropic")
        
        prompt = f"""You are a project supervisor mediating a conflict between agents.

Conflict Type: {conflict_type}
Parties Involved: {', '.join(parties)}
Details: {conflict.get('details', '')}

Your task:
1. Analyze the conflict objectively
2. Propose a fair resolution
3. Explain the reasoning

Respond in JSON format with keys: resolution, reasoning, action_items"""
        
        response = await llm.execute(
            messages=[{"role": "user", "content": prompt}],
            system="You are a neutral project supervisor agent focused on practical conflict resolution."
        )
        
        try:
            resolution = json.loads(response)
        except:
            resolution = {"resolution": response, "reasoning": "LLM response parsing failed"}
        
        # Store resolution in memory
        await self.store_in_memory(
            content=json.dumps(resolution, indent=2),
            metadata={
                "type": "conflict_resolution",
                "conflict_type": conflict_type,
                "parties": parties
            },
            collection="project_artifacts"
        )
        
        return {"status": "resolved", "resolution": resolution}
    
    async def allocate_resources(self, guild_name: str, priority: str = "normal") -> bool:
        """Allocate computational resources to a guild"""
        # This is a placeholder for resource management logic
        # In production, this could manage GPU allocation, API rate limits, etc.
        
        self.project_state["resource_allocation"][guild_name] = {
            "priority": priority,
            "allocated_at": datetime.now().isoformat()
        }
        
        self.logger.info(f"Allocated {priority} priority resources to {guild_name}")
        return True
    
    def get_project_status(self) -> Dict[str, Any]:
        """Get comprehensive project status"""
        return {
            "supervisor_status": self.get_status(),
            "project_state": self.project_state,
            "guilds": {name: guild.get_status() for name, guild in self.guilds.items()},
            "timestamp": datetime.now().isoformat()
        }
