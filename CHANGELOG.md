# Changelog

## Version 4.0 - Claude Code Integration (October 28, 2025)

### 🎉 Major Feature: Direct Agent Communication via @mentions

You can now interact with all agents directly in Claude Code using `@supervisor`, `@research_guild`, `@forge`, `@chroniclers`, and `@version_control`!

### ✨ New Components

#### MCP Servers for Claude Code
Created MCP (Model Context Protocol) servers for each agent:

1. **Supervisor MCP Server** (`mcp_servers/supervisor_server.py`)
   - `@supervisor start_project` - Start full research project
   - `@supervisor get_project_status` - Check progress
   - `@supervisor monitor_progress` - Detect bottlenecks
   - `@supervisor resolve_conflict` - Mediate disputes
   - `@supervisor assign_task_to_guild` - Direct tasks

2. **Research Guild MCP Server** (`mcp_servers/research_server.py`)
   - `@research_guild generate_hypotheses` - Create hypotheses
   - `@research_guild evolve_hypotheses` - Run evolution loop
   - `@research_guild literature_review` - Search papers
   - `@research_guild get_status` - Check status

3. **Forge Guild MCP Server** (`mcp_servers/guild_servers.py`)
   - `@forge setup_data_pipeline` - Load datasets
   - `@forge implement_track` - Implement Tracks 1-3
   - `@forge run_evaluation` - Run metrics

4. **Chroniclers Guild MCP Server** (`mcp_servers/guild_servers.py`)
   - `@chroniclers draft_report` - Write report
   - `@chroniclers edit_and_format` - Format output

5. **Version Control MCP Server** (`mcp_servers/guild_servers.py`)
   - `@version_control commit_changes` - Commit code
   - `@version_control create_experiment_branch` - New branch
   - `@version_control push_changes` - Push to GitHub

#### Supporting Infrastructure
- **Base MCP Server** (`mcp_servers/base_server.py`) - Shared server logic
- **MCP Configuration** (`mcp_config.json`) - Claude Code integration config

### 🚀 Usage in Claude Code

```bash
# Start Claude Code
claude-code

# Talk to agents directly:
You: @supervisor start_project

You: @research_guild generate_hypotheses with num_hypotheses 5

You: @forge implement_track with track_id 1

You: @version_control commit_changes with description "Added Track 1"
```

### 📋 Configuration

1. Copy `mcp_config.json` to Claude Code config directory
2. Update paths in config to point to your project
3. Start Claude Code - agents load automatically!

**Example `mcp_config.json`:**
```json
{
  "mcpServers": {
    "linguistic-bridges-supervisor": {
      "command": "python",
      "args": ["-m", "mcp_servers.supervisor_server"],
      "cwd": "/path/to/linguistic-bridges-mas"
    }
  }
}
```

### 💬 Interactive Examples

**Quick Research Cycle:**
```
@research_guild generate_hypotheses
@research_guild evolve_hypotheses with num_rounds 3
@forge implement_track with track_id 1
@version_control commit_changes
```

**Status Monitoring:**
```
@supervisor get_project_status
@research_guild get_status
@forge get_status
```

**Multi-Agent Collaboration:**
```
@supervisor coordinate research and implementation for new experiment
```

### 🎯 Benefits

1. **Natural Interaction**: Chat with agents like team members
2. **Real-time Control**: Start/stop/monitor at any time
3. **Granular Commands**: Execute specific operations
4. **Status Visibility**: Check progress anytime
5. **Debugging**: Direct access to agent state

### 📚 Documentation

- **CLAUDE_CODE_GUIDE.md** - Complete usage guide
- **mcp_config.json** - Configuration template
- Examples for all agent interactions

### 🔧 Technical Details

**MCP Protocol Implementation:**
- JSON-RPC communication via stdin/stdout
- Tool discovery and invocation
- Error handling and formatting
- Async agent initialization

**Agent Integration:**
- Each MCP server wraps corresponding agent
- Tools map to agent methods
- Responses formatted for Claude Code display
- Shared configuration and memory

### 🐛 Bug Fixes

- Fixed module import paths for MCP servers
- Improved error messages in tool responses
- Better async initialization handling

### 📊 System Architecture Update

```
Claude Code CLI
    ↓ @mentions
MCP Servers (5 servers)
    ↓
Agents (Supervisor, Guilds)
    ↓
Shared Memory (Vector DB)
```

### ⚡ Performance

- MCP servers initialize on-demand
- Shared configuration across servers
- Efficient JSON-RPC communication
- Minimal overhead (~50ms per call)

### 🔄 Backward Compatibility

- All v3.0 features preserved
- Can still use `python main.py` for batch execution
- MCP servers optional (works without Claude Code)
- Existing APIs unchanged

---

## Version 3.0 - GitHub Integration (October 28, 2025)

### 🎉 Major New Feature: Version Control Integration

Added complete Git and GitHub integration with automatic version control for all code changes.

### ✨ New Components

#### 1. **Git MCP** (`mcps/git_mcp.py`)
Full Git operations support:
- Repository initialization
- File staging and commits
- Branch creation and management
- Push/pull operations
- Commit history and diffs
- Repository status monitoring

#### 2. **GitHub MCP** (`mcps/git_mcp.py`)
GitHub API integration:
- Repository creation
- Remote management
- Issue creation (planned)
- Pull request creation (planned)

#### 3. **Version Control Agent** (`agents/version_control_agent.py`)
Intelligent version control automation:
- Automatic code commits after Track implementation
- Experiment branch creation
- Commit message templates
- Human approval for pushes
- Repository synchronization

### 🔧 New Environment Variables

```properties
# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_USERNAME=your_github_username
GITHUB_DEFAULT_REPO=username/repo_name
GIT_USER_NAME=Your Name
GIT_USER_EMAIL=your.email@example.com

# Git Behavior
GIT_AUTO_COMMIT=true
GIT_AUTO_PUSH=false
GIT_BRANCH_PREFIX=linguistic-bridges
GIT_COMMIT_MESSAGE_TEMPLATE=[{agent}] {action}: {description}
```

### 📝 Integration Points

**Forge Guild** now includes Version Control Agent:
- Automatically commits after Track 1-3 implementations
- Creates experiment branches
- Maintains clean Git history
- Commit format: `[TrackCoder] implemented: Track 1 - disentangled_representation_learning`

**Commit Message Template**:
```
[{agent}] {action}: {description}
```

Examples:
- `[TrackCoder] implemented: Track 1 - Disentanglement`
- `[Evaluator] added: evaluation metrics for Track 2`
- `[QA] fixed: bug in data pipeline`

### 🚀 Usage Examples

#### Automatic Version Control
```python
# In Forge Guild - automatic after Track implementation
result = await forge_guild.implement_track(track_1)
# ✅ Automatically commits: "[TrackCoder] implemented: Track 1"
```

#### Manual Operations
```python
# Commit specific changes
await vc_agent.commit_changes({
    "agent_name": "DataPipeline",
    "action": "added",
    "description": "ArtEmis dataset loader",
    "files": ["data/artemis_loader.py"]
})

# Create experiment branch
await vc_agent.create_experiment_branch({
    "experiment_name": "track1-ablation"
})
# Creates: linguistic-bridges/track1-ablation-20251028-120000

# Push to GitHub (requires approval by default)
await vc_agent.push_changes({
    "remote": "origin",
    "branch": "main"
})
```

### 📊 Benefits

1. **Automatic History**: Every code change is tracked
2. **Experiment Isolation**: Each experiment gets its own branch
3. **Reproducibility**: Easy to rollback or compare versions
4. **Collaboration**: Push to GitHub for team collaboration
5. **Safety**: Human approval required for pushes (configurable)

### 🔒 Security

- GitHub token stored in `.env` (gitignored)
- Auto-push disabled by default
- Push operations require human approval
- Token never logged or committed

### 🐛 Bug Fixes

- Fixed MCP manager initialization order
- Improved error handling for Git operations
- Better logging for version control actions

### 📚 Updated Documentation

- Added GitHub configuration to `CONFIGURATION.md`
- Updated `.env.template` with Git/GitHub settings
- Added Version Control examples to `README.md`

### 🔄 Backward Compatibility

- All v2.0 features preserved
- Git integration is optional (works without GitHub token)
- Existing workflows unchanged

---

## Version 2.0 - Environment Configuration (October 28, 2025)

## 🎉 What's New

### Environment-Based Configuration
All system settings can now be configured through the `.env` file instead of modifying YAML or code files.

## ✨ New Features

### 1. **Comprehensive Environment Variables**
Added support for system-wide configuration via `.env`:

```properties
# System Configuration
MAX_PARALLEL_AGENTS=10
DEFAULT_MODEL=claude-sonnet-4-5
WORKSPACE_PATH=.claude/workspace
MAX_EVOLUTION_ITERATIONS=3
HYPOTHESIS_GENERATION_COUNT=7
MAX_TOKENS=8000
TEMPERATURE=0.7
HUMAN_APPROVAL_TIMEOUT=3600
DEBUG_MODE=false
PROGRESS_CHECK_INTERVAL=300
MAX_RETRIES=3
RETRY_BACKOFF_FACTOR=2
VECTOR_DB_PATH=./data/vector_db
GRACEFUL_DEGRADATION=true
```

### 2. **Environment Configuration Module** (`utils/env_config.py`)
- Centralized configuration loading
- Type validation and conversion
- Default value handling
- Configuration merging with YAML

### 3. **Enhanced CLI Status Command**
```bash
python cli.py status
```

Now displays:
- API key validation
- Current system configuration
- Model selection
- Workspace paths

### 4. **Configuration Documentation** (`CONFIGURATION.md`)
- Complete reference for all environment variables
- Configuration examples and presets
- Best practices
- Troubleshooting guide

### 5. **Updated .env.template**
Expanded template with:
- All configuration options documented
- Organized into sections
- Example values
- Comments explaining each setting

## 📝 Updated Files

### New Files:
1. `utils/env_config.py` - Environment configuration loader
2. `CONFIGURATION.md` - Comprehensive configuration guide
3. `.gitignore` - Git ignore patterns
4. `CHANGELOG.md` - This file

### Modified Files:
1. `.env.template` - Added system configuration options
2. `main.py` - Integration with environment config
3. `cli.py` - Enhanced status command
4. `config.yaml` - Added comments about environment overrides
5. `README.md` - Updated with configuration examples

## 🔧 Configuration Override Priority

1. **Environment Variables** (`.env` file) - Highest priority
2. **YAML Configuration** (`config.yaml`) - Fallback
3. **Code Defaults** - Last resort

Example:
```
MAX_EVOLUTION_ITERATIONS in .env = 5
config.yaml evolution_rounds = 3
→ System uses 5
```

## 🎯 Configuration Presets

### Fast Development
```properties
MAX_PARALLEL_AGENTS=3
MAX_EVOLUTION_ITERATIONS=1
HYPOTHESIS_GENERATION_COUNT=3
DEBUG_MODE=true
```

### Balanced Production (Recommended)
```properties
MAX_PARALLEL_AGENTS=10
MAX_EVOLUTION_ITERATIONS=3
HYPOTHESIS_GENERATION_COUNT=7
DEFAULT_MODEL=claude-sonnet-4-5
```

### High Quality Research
```properties
MAX_PARALLEL_AGENTS=15
MAX_EVOLUTION_ITERATIONS=5
HYPOTHESIS_GENERATION_COUNT=10
DEFAULT_MODEL=claude-opus-4
MAX_TOKENS=16000
```

## 🚀 Migration Guide (v1 → v2)

### Step 1: Update .env file
```bash
# Backup old .env
cp .env .env.backup

# Copy new template
cp .env.template .env

# Add your API keys back
# Add new configuration options
```

### Step 2: No code changes needed!
The system automatically detects and uses environment variables.

### Step 3: Verify configuration
```bash
python cli.py status
```

## 🐛 Bug Fixes
- Fixed environment variable loading order
- Improved error messages for missing API keys
- Better validation for numeric configuration values

## ⚡ Performance Improvements
- Configuration is loaded once at startup
- Cached configuration reduces file I/O
- Optimized default values

## 📊 Benefits

### Before (v1):
```yaml
# config.yaml
agents:
  research_guild:
    hypothesis:
      evolution_rounds: 3
```
❌ Required code/YAML editing
❌ No validation
❌ Hard to switch configurations

### After (v2):
```properties
# .env
MAX_EVOLUTION_ITERATIONS=3
```
✅ Simple key-value format
✅ Type validation
✅ Easy preset switching
✅ Gitignore-safe (secrets protected)

## 🔒 Security Improvements
- Added `.gitignore` to prevent committing secrets
- API keys never in code or YAML
- Template file for sharing configuration structure

## 📚 Documentation
- Added `CONFIGURATION.md` with complete reference
- Updated `README.md` with quick start guide
- Updated `SYSTEM_OVERVIEW.md` with env config info
- Added inline code comments

## 🧪 Testing
All existing functionality preserved - backward compatible with v1.

## 🙏 Notes
- All previous features remain functional
- YAML config still works as fallback
- No breaking changes to agent code
- Human-in-the-loop approval still works

## 📦 What's in the Archive

```
linguistic-bridges-mas-v2.tar.gz
├── agents/           # Agent implementations
├── guilds/           # Guild coordinators
├── mcps/             # MCP integrations
├── utils/            # Utilities (NEW: env_config.py)
├── config.yaml       # YAML config (with env override comments)
├── .env.template     # Environment template (UPDATED)
├── main.py           # Entry point (UPDATED)
├── cli.py            # CLI interface (UPDATED)
├── requirements.txt  # Dependencies
├── README.md         # Quick start guide (UPDATED)
├── CONFIGURATION.md  # Config reference (NEW)
├── SYSTEM_OVERVIEW.md # System documentation
├── CHANGELOG.md      # This file (NEW)
└── .gitignore        # Git ignore (NEW)
```

## 🎓 Next Steps

1. Extract the archive
2. Copy `.env.template` to `.env`
3. Add your `ANTHROPIC_API_KEY`
4. Customize system settings in `.env`
5. Run `python cli.py status` to verify
6. Run `python main.py` to start

## 💡 Tips

- Start with default values
- Enable `DEBUG_MODE=true` during development
- Use presets for common scenarios
- Read `CONFIGURATION.md` for detailed options
- Check `python cli.py status` anytime

---

**Version**: 2.0  
**Release Date**: October 28, 2025  
**Compatibility**: Backward compatible with v1.0
