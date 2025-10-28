"""
Chroniclers Guild - Handles documentation and report writing
"""
import json
from typing import Dict, Any
from agents.base_agent import BaseAgent


class ChroniclersGuild(BaseAgent):
    """Guild for writing documentation and reports"""
    
    def __init__(self, name: str, agent_id: str, config: Dict[str, Any], shared_memory: Any, mcp_manager: Any):
        super().__init__(name, agent_id, config, shared_memory)
        self.mcp_manager = mcp_manager
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute chroniclers guild task"""
        task_type = task.get("type")
        
        if task_type == "draft_report":
            return await self._draft_report(task)
        elif task_type == "edit_and_format":
            return await self._edit_and_format(task)
        else:
            self.logger.warning(f"Unknown task: {task_type}")
            return {"status": "error", "message": f"Unknown task: {task_type}"}
    
    async def _draft_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Draft report sections"""
        self.logger.info("📝 Drafting report")
        
        sections = task.get("sections", [])
        research_data = task.get("research_data", {})
        implementation_data = task.get("implementation_data", {})
        
        # Retrieve relevant artifacts from memory
        research_artifacts = await self.retrieve_from_memory(
            query="final hypotheses research findings",
            n_results=10,
            collection="research_artifacts"
        )
        
        code_artifacts = await self.retrieve_from_memory(
            query="implementation results code",
            n_results=10,
            collection="code_artifacts"
        )
        
        # Generate report using LLM with RAG
        llm = self.mcp_manager.get_mcp("llm_anthropic")
        
        prompt = f"""Write a research report with these sections: {', '.join(sections)}

Research Findings:
{json.dumps(research_data, indent=2)[:1000]}

Implementation Results:
{json.dumps(implementation_data, indent=2)[:1000]}

Memory Context:
{json.dumps(research_artifacts['documents'][0][:3], indent=2)[:500]}

Write in academic style, include citations, and structure properly."""
        
        draft = await llm.execute(
            messages=[{"role": "user", "content": prompt}],
            system="You are an academic writer specializing in AI research papers."
        )
        
        # Store draft
        await self.store_in_memory(
            content=draft,
            metadata={
                "type": "report_draft",
                "sections": ",".join(sections)
            },
            collection="documentation"
        )
        
        return {
            "success": True,
            "draft": draft,
            "sections_completed": sections
        }
    
    async def _edit_and_format(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Edit and format report"""
        self.logger.info("✍️ Editing and formatting")
        
        draft = task.get("draft", "")
        output_format = task.get("format", "latex")
        
        llm = self.mcp_manager.get_mcp("llm_anthropic")
        
        prompt = f"""Edit and format this draft into {output_format}:

{draft}

Requirements:
1. Fix grammar and style
2. Ensure academic tone
3. Add proper formatting
4. Include bibliography section"""
        
        formatted = await llm.execute(
            messages=[{"role": "user", "content": prompt}],
            system="You are a copy editor for academic publications."
        )
        
        return {
            "success": True,
            "formatted_report": formatted,
            "format": output_format
        }
