"""
Base MCP Server for Claude Code integration
Allows direct communication with agents via @mentions
"""
import asyncio
import json
import sys
import logging
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


class BaseMCPServer(ABC):
    """Base class for MCP servers that expose agents to Claude Code"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.agent_instance = None
        self.logger = logging.getLogger(f"MCP.{agent_name}")
        logging.basicConfig(level=logging.INFO)
    
    @abstractmethod
    async def initialize_agent(self) -> Any:
        """Initialize the agent instance"""
        pass
    
    @abstractmethod
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools for this agent"""
        pass
    
    async def handle_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP protocol request"""
        if method == "tools/list":
            return {
                "tools": self.get_available_tools()
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            return await self.call_tool(tool_name, arguments)
        else:
            return {"error": f"Unknown method: {method}"}
    
    @abstractmethod
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call"""
        pass
    
    def run(self):
        """Run the MCP server"""
        asyncio.run(self._run_async())
    
    async def _run_async(self):
        """Async server loop"""
        # Initialize agent
        self.agent_instance = await self.initialize_agent()
        self.logger.info(f"🚀 {self.agent_name} MCP Server started")
        
        # Main loop - read JSON-RPC from stdin, write to stdout
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line)
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")
                
                # Handle request
                result = await self.handle_request(method, params)
                
                # Send response
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
                
                print(json.dumps(response))
                sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON: {e}")
            except Exception as e:
                self.logger.error(f"Error handling request: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request_id if 'request_id' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()


def format_tool_response(content: str, is_error: bool = False) -> Dict[str, Any]:
    """Format tool response for MCP protocol"""
    return {
        "content": [
            {
                "type": "text",
                "text": content
            }
        ],
        "isError": is_error
    }
