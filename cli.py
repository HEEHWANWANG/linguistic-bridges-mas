#!/usr/bin/env python3
"""
CLI Runner for Linguistic Bridges MAS
"""
import typer
import asyncio
from pathlib import Path
from rich.console import Console

app = typer.Typer(help="Linguistic Bridges Multi-Agent System CLI")
console = Console()


@app.command()
def run(
    mode: str = typer.Option("full", help="Execution mode: full, research, forge, chroniclers"),
    config: Path = typer.Option("config.yaml", help="Path to config file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Run the multi-agent system"""
    console.print(f"[bold cyan]Starting in {mode} mode...[/bold cyan]")
    
    if verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    from main import main
    asyncio.run(main())


@app.command()
def status():
    """Check system status and MCP health"""
    console.print("[bold]System Status Check[/bold]\n")
    
    # Load environment config
    from dotenv import load_dotenv
    load_dotenv()
    from utils.env_config import get_config
    
    env_config = get_config()
    
    # Check if .env exists
    env_exists = Path(".env").exists()
    console.print(f"{'✅' if env_exists else '❌'} Environment file (.env)")
    
    # Check API keys
    console.print(f"{'✅' if env_config.ANTHROPIC_API_KEY else '❌'} Anthropic API Key")
    console.print(f"{'✅' if env_config.GOOGLE_API_KEY else '⚠️ '} Google API Key (optional)")
    console.print(f"{'✅' if env_config.TAVILY_API_KEY else '⚠️ '} Tavily API Key (optional)")
    
    # Check if vector DB exists
    vdb_exists = Path(env_config.VECTOR_DB_PATH).exists()
    console.print(f"{'✅' if vdb_exists else '❌'} Vector database")
    
    # Display configuration
    console.print("\n[bold]Current Configuration:[/bold]")
    console.print(f"  Model: {env_config.DEFAULT_MODEL}")
    console.print(f"  Max Parallel Agents: {env_config.MAX_PARALLEL_AGENTS}")
    console.print(f"  Evolution Iterations: {env_config.MAX_EVOLUTION_ITERATIONS}")
    console.print(f"  Hypothesis Count: {env_config.HYPOTHESIS_GENERATION_COUNT}")
    console.print(f"  Workspace: {env_config.WORKSPACE_PATH}")
    console.print(f"  Debug Mode: {env_config.DEBUG_MODE}")
    console.print(f"  Vector DB: {env_config.VECTOR_DB_PATH}")
    
    if not env_exists:
        console.print("\n[yellow]⚠️ Create .env file with API keys (see .env.template)[/yellow]")
    
    if not env_config.ANTHROPIC_API_KEY:
        console.print("\n[red]❌ ANTHROPIC_API_KEY is required! Set it in .env file[/red]")


@app.command()
def init():
    """Initialize the system (create directories, check dependencies)"""
    console.print("[bold]Initializing system...[/bold]\n")
    
    # Create directories
    dirs = ["data", "outputs", "logs", "data/vector_db"]
    for d in dirs:
        Path(d).mkdir(exist_ok=True, parents=True)
        console.print(f"✅ Created directory: {d}")
    
    # Create .env if not exists
    if not Path(".env").exists():
        import shutil
        shutil.copy(".env.template", ".env")
        console.print("✅ Created .env file (please edit with your API keys)")
    
    console.print("\n[green]✨ Initialization complete![/green]")


@app.command()
def clean():
    """Clean temporary files and caches"""
    import shutil
    
    console.print("[bold]Cleaning temporary files...[/bold]\n")
    
    # Clean vector DB
    if typer.confirm("Remove vector database?"):
        shutil.rmtree("./data/vector_db", ignore_errors=True)
        console.print("✅ Removed vector database")
    
    # Clean logs
    if typer.confirm("Remove logs?"):
        shutil.rmtree("./logs", ignore_errors=True)
        Path("./logs").mkdir(exist_ok=True)
        console.print("✅ Cleaned logs")
    
    console.print("\n[green]✨ Cleanup complete![/green]")


if __name__ == "__main__":
    app()
