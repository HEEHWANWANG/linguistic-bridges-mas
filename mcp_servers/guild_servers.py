"""
Forge, Chroniclers, and Version Control MCP Servers
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_servers.supervisor_server import SupervisorMCPServer
from mcp_servers.base_server import format_tool_response
from typing import Dict, Any, List


class ForgeMCPServer(SupervisorMCPServer):
    """MCP Server for Forge Guild"""
    
    def __init__(self):
        super().__init__()
        self.agent_name = "ForgeGuild"
    
    async def initialize_agent(self):
        await super().initialize_agent()
        return self.guilds["forge"]
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "setup_data_pipeline",
                "description": "Setup data loading pipeline for ArtEmis and SDD",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "implement_track",
                "description": "Implement a research track (1: Disentanglement, 2: Mediator, 3: Generation)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "track_id": {"type": "integer", "enum": [1, 2, 3]},
                        "track_name": {"type": "string"}
                    },
                    "required": ["track_id"]
                }
            },
            {
                "name": "run_evaluation",
                "description": "Run evaluation metrics on implemented tracks",
                "inputSchema": {"type": "object", "properties": {}}
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = await self.agent_instance.execute_task({
                "type": tool_name,
                **arguments
            })
            return format_tool_response(f"✅ {tool_name}: {result.get('status', 'completed')}")
        except Exception as e:
            return format_tool_response(f"❌ Error: {e}", is_error=True)


class ChroniclersMCPServer(SupervisorMCPServer):
    """MCP Server for Chroniclers Guild"""
    
    def __init__(self):
        super().__init__()
        self.agent_name = "ChroniclersGuild"
    
    async def initialize_agent(self):
        await super().initialize_agent()
        return self.guilds["chroniclers"]
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "draft_report",
                "description": "Draft research report sections",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "sections": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["introduction", "methodology", "results", "conclusion"]
                        }
                    }
                }
            },
            {
                "name": "edit_and_format",
                "description": "Edit and format report to LaTeX/Markdown",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "format": {"type": "string", "enum": ["latex", "markdown"], "default": "latex"}
                    }
                }
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = await self.agent_instance.execute_task({
                "type": tool_name,
                **arguments
            })
            return format_tool_response(f"✅ {tool_name}: {result.get('status', 'completed')}")
        except Exception as e:
            return format_tool_response(f"❌ Error: {e}", is_error=True)


class VersionControlMCPServer(SupervisorMCPServer):
    """MCP Server for Version Control Agent"""
    
    def __init__(self):
        super().__init__()
        self.agent_name = "VersionControl"
    
    async def initialize_agent(self):
        await super().initialize_agent()
        return self.guilds["forge"].sub_agents["version_control"]
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "commit_changes",
                "description": "Commit changes to Git repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent_name": {"type": "string", "default": "user"},
                        "action": {"type": "string", "default": "updated"},
                        "description": {"type": "string", "required": True}
                    }
                }
            },
            {
                "name": "create_experiment_branch",
                "description": "Create a new branch for an experiment",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "experiment_name": {"type": "string", "required": True}
                    }
                }
            },
            {
                "name": "push_changes",
                "description": "Push changes to GitHub",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_status",
                "description": "Get repository status",
                "inputSchema": {"type": "object", "properties": {}}
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = await self.agent_instance.execute_task({
                "type": tool_name,
                **arguments
            })
            
            if result.get("success"):
                return format_tool_response(f"✅ {result.get('message', 'Operation completed')}")
            else:
                return format_tool_response(f"❌ {result.get('error', 'Operation failed')}", is_error=True)
        
        except Exception as e:
            return format_tool_response(f"❌ Error: {e}", is_error=True)


# Entry points for each server
def main_forge():
    server = ForgeMCPServer()
    server.run()


def main_chroniclers():
    server = ChroniclersMCPServer()
    server.run()


def main_version_control():
    server = VersionControlMCPServer()
    server.run()


if __name__ == "__main__":
    import sys
    if "forge" in sys.argv[0]:
        main_forge()
    elif "chroniclers" in sys.argv[0]:
        main_chroniclers()
    elif "version" in sys.argv[0]:
        main_version_control()
