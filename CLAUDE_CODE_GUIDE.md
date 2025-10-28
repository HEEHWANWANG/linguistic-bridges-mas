# Claude Code Integration Guide

## 🎯 Overview

Version 4.0 enables direct interaction with all agents through Claude Code's CLI interface using `@mentions`. This allows you to chat directly with the Supervisor, Research Guild, Forge Guild, and more!

## 🚀 Quick Start

### Step 1: Configure MCP Servers

Copy the MCP configuration to your Claude Code config directory:

**macOS/Linux:**
```bash
# Create config directory if it doesn't exist
mkdir -p ~/.config/claude-code

# Copy MCP configuration
cp mcp_config.json ~/.config/claude-code/mcp_config.json
```

**Windows:**
```powershell
# Create config directory
New-Item -Path "$env:APPDATA\claude-code" -ItemType Directory -Force

# Copy configuration
Copy-Item mcp_config.json "$env:APPDATA\claude-code\mcp_config.json"
```

### Step 2: Update Configuration Paths

Edit the copied `mcp_config.json` to use absolute paths:

```json
{
  "mcpServers": {
    "linguistic-bridges-supervisor": {
      "command": "python",
      "args": ["-m", "mcp_servers.supervisor_server"],
      "cwd": "/absolute/path/to/linguistic-bridges-mas",
      "env": {
        "PYTHONPATH": "/absolute/path/to/linguistic-bridges-mas"
      }
    }
  }
}
```

Replace `/absolute/path/to/linguistic-bridges-mas` with your actual project path.

### Step 3: Start Claude Code

```bash
cd /path/to/your/research/project
claude-code
```

Claude Code will automatically load the MCP servers!

## 💬 Usage Examples

### Talk to Supervisor

```
You: @supervisor start_project with goal "Test hypothesis evolution system"

Supervisor: 🚀 Project Started!

Status: success
Phase: research

The system is now working on your research project.
Use @supervisor get_project_status to check progress.
```

### Check Project Status

```
You: @supervisor get_project_status

Supervisor: 📊 Project Status

Phase: implementation
Progress: {'research': {...}, 'forge': {...}}

Guilds:
  • research: idle
  • forge: executing
  • chroniclers: idle
```

### Generate Research Hypotheses

```
You: @research_guild generate_hypotheses with topic "multimodal learning" and num_hypotheses 5

Research Guild: 🧠 Hypothesis Generation Complete

Generated: 5 hypotheses
Papers reviewed: 10

Top 3 Hypotheses:

1. Disentangled representations in shared latent space enable...
   Novelty: 8/10

2. Cross-modal attention mechanisms can learn...
   Novelty: 7/10

3. Emotion vectors mediate between structure and style...
   Novelty: 9/10
```

### Evolve Hypotheses

```
You: @research_guild evolve_hypotheses with num_rounds 3

Research Guild: 🔄 Hypothesis Evolution Complete

Rounds completed: 3
Final hypotheses: 5

Best Hypothesis:
Emotion emerges as a compositional function of structure and style...
```

### Implement Research Track

```
You: @forge implement_track with track_id 1 and track_name "disentanglement"

Forge Guild: ✅ implement_track: Track 1 implementation complete (committed to Git)
```

### Commit Code Changes

```
You: @version_control commit_changes with description "Added data preprocessing pipeline"

Version Control: ✅ [user] updated: Added data preprocessing pipeline
```

### Create Experiment Branch

```
You: @version_control create_experiment_branch with experiment_name "ablation-study"

Version Control: ✅ Created experiment branch: linguistic-bridges/ablation-study-20251028-150230
```

### Draft Research Report

```
You: @chroniclers draft_report

Chroniclers Guild: ✅ draft_report: completed
```

## 🛠️ Available Agents

### @supervisor
**Main orchestrator for the entire project**

Tools:
- `start_project` - Start full research project
- `get_project_status` - Check overall status
- `monitor_progress` - Detect bottlenecks
- `resolve_conflict` - Mediate between guilds
- `assign_task_to_guild` - Direct task to specific guild

### @research_guild
**Research and hypothesis development**

Tools:
- `generate_hypotheses` - Create initial hypotheses
- `evolve_hypotheses` - Run evolution loop
- `literature_review` - Search academic papers
- `get_status` - Check research status

### @forge
**Code implementation and experiments**

Tools:
- `setup_data_pipeline` - Load datasets
- `implement_track` - Implement Tracks 1-3
- `run_evaluation` - Run metrics
- `get_status` - Check implementation status

### @chroniclers
**Documentation and reports**

Tools:
- `draft_report` - Write report sections
- `edit_and_format` - Format to LaTeX/Markdown
- `get_status` - Check writing status

### @version_control
**Git and GitHub operations**

Tools:
- `commit_changes` - Commit to Git
- `create_experiment_branch` - New branch
- `push_changes` - Push to GitHub
- `get_status` - Repository status

## 🎓 Advanced Usage

### Multi-Agent Collaboration

Have multiple agents work together:

```
You: @supervisor I want to test a new hypothesis about emotion vectors.
     Can you coordinate the research and implementation?

Supervisor: I'll coordinate this for you!

     @research_guild please generate hypotheses focused on emotion vectors

     @forge once we have the hypotheses, implement Track 2

     @version_control create an experiment branch for this
```

### Iterative Development

```
You: @research_guild generate some hypotheses about cross-modal alignment

Research Guild: [generates 7 hypotheses]

You: @research_guild evolve these for 5 rounds to refine them

Research Guild: [runs evolution]

You: @forge implement the best hypothesis as Track 1

Forge Guild: [implements and commits]

You: @version_control push the changes

Version Control: [requests approval and pushes]
```

### Debugging

```
You: @supervisor monitor_progress

Supervisor: ⚠️ Bottlenecks detected:
  • forge: agent_stuck (duration: 1800s)

You: @forge what's the issue?

Forge Guild: Track 2 implementation failed due to GPU OOM

You: @supervisor resolve_conflict between forge and research about GPU requirements

Supervisor: [mediates and provides solution]
```

## 🔧 Configuration

### Custom MCP Server Paths

If you have a custom project structure:

```json
{
  "mcpServers": {
    "my-supervisor": {
      "command": "python",
      "args": ["-m", "mcp_servers.supervisor_server"],
      "cwd": "/my/custom/path",
      "env": {
        "PYTHONPATH": "/my/custom/path",
        "ANTHROPIC_API_KEY": "your-key-here"
      }
    }
  }
}
```

### Environment Variables

Pass environment variables to MCP servers:

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-...",
    "DEBUG_MODE": "true",
    "MAX_EVOLUTION_ITERATIONS": "5"
  }
}
```

## 🐛 Troubleshooting

### MCP Server Not Loading

```bash
# Check if Python can import the module
cd /path/to/linguistic-bridges-mas
python -m mcp_servers.supervisor_server --help

# Check logs
cat ~/.config/claude-code/mcp_server.log
```

### Agent Not Responding

```
You: @supervisor get_project_status

# If no response, check if MCP server is running:
ps aux | grep supervisor_server
```

### Import Errors

```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check PYTHONPATH
echo $PYTHONPATH
```

## 💡 Pro Tips

1. **Tab Completion**: Type `@` to see all available agents
2. **Help**: Ask any agent "what can you do?" to see capabilities
3. **Status Checks**: Regularly use `get_status` tools to monitor progress
4. **Batch Operations**: Supervisor can coordinate multiple guilds at once
5. **Version Control**: Always create experiment branches for new ideas

## 📚 Examples

### Complete Research Workflow

```bash
# Start Claude Code
claude-code

# Inside Claude Code:
You: @supervisor I need to run the full Linguistic Bridges research project

Supervisor: Starting project...
[Coordinates Research → Forge → Chroniclers]

You: @supervisor get_project_status
[Check progress at any time]

You: @version_control get_status
[See what's been committed]

You: @chroniclers draft_report
[Get final report when ready]
```

### Quick Hypothesis Test

```bash
You: @research_guild generate_hypotheses with topic "audio-visual alignment" and num_hypotheses 3

Research Guild: [generates 3 hypotheses]

You: These look good. @forge can you implement the first one as a quick prototype?

Forge Guild: [implements basic version]

You: @version_control commit this as "prototype for audio-visual alignment"

Version Control: ✅ Committed
```

### Collaborative Mode

Work with Claude Code to iterate:

```
You: What's the current hypothesis quality?

You: @research_guild get_status

Research Guild: [shows status]

You: Hmm, novelty scores are low. Let's evolve them more.

You: @research_guild evolve_hypotheses with num_rounds 5

Research Guild: [evolves hypotheses]

You: Much better! Now implement this.

You: @forge implement_track with track_id 1

Forge Guild: [implements]
```

## 🎯 Best Practices

1. **Always check status** before starting new tasks
2. **Use version control** for every major change
3. **Let supervisor coordinate** complex multi-guild tasks
4. **Monitor progress** during long-running operations
5. **Create branches** for experiments
6. **Commit frequently** with descriptive messages

## 📖 Further Reading

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- See `SYSTEM_OVERVIEW.md` for architecture details

---

**Version**: 4.0  
**Updated**: October 28, 2025  
**Compatibility**: Claude Code 1.0+
