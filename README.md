# 🌉 Linguistic Bridges Multi-Agent System

A sophisticated multi-agent system for researching and implementing the "Linguistic Bridges" project: Modeling Visual Art and Music Alignment through Language.

## 🏗️ Architecture

The system consists of:

- **Supervisor Agent**: Orchestrates the entire project workflow
- **Research Guild**: Hypothesis generation, reflection, ranking, evolution, and meta-review
- **Forge Guild**: Code implementation, experimentation, and evaluation
- **Chroniclers Guild**: Documentation and report writing

### MCP (Model Context Protocol) Integrations

- LLM APIs (Anthropic Claude, Google Gemini)
- Web Search (Tavily)
- Academic Search (arXiv)
- PDF Parsing
- Vector Database (ChromaDB) for shared memory
- Git integration (planned)
- Audio/Image feature extraction (planned)

## 📋 Prerequisites

- Python 3.10+
- API Keys:
  - Anthropic API Key
  - Google AI API Key (optional)
  - Tavily API Key (for web search)

## 🚀 Quick Start

### 1. Installation

```bash
cd linguistic-bridges-mas
pip install -r requirements.txt
```

### 2. Environment Setup

Create and configure your `.env` file:

```bash
# Copy the template
cp .env.template .env

# Edit with your settings
nano .env  # or use your preferred editor
```

**Required settings:**
```properties
# Minimum required
ANTHROPIC_API_KEY=your_anthropic_key_here

# Recommended system configuration
MAX_PARALLEL_AGENTS=10
DEFAULT_MODEL=claude-sonnet-4-5
MAX_EVOLUTION_ITERATIONS=3
HYPOTHESIS_GENERATION_COUNT=7
```

For detailed configuration options, see [CONFIGURATION.md](CONFIGURATION.md).

### 3. Run the System

```bash
# Initialize directories
python cli.py init

# Check system status
python cli.py status

# Run the full system
python main.py
```

## 🎯 Usage Examples

### Basic Usage

The system will automatically:
1. Generate and evolve research hypotheses
2. Implement the 3-track methodology
3. Write a comprehensive research report

### Custom Configuration

All system behavior can be customized via the `.env` file:

```properties
# Control parallelism
MAX_PARALLEL_AGENTS=10

# Choose your model
DEFAULT_MODEL=claude-sonnet-4-5  # or claude-opus-4, gemini-2.0-flash

# Adjust research depth
MAX_EVOLUTION_ITERATIONS=3
HYPOTHESIS_GENERATION_COUNT=7

# Set workspace location
WORKSPACE_PATH=.claude/workspace

# Enable debugging
DEBUG_MODE=true
```

See [CONFIGURATION.md](CONFIGURATION.md) for complete configuration reference.

### Configuration Presets

**Fast Development:**
```properties
MAX_PARALLEL_AGENTS=3
MAX_EVOLUTION_ITERATIONS=1
HYPOTHESIS_GENERATION_COUNT=3
DEBUG_MODE=true
```

**Production Quality:**
```properties
MAX_PARALLEL_AGENTS=10
MAX_EVOLUTION_ITERATIONS=3
HYPOTHESIS_GENERATION_COUNT=7
DEFAULT_MODEL=claude-sonnet-4-5
```

**High Quality Research:**
```properties
MAX_PARALLEL_AGENTS=15
MAX_EVOLUTION_ITERATIONS=5
HYPOTHESIS_GENERATION_COUNT=10
DEFAULT_MODEL=claude-opus-4
```

## 📁 Project Structure

```
linguistic-bridges-mas/
├── agents/
│   ├── base_agent.py          # Base agent class
│   └── supervisor.py           # Supervisor orchestrator
├── guilds/
│   ├── research_guild.py       # Research coordination
│   ├── forge_guild.py          # Implementation
│   ├── chroniclers_guild.py    # Documentation
│   └── research/
│       ├── hypothesis_generator.py
│       └── research_agents.py  # Reflector, Ranker, Evolver, Meta-Reviewer
├── mcps/
│   └── mcp_manager.py          # MCP integrations
├── shared/                     # Shared utilities
├── data/                       # Datasets and vector DB
├── outputs/                    # Generated reports and results
├── logs/                       # System logs
├── config.yaml                 # Configuration
├── requirements.txt
└── main.py                     # Entry point
```

## 🔄 Workflow

### Phase 1: Research
1. **Generate** initial hypotheses using LLM + literature
2. **Reflect** on each hypothesis critically
3. **Rank** through Elo-based debate tournaments
4. **Evolve** top hypotheses with meta-feedback
5. Repeat for N rounds (default: 3)

### Phase 2: Implementation
1. Setup data pipeline (ArtEmis, SDD)
2. Implement Track 1: Disentangled Representation Learning
3. Implement Track 2: Mediator Function Learning
4. Implement Track 3: Blueprint-Driven Generation
5. Run evaluations (t-SNE, CLIP Score, etc.)

### Phase 3: Documentation
1. Draft report sections (Intro, Methods, Results, Conclusion)
2. Edit and format (LaTeX/Markdown)
3. Generate final deliverable

## 🛠️ Advanced Features

### Human-in-the-Loop

Critical decisions require human approval:

```python
# Configured in config.yaml
human_approval:
  required_for:
    - "finalize_hypothesis"
    - "deploy_experiment"
```

### Failure Recovery

Automatic retry with exponential backoff:

```yaml
failure_recovery:
  max_retries: 3
  backoff_factor: 2
  fallback_agents_enabled: true
```

### Progress Monitoring

Real-time monitoring of guild progress:

```python
status = supervisor.get_project_status()
```

## 📊 Memory System

Shared Vector Database (ChromaDB) enables:
- Cross-guild knowledge sharing
- RAG-based report generation
- Hypothesis deduplication
- Experimental result retrieval

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest tests/
```

## 🤝 Contributing

This is a research project. Contributions for improving:
- Agent reasoning capabilities
- MCP integrations
- Evaluation metrics
- Documentation quality

are welcome!

## 📝 License

MIT License (or specify your license)

## 🙏 Acknowledgments

- Based on "AI co-scientist" paper's Generate-Debate-Evolve workflow
- Inspired by the "Linguistic Bridges" research proposal
- Anthropic Claude for LLM capabilities
- ChromaDB for vector memory

## 📞 Contact

For questions or issues, please open a GitHub issue.

---

**Status**: Active Development 🚧

**Version**: 1.0.0

**Last Updated**: October 28, 2025
