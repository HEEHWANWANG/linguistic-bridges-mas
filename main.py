"""
Linguistic Bridges Multi-Agent System - Main Entry Point
"""
import asyncio
import os
import logging
import yaml
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler

# Load environment variables
load_dotenv()

# Import environment configuration
from utils.env_config import get_config

# Get configuration
env_config = get_config()

# Setup logging with DEBUG_MODE from environment
log_level = logging.DEBUG if env_config.DEBUG_MODE else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("LinguisticBridgesMAS")
console = Console()


async def main():
    """Main execution function"""
    
    console.print("\n[bold cyan]🌉 Linguistic Bridges Multi-Agent System[/bold cyan]")
    console.print("[dim]Modeling Visual Art and Music Alignment through Language[/dim]\n")
    
    # Display configuration
    if env_config.DEBUG_MODE:
        console.print("[bold]Configuration:[/bold]")
        console.print(f"  Model: {env_config.DEFAULT_MODEL}")
        console.print(f"  Max Parallel Agents: {env_config.MAX_PARALLEL_AGENTS}")
        console.print(f"  Evolution Iterations: {env_config.MAX_EVOLUTION_ITERATIONS}")
        console.print(f"  Hypothesis Count: {env_config.HYPOTHESIS_GENERATION_COUNT}")
        console.print(f"  Workspace: {env_config.WORKSPACE_PATH}\n")
    
    # Load YAML configuration
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Override config with environment variables
    config['apis']['anthropic'].update(env_config.get_model_config())
    config['apis']['google'].update(env_config.get_model_config())
    config['agents']['supervisor'] = env_config.get_supervisor_config()
    config['agents']['research_guild'] = env_config.get_research_config()
    config['failure_recovery'] = env_config.get_failure_recovery_config()
    config['human_approval'] = env_config.get_human_approval_config()
    config['vector_db']['persist_directory'] = env_config.VECTOR_DB_PATH
    
    # Add Git/GitHub configuration
    config['git'] = {
        "repo_path": ".",
        "git_user_name": env_config.GIT_USER_NAME,
        "git_user_email": env_config.GIT_USER_EMAIL
    }
    config['github'] = env_config.get_github_config()
    
    logger.info("📋 Configuration loaded (environment variables applied)")
    
    # Initialize MCP Manager
    from mcps.mcp_manager import MCPManager
    mcp_manager = MCPManager(config)
    await mcp_manager.initialize()
    
    logger.info("🔌 MCP connections established")
    
    # Health check
    health = await mcp_manager.health_check_all()
    console.print("\n[bold]MCP Health Status:[/bold]")
    for mcp_name, status in health.items():
        status_icon = "✅" if status else "❌"
        console.print(f"  {status_icon} {mcp_name}")
    
    # Get shared memory (Vector DB)
    shared_memory = mcp_manager.get_mcp("vector_db")
    
    # Initialize Guilds
    from guilds.research_guild import ResearchGuild
    from guilds.forge_guild import ForgeGuild
    from guilds.chroniclers_guild import ChroniclersGuild
    
    research_guild = ResearchGuild(
        "ResearchGuild", "guild.research",
        config.get("agents", {}).get("research_guild", {}),
        shared_memory, mcp_manager
    )
    
    forge_guild = ForgeGuild(
        "ForgeGuild", "guild.forge",
        config.get("agents", {}).get("forge_guild", {}),
        shared_memory, mcp_manager
    )
    
    chroniclers_guild = ChroniclersGuild(
        "ChroniclersGuild", "guild.chroniclers",
        config.get("agents", {}).get("chroniclers_guild", {}),
        shared_memory, mcp_manager
    )
    
    logger.info("🏛️ Guilds initialized")
    
    # Initialize Supervisor
    from agents.supervisor import SupervisorAgent
    
    supervisor = SupervisorAgent(
        "Supervisor", "supervisor",
        config.get("agents", {}).get("supervisor", {}),
        shared_memory, mcp_manager
    )
    
    # Register guilds with supervisor
    supervisor.register_guild("research", research_guild)
    supervisor.register_guild("forge", forge_guild)
    supervisor.register_guild("chroniclers", chroniclers_guild)
    
    logger.info("👔 Supervisor ready")
    
    console.print("\n[bold green]✨ System Ready[/bold green]\n")
    
    # Start orchestration
    project_task = {
        "type": "orchestrate_project",
        "goal": "Complete Linguistic Bridges research project",
        "tracks": ["disentanglement", "mediator_function", "generation"]
    }
    
    console.print("[bold]🚀 Starting Project Orchestration[/bold]\n")
    
    try:
        result = await supervisor.execute_task(project_task)
        
        console.print("\n[bold green]✅ Project Complete![/bold green]")
        console.print(f"\nFinal Status: {result.get('status')}")
        
        # Save results
        import json
        output_path = Path("./outputs/project_results.json")
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        console.print(f"\n📄 Results saved to: {output_path}")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        logger.exception("Fatal error during orchestration")
    
    console.print("\n[dim]Shutting down...[/dim]")


if __name__ == "__main__":
    asyncio.run(main())
