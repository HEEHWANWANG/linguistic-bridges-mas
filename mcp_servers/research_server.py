"""
Research Guild MCP Server for Claude Code
Allows interaction via @research_guild
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_servers.supervisor_server import SupervisorMCPServer
from mcp_servers.base_server import format_tool_response
from typing import Dict, Any, List


class ResearchGuildMCPServer(SupervisorMCPServer):
    """MCP Server for Research Guild"""
    
    def __init__(self):
        super().__init__()
        self.agent_name = "ResearchGuild"
    
    async def initialize_agent(self):
        """Initialize only research guild"""
        await super().initialize_agent()
        return self.guilds["research"]
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Research guild specific tools"""
        return [
            {
                "name": "generate_hypotheses",
                "description": "Generate research hypotheses for the project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Research topic",
                            "default": "music and visual art alignment through language"
                        },
                        "focus_areas": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific focus areas",
                            "default": ["disentanglement", "mediator_function", "generation"]
                        },
                        "num_hypotheses": {
                            "type": "integer",
                            "description": "Number of hypotheses to generate",
                            "default": 7
                        }
                    }
                }
            },
            {
                "name": "evolve_hypotheses",
                "description": "Run hypothesis evolution loop (Generate-Debate-Evolve)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "num_rounds": {
                            "type": "integer",
                            "description": "Number of evolution rounds",
                            "default": 3
                        }
                    }
                }
            },
            {
                "name": "literature_review",
                "description": "Conduct literature review on a topic",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for literature"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_status",
                "description": "Get research guild status",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research guild tool"""
        try:
            if tool_name == "generate_hypotheses":
                result = await self.agent_instance.execute_task({
                    "type": "generate_hypotheses",
                    "topic": arguments.get("topic", "music and visual art alignment"),
                    "focus_areas": arguments.get("focus_areas", ["disentanglement", "mediator_function", "generation"]),
                    "num_hypotheses": arguments.get("num_hypotheses", 7)
                })
                
                response = f"🧠 Hypothesis Generation Complete\n\n"
                response += f"Generated: {result.get('count', 0)} hypotheses\n"
                response += f"Papers reviewed: {result.get('papers_reviewed', 0)}\n\n"
                
                if result.get('hypotheses'):
                    response += "Top 3 Hypotheses:\n"
                    for i, hyp in enumerate(result['hypotheses'][:3], 1):
                        response += f"\n{i}. {hyp.get('statement', 'N/A')}\n"
                        response += f"   Novelty: {hyp.get('novelty_score', 0)}/10\n"
                
                return format_tool_response(response)
            
            elif tool_name == "evolve_hypotheses":
                # First generate if no hypotheses exist
                gen_result = await self.agent_instance.execute_task({
                    "type": "generate_hypotheses",
                    "topic": "music and visual art alignment",
                    "focus_areas": ["disentanglement", "mediator_function", "generation"],
                    "num_hypotheses": 7
                })
                
                # Then evolve
                result = await self.agent_instance.execute_task({
                    "type": "evolve_hypotheses",
                    "initial_hypotheses": gen_result.get('hypotheses', []),
                    "num_rounds": arguments.get("num_rounds", 3)
                })
                
                response = f"🔄 Hypothesis Evolution Complete\n\n"
                response += f"Rounds completed: {result.get('rounds_completed', 0)}\n"
                response += f"Final hypotheses: {len(result.get('final_hypotheses', []))}\n\n"
                
                if result.get('final_hypotheses'):
                    response += "Best Hypothesis:\n"
                    best = result['final_hypotheses'][0]
                    response += f"{best.get('statement', 'N/A')}\n"
                
                return format_tool_response(response)
            
            elif tool_name == "literature_review":
                result = await self.agent_instance.execute_task({
                    "type": "literature_review",
                    "query": arguments["query"]
                })
                
                response = f"📚 Literature Review\n\n"
                response += f"Papers found: {result.get('papers_found', 0)}\n"
                response += f"Web results: {result.get('web_results_found', 0)}\n\n"
                response += f"Synthesis:\n{result.get('synthesis', 'See memory for details')[:500]}...\n"
                
                return format_tool_response(response)
            
            elif tool_name == "get_status":
                status = self.agent_instance.get_status()
                
                response = f"📊 Research Guild Status\n\n"
                response += f"State: {status['state']}\n"
                response += f"Tasks completed: {status['tasks_completed']}\n\n"
                response += f"Sub-agents:\n"
                for name, agent_status in status.get('sub_agents', {}).items():
                    response += f"  • {name}: {agent_status['state']}\n"
                
                return format_tool_response(response)
            
            else:
                return format_tool_response(
                    f"❌ Unknown tool: {tool_name}",
                    is_error=True
                )
        
        except Exception as e:
            return format_tool_response(f"❌ Error: {str(e)}", is_error=True)


def main():
    server = ResearchGuildMCPServer()
    server.run()


if __name__ == "__main__":
    main()
