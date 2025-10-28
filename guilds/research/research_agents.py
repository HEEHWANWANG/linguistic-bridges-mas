"""
Research Sub-Agents: Reflector, Ranker, Evolver, Meta-Reviewer
"""
import json
from typing import Dict, Any, List
from agents.base_agent import BaseAgent


class HypothesisReflector(BaseAgent):
    """Critically evaluates hypothesis quality, novelty, and testability"""
    
    def __init__(self, name: str, agent_id: str, config: Dict[str, Any], shared_memory: Any, mcp_manager: Any):
        super().__init__(name, agent_id, config, shared_memory)
        self.mcp_manager = mcp_manager
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return await self.reflect(task.get("hypothesis", {}))
    
    async def reflect(self, hypothesis: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on a single hypothesis"""
        llm = self.mcp_manager.get_mcp("llm_anthropic")
        
        prompt = f"""Critically evaluate this research hypothesis:

{json.dumps(hypothesis, indent=2)}

Provide structured critique on:
1. Scientific rigor (0-10)
2. Novelty (0-10)
3. Testability (0-10)
4. Potential weaknesses
5. Suggestions for improvement

Return as JSON."""
        
        response = await llm.execute(
            messages=[{"role": "user", "content": prompt}],
            system="You are a critical peer reviewer in AI research."
        )
        
        try:
            reflection = json.loads(response)
        except:
            reflection = {"critique": response, "scores": {"overall": 5}}
        
        return {"hypothesis": hypothesis, "reflection": reflection}


class HypothesisRanker(BaseAgent):
    """Ranks hypotheses through Elo-based tournament debate"""
    
    def __init__(self, name: str, agent_id: str, config: Dict[str, Any], shared_memory: Any, mcp_manager: Any):
        super().__init__(name, agent_id, config, shared_memory)
        self.mcp_manager = mcp_manager
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return await self.rank_hypotheses(
            hypotheses=task.get("hypotheses", []),
            reflections=task.get("reflections", [])
        )
    
    async def rank_hypotheses(
        self,
        hypotheses: List[Dict[str, Any]],
        reflections: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Rank hypotheses through simulated debate"""
        llm = self.mcp_manager.get_mcp("llm_anthropic")
        
        # Initialize Elo scores
        scores = {i: 1500 for i in range(len(hypotheses))}
        
        # Tournament: each hypothesis debates every other
        for i in range(len(hypotheses)):
            for j in range(i + 1, len(hypotheses)):
                debate_prompt = f"""Compare these two hypotheses and determine which is stronger:

Hypothesis A:
{json.dumps(hypotheses[i], indent=2)}
Critique A: {reflections[i].get('reflection', {}).get('critique', '')}

Hypothesis B:
{json.dumps(hypotheses[j], indent=2)}
Critique B: {reflections[j].get('reflection', {}).get('critique', '')}

Which is stronger? Respond: A, B, or TIE
Include brief reasoning."""
                
                response = await llm.execute(
                    messages=[{"role": "user", "content": debate_prompt}],
                    system="You are an impartial research judge.",
                    max_tokens=200
                )
                
                # Simple Elo update
                winner = response.strip().upper()[0]
                if winner == 'A':
                    scores[i] += 32
                    scores[j] -= 32
                elif winner == 'B':
                    scores[j] += 32
                    scores[i] -= 32
        
        # Sort by score
        ranked_indices = sorted(range(len(hypotheses)), key=lambda i: scores[i], reverse=True)
        ranked_hypotheses = [hypotheses[i] for i in ranked_indices]
        
        return {
            "ranked_hypotheses": ranked_hypotheses,
            "scores": {i: scores[i] for i in ranked_indices}
        }


class HypothesisEvolver(BaseAgent):
    """Evolves top hypotheses by combining and refining them"""
    
    def __init__(self, name: str, agent_id: str, config: Dict[str, Any], shared_memory: Any, mcp_manager: Any):
        super().__init__(name, agent_id, config, shared_memory)
        self.mcp_manager = mcp_manager
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return await self.evolve(
            hypotheses=task.get("hypotheses", []),
            meta_feedback=task.get("meta_feedback", {})
        )
    
    async def evolve(
        self,
        hypotheses: List[Dict[str, Any]],
        meta_feedback: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evolve hypotheses based on top performers and meta-review"""
        llm = self.mcp_manager.get_mcp("llm_anthropic")
        
        prompt = f"""Given these top-ranked hypotheses:

{json.dumps(hypotheses, indent=2)}

And this meta-review highlighting common issues:
{json.dumps(meta_feedback, indent=2)}

Generate {len(hypotheses)} EVOLVED hypotheses that:
1. Combine strengths of multiple input hypotheses
2. Address the common issues identified
3. Are more refined and specific
4. Maintain testability

Return as JSON array."""
        
        response = await llm.execute(
            messages=[{"role": "user", "content": prompt}],
            system="You are a research scientist synthesizing and improving hypotheses."
        )
        
        try:
            evolved = json.loads(response)
            if not isinstance(evolved, list):
                evolved = [evolved]
        except:
            evolved = hypotheses  # Fallback to original
        
        return {"evolved_hypotheses": evolved, "source_count": len(hypotheses)}


class MetaReviewer(BaseAgent):
    """Identifies common patterns and issues across all reviews"""
    
    def __init__(self, name: str, agent_id: str, config: Dict[str, Any], shared_memory: Any, mcp_manager: Any):
        super().__init__(name, agent_id, config, shared_memory)
        self.mcp_manager = mcp_manager
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return await self.review(
            hypotheses=task.get("hypotheses", []),
            reflections=task.get("reflections", [])
        )
    
    async def review(
        self,
        hypotheses: List[Dict[str, Any]],
        reflections: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Meta-review to find common issues"""
        llm = self.mcp_manager.get_mcp("llm_anthropic")
        
        prompt = f"""Analyze these hypotheses and their critiques:

{json.dumps([{'hyp': h, 'critique': r.get('reflection', {})} for h, r in zip(hypotheses, reflections)][:5], indent=2)}

Identify:
1. Common weaknesses across ALL hypotheses
2. Recurring methodological issues
3. Systematic improvements needed
4. Overall quality trends

Return as structured JSON."""
        
        response = await llm.execute(
            messages=[{"role": "user", "content": prompt}],
            system="You are a meta-analyst identifying patterns in research quality."
        )
        
        try:
            meta_review = json.loads(response)
        except:
            meta_review = {"summary": response}
        
        return meta_review
