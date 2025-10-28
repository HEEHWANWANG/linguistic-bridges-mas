"""
Hypothesis Generator Agent - Generates initial research hypotheses
"""
import json
from typing import Dict, Any, List
from agents.base_agent import BaseAgent


class HypothesisGenerator(BaseAgent):
    """Generates initial research hypotheses based on topic and focus areas"""
    
    def __init__(self, name: str, agent_id: str, config: Dict[str, Any], shared_memory: Any, mcp_manager: Any):
        super().__init__(name, agent_id, config, shared_memory)
        self.mcp_manager = mcp_manager
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute hypothesis generation task"""
        return await self.generate(
            topic=task.get("topic", ""),
            focus_areas=task.get("focus_areas", []),
            num_hypotheses=task.get("num_hypotheses", 5)
        )
    
    async def generate(
        self,
        topic: str,
        focus_areas: List[str],
        num_hypotheses: int = 5
    ) -> Dict[str, Any]:
        """
        Generate research hypotheses
        
        Args:
            topic: Main research topic
            focus_areas: Specific areas to focus on
            num_hypotheses: Number of hypotheses to generate
            
        Returns:
            Dictionary with generated hypotheses
        """
        self.state = "generating"
        self.logger.info(f"Generating {num_hypotheses} hypotheses for: {topic}")
        
        # Search for relevant literature first
        arxiv_mcp = self.mcp_manager.get_mcp("arxiv")
        papers = await arxiv_mcp.execute(query=topic, max_results=10)
        
        web_search_mcp = self.mcp_manager.get_mcp("web_search")
        web_results = await web_search_mcp.execute(query=topic, max_results=5)
        
        # Retrieve existing hypotheses from memory to avoid duplication
        existing_hypotheses = await self.retrieve_from_memory(
            query=topic,
            n_results=10,
            collection="research_artifacts",
            filter_metadata={"type": "hypothesis"}
        )
        
        # Generate hypotheses using LLM
        llm = self.mcp_manager.get_mcp("llm_anthropic")
        
        prompt = f"""You are a research scientist generating novel hypotheses for a multimodal AI project.

Project: {topic}
Focus Areas: {', '.join(focus_areas)}

Recent Literature (arXiv):
{json.dumps([{'title': p['title'], 'summary': p['summary'][:200]} for p in papers[:5]], indent=2)}

Existing Hypotheses (to avoid duplication):
{json.dumps(existing_hypotheses.get('documents', [[]])[0][:5], indent=2)}

Generate {num_hypotheses} NOVEL, TESTABLE hypotheses that:
1. Are specific and measurable
2. Build on existing literature but introduce new angles
3. Address the focus areas: {', '.join(focus_areas)}
4. Are feasible to test within a research project

For each hypothesis, provide:
- statement: Clear hypothesis statement
- rationale: Why this is worth testing
- testability: How it can be tested
- novelty_score: 0-10 score for novelty
- expected_impact: Potential impact if proven

Return as JSON array of hypothesis objects."""
        
        response = await llm.execute(
            messages=[{"role": "user", "content": prompt}],
            system="You are a creative research scientist specializing in multimodal AI, computational arts, and cross-modal learning."
        )
        
        try:
            hypotheses = json.loads(response)
            if not isinstance(hypotheses, list):
                hypotheses = [hypotheses]
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse JSON, using fallback")
            hypotheses = [{
                "statement": response[:500],
                "rationale": "Generated from LLM response",
                "testability": "To be determined",
                "novelty_score": 5,
                "expected_impact": "To be evaluated"
            }]
        
        # Store each hypothesis in memory
        for i, hypothesis in enumerate(hypotheses):
            await self.store_in_memory(
                content=json.dumps(hypothesis, indent=2),
                metadata={
                    "type": "hypothesis",
                    "topic": topic,
                    "focus_areas": ",".join(focus_areas),
                    "generation_method": "initial",
                    "hypothesis_id": f"hyp_{i}_{hash(hypothesis['statement'])}"
                },
                collection="research_artifacts"
            )
        
        self.state = "idle"
        result = {
            "success": True,
            "hypotheses": hypotheses,
            "count": len(hypotheses),
            "papers_reviewed": len(papers)
        }
        
        self.log_task({"type": "generate_hypotheses"}, result)
        return result
