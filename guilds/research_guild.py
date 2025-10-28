"""
Research Guild - Manages hypothesis generation, reflection, ranking, and evolution
Implements the "Generate, Debate, Evolve" workflow from AI co-scientist
"""
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from agents.base_agent import BaseAgent


class ResearchGuild(BaseAgent):
    """
    Guild coordinating all research agents for hypothesis development
    """
    
    def __init__(self, name: str, agent_id: str, config: Dict[str, Any], shared_memory: Any, mcp_manager: Any):
        super().__init__(name, agent_id, config, shared_memory)
        self.mcp_manager = mcp_manager
        self.sub_agents = {}
        self._initialize_sub_agents()
    
    def _initialize_sub_agents(self):
        """Initialize all research sub-agents"""
        from guilds.research.hypothesis_generator import HypothesisGenerator
        from guilds.research.hypothesis_reflector import HypothesisReflector
        from guilds.research.hypothesis_ranker import HypothesisRanker
        from guilds.research.hypothesis_evolver import HypothesisEvolver
        from guilds.research.meta_reviewer import MetaReviewer
        
        self.sub_agents = {
            "generator": HypothesisGenerator(
                "HypothesisGenerator", f"{self.agent_id}.generator",
                self.config, self.shared_memory, self.mcp_manager
            ),
            "reflector": HypothesisReflector(
                "HypothesisReflector", f"{self.agent_id}.reflector",
                self.config, self.shared_memory, self.mcp_manager
            ),
            "ranker": HypothesisRanker(
                "HypothesisRanker", f"{self.agent_id}.ranker",
                self.config, self.shared_memory, self.mcp_manager
            ),
            "evolver": HypothesisEvolver(
                "HypothesisEvolver", f"{self.agent_id}.evolver",
                self.config, self.shared_memory, self.mcp_manager
            ),
            "meta_reviewer": MetaReviewer(
                "MetaReviewer", f"{self.agent_id}.meta_reviewer",
                self.config, self.shared_memory, self.mcp_manager
            )
        }
        
        self.logger.info(f"Initialized {len(self.sub_agents)} research sub-agents")
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research guild task"""
        task_type = task.get("type", "unknown")
        
        if task_type == "generate_hypotheses":
            return await self._generate_hypotheses(task)
        elif task_type == "evolve_hypotheses":
            return await self._evolve_hypotheses(task)
        elif task_type == "literature_review":
            return await self._conduct_literature_review(task)
        else:
            self.logger.warning(f"Unknown task type: {task_type}")
            return {"status": "error", "message": f"Unknown task type: {task_type}"}
    
    async def _generate_hypotheses(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate initial hypotheses"""
        self.logger.info("🧠 Generating initial hypotheses")
        
        generator = self.sub_agents["generator"]
        result = await generator.generate(
            topic=task.get("topic", ""),
            focus_areas=task.get("focus_areas", []),
            num_hypotheses=task.get("num_hypotheses", 5)
        )
        
        return result
    
    async def _evolve_hypotheses(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement the Generate-Debate-Evolve loop
        """
        self.logger.info("🔄 Starting hypothesis evolution loop")
        
        initial_hypotheses = task.get("initial_hypotheses", [])
        num_rounds = task.get("num_rounds", 3)
        
        current_hypotheses = initial_hypotheses
        evolution_history = []
        
        for round_num in range(num_rounds):
            self.logger.info(f"Round {round_num + 1}/{num_rounds}")
            
            # Step 1: Reflect on hypotheses
            reflection_tasks = [
                self.sub_agents["reflector"].reflect(hypothesis)
                for hypothesis in current_hypotheses
            ]
            reflections = await asyncio.gather(*reflection_tasks)
            
            # Step 2: Rank hypotheses through debate
            ranking_result = await self.sub_agents["ranker"].rank_hypotheses(
                hypotheses=current_hypotheses,
                reflections=reflections
            )
            
            ranked_hypotheses = ranking_result.get("ranked_hypotheses", [])
            
            # Step 3: Meta-review to find common issues
            meta_review = await self.sub_agents["meta_reviewer"].review(
                hypotheses=ranked_hypotheses,
                reflections=reflections
            )
            
            # Step 4: Evolve top hypotheses
            top_hypotheses = ranked_hypotheses[:3]  # Top 3
            evolution_result = await self.sub_agents["evolver"].evolve(
                hypotheses=top_hypotheses,
                meta_feedback=meta_review
            )
            
            evolved_hypotheses = evolution_result.get("evolved_hypotheses", [])
            
            # Store round results
            round_summary = {
                "round": round_num + 1,
                "input_count": len(current_hypotheses),
                "output_count": len(evolved_hypotheses),
                "top_hypothesis": evolved_hypotheses[0] if evolved_hypotheses else None,
                "meta_review": meta_review
            }
            evolution_history.append(round_summary)
            
            # Update current hypotheses for next round
            current_hypotheses = evolved_hypotheses
            
            # Store in shared memory
            await self.store_in_memory(
                content=json.dumps(round_summary, indent=2),
                metadata={
                    "type": "evolution_round",
                    "round": round_num + 1,
                    "guild": "research"
                },
                collection="research_artifacts"
            )
        
        final_result = {
            "success": True,
            "final_hypotheses": current_hypotheses,
            "rounds_completed": num_rounds,
            "evolution_history": evolution_history
        }
        
        # Store final hypotheses
        await self.store_in_memory(
            content=json.dumps(final_result, indent=2),
            metadata={
                "type": "final_hypotheses",
                "guild": "research",
                "rounds": num_rounds
            },
            collection="research_artifacts"
        )
        
        return final_result
    
    async def _conduct_literature_review(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct literature review using arXiv and web search"""
        self.logger.info("📚 Conducting literature review")
        
        query = task.get("query", "")
        
        # Search arXiv
        arxiv_mcp = self.mcp_manager.get_mcp("arxiv")
        papers = await arxiv_mcp.execute(query=query, max_results=10)
        
        # Search web
        web_search_mcp = self.mcp_manager.get_mcp("web_search")
        web_results = await web_search_mcp.execute(query=query, max_results=5)
        
        # Synthesize findings using LLM
        llm = self.mcp_manager.get_mcp("llm_anthropic")
        
        synthesis_prompt = f"""Synthesize the following research findings:

arXiv Papers:
{json.dumps(papers[:5], indent=2)}

Web Results:
{json.dumps(web_results, indent=2)}

Provide:
1. Key themes and trends
2. Relevant methodologies
3. Gaps in current research
4. Connections to our project (music-visual art alignment)

Format as structured JSON."""
        
        synthesis = await llm.execute(
            messages=[{"role": "user", "content": synthesis_prompt}],
            system="You are a research assistant specialized in multimodal AI and computational arts."
        )
        
        result = {
            "success": True,
            "papers_found": len(papers),
            "web_results_found": len(web_results),
            "synthesis": synthesis
        }
        
        # Store in memory
        await self.store_in_memory(
            content=json.dumps(result, indent=2),
            metadata={
                "type": "literature_review",
                "query": query,
                "guild": "research"
            },
            collection="research_artifacts"
        )
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get research guild status"""
        status = super().get_status()
        status["sub_agents"] = {
            name: agent.get_status()
            for name, agent in self.sub_agents.items()
        }
        return status
