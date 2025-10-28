"""
Supervisor MCP Server for Claude Code
Allows interaction with Supervisor agent via @supervisor
"""
import os
import sys
import yaml
import asyncio
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_servers.base_server import BaseMCPServer, format_tool_response
from utils.env_config import get_config


class SupervisorMCPServer(BaseMCPServer):
    """MCP Server for Supervisor Agent"""
    
    def __init__(self):
        super().__init__("Supervisor")
        self.mcp_manager = None
        self.guilds = {}
    
    async def initialize_agent(self):
        """Initialize supervisor and all guilds"""
        # Load environment
        load_dotenv()
        env_config = get_config()
        
        # Load YAML config
        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Override with env vars
        config['apis']['anthropic'].update(env_config.get_model_config())
        config['agents']['supervisor'] = env_config.get_supervisor_config()
        config['agents']['research_guild'] = env_config.get_research_config()
        config['git'] = {
            "repo_path": ".",
            "git_user_name": env_config.GIT_USER_NAME,
            "git_user_email": env_config.GIT_USER_EMAIL
        }
        config['github'] = env_config.get_github_config()
        
        # Initialize MCP Manager
        from mcps.mcp_manager import MCPManager
        self.mcp_manager = MCPManager(config)
        await self.mcp_manager.initialize()
        
        shared_memory = self.mcp_manager.get_mcp("vector_db")
        
        # Initialize Guilds
        from guilds.research_guild import ResearchGuild
        from guilds.forge_guild import ForgeGuild
        from guilds.chroniclers_guild import ChroniclersGuild
        
        self.guilds["research"] = ResearchGuild(
            "ResearchGuild", "guild.research",
            config.get("agents", {}).get("research_guild", {}),
            shared_memory, self.mcp_manager
        )
        
        self.guilds["forge"] = ForgeGuild(
            "ForgeGuild", "guild.forge",
            config.get("agents", {}).get("forge_guild", {}),
            shared_memory, self.mcp_manager
        )
        
        self.guilds["chroniclers"] = ChroniclersGuild(
            "ChroniclersGuild", "guild.chroniclers",
            config.get("agents", {}).get("chroniclers_guild", {}),
            shared_memory, self.mcp_manager
        )
        
        # Initialize Supervisor
        from agents.supervisor import SupervisorAgent
        
        supervisor = SupervisorAgent(
            "Supervisor", "supervisor",
            config.get("agents", {}).get("supervisor", {}),
            shared_memory, self.mcp_manager
        )
        
        # Register guilds
        supervisor.register_guild("research", self.guilds["research"])
        supervisor.register_guild("forge", self.guilds["forge"])
        supervisor.register_guild("chroniclers", self.guilds["chroniclers"])
        
        self.logger.info("✅ Supervisor initialized with all guilds")
        return supervisor
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """List of tools available to Claude Code"""
        return [
            {
                "name": "start_project",
                "description": "Start the full Linguistic Bridges research project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "goal": {
                            "type": "string",
                            "description": "Project goal description",
                            "default": "Complete Linguistic Bridges research project"
                        }
                    }
                }
            },
            {
                "name": "get_project_status",
                "description": "Get current status of the project and all guilds",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "monitor_progress",
                "description": "Check progress and detect any bottlenecks",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "resolve_conflict",
                "description": "Resolve a conflict between guilds",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "conflict_type": {
                            "type": "string",
                            "description": "Type of conflict"
                        },
                        "parties": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Guilds involved in conflict"
                        },
                        "details": {
                            "type": "string",
                            "description": "Conflict details"
                        }
                    },
                    "required": ["conflict_type", "parties", "details"]
                }
            },
            {
                "name": "assign_task_to_guild",
                "description": "Assign a specific task to a guild (research, forge, chroniclers)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "guild": {
                            "type": "string",
                            "enum": ["research", "forge", "chroniclers"],
                            "description": "Target guild"
                        },
                        "task": {
                            "type": "object",
                            "description": "Task details"
                        }
                    },
                    "required": ["guild", "task"]
                }
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute supervisor tool"""
        try:
            if tool_name == "start_project":
                result = await self.agent_instance.orchestrate_project({
                    "goal": arguments.get("goal", "Complete Linguistic Bridges research project"),
                    "tracks": ["disentanglement", "mediator_function", "generation"]
                })
                
                return format_tool_response(
                    f"🚀 Project Started!\n\n"
                    f"Status: {result.get('status')}\n"
                    f"Phase: {self.agent_instance.project_state.get('phase')}\n\n"
                    f"The system is now working on your research project. "
                    f"Use @supervisor get_project_status to check progress."
                )
            
            elif tool_name == "get_project_status":
                status = self.agent_instance.get_project_status()
                
                status_text = f"📊 Project Status\n\n"
                status_text += f"Phase: {status['project_state']['phase']}\n"
                status_text += f"Progress: {status['project_state']['progress']}\n\n"
                status_text += f"Guilds:\n"
                for guild_name, guild_status in status['guilds'].items():
                    status_text += f"  • {guild_name}: {guild_status['state']}\n"
                
                if status['project_state'].get('blockers'):
                    status_text += f"\n⚠️ Blockers: {len(status['project_state']['blockers'])}\n"
                
                return format_tool_response(status_text)
            
            elif tool_name == "monitor_progress":
                result = await self.agent_instance.monitor_progress()
                
                response = f"🔍 Progress Check\n\n"
                if result['status'] == 'skipped':
                    response += "Too soon since last check. Try again later.\n"
                else:
                    response += f"Progress:\n"
                    for guild, prog in result.get('progress', {}).items():
                        response += f"  • {guild}: {prog['state']}\n"
                    
                    if result.get('bottlenecks'):
                        response += f"\n⚠️ Bottlenecks detected:\n"
                        for bottleneck in result['bottlenecks']:
                            response += f"  • {bottleneck['guild']}: {bottleneck['issue']}\n"
                
                return format_tool_response(response)
            
            elif tool_name == "resolve_conflict":
                result = await self.agent_instance.resolve_conflict({
                    "type": arguments["conflict_type"],
                    "parties": arguments["parties"],
                    "details": arguments.get("details", "")
                })
                
                return format_tool_response(
                    f"⚖️ Conflict Resolution\n\n"
                    f"Status: {result['status']}\n"
                    f"Resolution: {result['resolution'].get('resolution', 'See details')}\n"
                )
            
            elif tool_name == "assign_task_to_guild":
                guild_name = arguments["guild"]
                task = arguments["task"]
                
                if guild_name not in self.guilds:
                    return format_tool_response(
                        f"❌ Guild '{guild_name}' not found",
                        is_error=True
                    )
                
                guild = self.guilds[guild_name]
                result = await guild.execute_task(task)
                
                return format_tool_response(
                    f"✅ Task assigned to {guild_name} guild\n\n"
                    f"Result: {result.get('status', 'completed')}\n"
                )
            
            else:
                return format_tool_response(
                    f"❌ Unknown tool: {tool_name}",
                    is_error=True
                )
        
        except Exception as e:
            self.logger.error(f"Tool execution failed: {e}")
            return format_tool_response(
                f"❌ Error: {str(e)}",
                is_error=True
            )


def main():
    """Entry point for supervisor MCP server"""
    server = SupervisorMCPServer()
    server.run()


if __name__ == "__main__":
    main()
