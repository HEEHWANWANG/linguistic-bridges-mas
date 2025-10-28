# Linguistic Bridges Multi-Agent System - Complete Overview

## 🎯 System Purpose

This multi-agent system implements a sophisticated research workflow for the "Linguistic Bridges" project, which aims to model how visual art and music align through language by understanding the interaction between structure, style, and emotion.

## 🏗️ Architecture Overview

### 1. **Supervisor Agent** (Central Orchestrator)
- **Role**: Project manager coordinating all guilds
- **Capabilities**:
  - Task decomposition and distribution
  - Progress monitoring with bottleneck detection
  - Conflict resolution between guilds
  - Resource allocation (GPU, API rate limits)
  - Human-in-the-loop decision points

### 2. **Research Guild** (Hypothesis Development)
Implements the "Generate, Debate, Evolve" workflow:

**Sub-Agents:**
- **Hypothesis Generator**: Creates initial hypotheses using LLM + literature search
- **Hypothesis Reflector**: Critically evaluates novelty, rigor, testability
- **Hypothesis Ranker**: Elo-based tournament debate for ranking
- **Hypothesis Evolver**: Synthesizes and improves top hypotheses
- **Meta-Reviewer**: Identifies systemic issues across all hypotheses

**Workflow:**
```
Generate → Reflect → Rank → Evolve → Repeat (N rounds)
```

### 3. **Forge Guild** (Implementation)
**Sub-Agents (planned):**
- Data Pipeline Agent: ArtEmis + SDD dataset loading
- Track Coder Agents (1-3): Implement disentanglement, mediator, generation
- Evaluation Agent: Run t-SNE, CLIP Score, metrics
- QA & DevOps Agent: Code review, Git integration
- Experimental Loop Agent: Feedback to Research Guild

**Key Feature:** Bidirectional feedback with Research Guild when experiments fail

### 4. **Chroniclers Guild** (Documentation)
**Sub-Agents:**
- Drafting Agent: RAG-based report generation
- Editing & Formatting Agent: LaTeX/Markdown output

## 🔌 MCP (Model Context Protocol) Integrations

### Current MCPs:
1. **LLM Providers**
   - Anthropic Claude Sonnet 4.5
   - Google Gemini 2.0 Flash

2. **Web Search**
   - Tavily API (primary)
   - Fallback to Google Custom Search

3. **Academic Search**
   - arXiv API for paper retrieval

4. **PDF Parser**
   - PyMuPDF for extracting paper content

5. **Vector Database**
   - ChromaDB for shared memory
   - RAG capabilities for cross-guild knowledge

### Planned MCPs:
- Git integration for version control
- Audio feature extraction (librosa, essentia)
- Image feature extraction (CLIP, OpenCV)
- Embedding visualization (t-SNE, UMAP)
- Diffusion model API (Stable Diffusion)

## 📊 Shared Memory System

**Vector Database (ChromaDB)**
- **Purpose**: Shared long-term memory for all agents
- **Collections**:
  - `research_artifacts`: Hypotheses, literature reviews
  - `code_artifacts`: Generated code, experiment results
  - `documentation`: Report drafts, final documents
  - `project_artifacts`: Conflict resolutions, decisions

**Benefits:**
- Asynchronous guild communication
- RAG-based report generation
- Hypothesis deduplication
- Cross-modal knowledge retrieval

## 🔄 Complete Workflow

### Phase 1: Research (Hypothesis Development)
```
1. Generate initial hypotheses (5-10)
2. For each evolution round (default: 3):
   a. Reflect on each hypothesis
   b. Rank through debates
   c. Meta-review for systemic issues
   d. Evolve top 3 hypotheses
3. Human approval for final hypotheses
4. Store in shared memory
```

### Phase 2: Implementation (Code & Experiments)
```
1. Setup data pipeline (ArtEmis, SDD)
2. For each track (1-3):
   a. Generate PyTorch implementation
   b. Run experiments
   c. If results poor → feedback to Research Guild
3. Run comprehensive evaluation
4. Store code and results
```

### Phase 3: Documentation (Report Writing)
```
1. Retrieve artifacts from memory (RAG)
2. Draft report sections
3. Edit and format (LaTeX/Markdown)
4. Generate final deliverable
```

## 🎛️ Key Features

### 1. Human-in-the-Loop
Critical decisions require approval:
- Finalizing research hypotheses
- Deploying expensive experiments
- Major code changes

### 2. Failure Recovery
- Exponential backoff for API failures
- Fallback agents when primary fails
- Graceful degradation (partial completion)

### 3. Progress Monitoring
- Real-time guild status tracking
- Bottleneck detection (>30min stagnation)
- Automatic alerts and interventions

### 4. Conflict Resolution
- LLM-mediated disputes between guilds
- Stored resolutions for future reference

## 📁 Project Structure

```
linguistic-bridges-mas/
├── agents/
│   ├── base_agent.py              # Abstract base class
│   └── supervisor.py              # Orchestrator
├── guilds/
│   ├── research_guild.py          # Research coordinator
│   ├── forge_guild.py             # Implementation guild
│   ├── chroniclers_guild.py       # Documentation guild
│   └── research/
│       ├── hypothesis_generator.py
│       └── research_agents.py     # Reflector, Ranker, Evolver, Meta-Reviewer
├── mcps/
│   └── mcp_manager.py             # MCP integrations
├── shared/                        # Shared utilities
├── utils/                         # Helper functions
├── data/                          # Datasets & vector DB
├── outputs/                       # Results & reports
├── logs/                          # System logs
├── config.yaml                    # Configuration
├── requirements.txt               # Dependencies
├── main.py                        # Entry point
├── cli.py                         # CLI interface
├── .env.template                  # Environment template
└── README.md                      # Documentation
```

## 🚀 Usage

### Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.template .env
# Edit .env with your API keys

# 3. Initialize
python cli.py init

# 4. Run
python main.py
```

### CLI Commands
```bash
# Run full workflow
python cli.py run

# Check system status
python cli.py status

# Initialize directories
python cli.py init

# Clean temporary files
python cli.py clean
```

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
agents:
  supervisor:
    max_iterations: 100
    progress_check_interval: 300  # seconds
    
  research_guild:
    hypothesis:
      generation_batch_size: 5
      evolution_rounds: 3
      
  forge_guild:
    experimental_loop:
      feedback_threshold: 0.7
      
human_approval:
  required_for:
    - finalize_hypothesis
    - deploy_experiment
```

## 🔐 Environment Variables

Required:
- `ANTHROPIC_API_KEY`: Claude API access

Optional:
- `GOOGLE_API_KEY`: Gemini API access
- `TAVILY_API_KEY`: Web search
- `STABILITY_API_KEY`: Image generation

## 📈 Monitoring & Debugging

### System Status
```python
status = supervisor.get_project_status()
# Returns:
# - Supervisor status
# - Guild statuses
# - Resource allocation
# - Current blockers
```

### Logs
- Location: `./logs/`
- Levels: DEBUG, INFO, WARNING, ERROR
- Rich formatting with tracebacks

## 🧪 Testing & Validation

The system includes:
- Health checks for all MCPs
- Hypothesis quality metrics (novelty, testability)
- Code evaluation metrics
- Human validation checkpoints

## 🔬 Research-Specific Features

### For "Linguistic Bridges" Project:

1. **Track 1 - Disentanglement**
   - Separates structure, style, affect representations
   - Multi-axis contrastive learning

2. **Track 2 - Mediator Function**
   - Models emotion = f(structure, style)
   - Cross-modal consistency

3. **Track 3 - Blueprint-Driven Generation**
   - Music → Visual synthesis
   - Diffusion-based generation

## 🤝 Extensibility

Easy to extend:
- Add new agents by inheriting `BaseAgent`
- Register new MCPs in `MCPManager`
- Create custom guilds for new workflows
- Plug in domain-specific tools

## ⚠️ Limitations & Future Work

**Current Limitations:**
- Forge Guild sub-agents are stubs (need full implementation)
- Git integration not yet implemented
- Audio/image feature extraction planned
- Diffusion model integration pending

**Future Enhancements:**
- Multi-modal embedding alignment
- Automated hyperparameter tuning
- Distributed execution across GPUs
- Real-time dashboard for monitoring
- Automated testing suite

## 📊 Expected Outputs

1. **Research Artifacts**
   - Evolved hypotheses (JSON)
   - Literature synthesis
   - Meta-reviews

2. **Code Artifacts**
   - PyTorch implementations for 3 tracks
   - Training/evaluation scripts
   - Experiment results

3. **Documentation**
   - Final research report (LaTeX/PDF)
   - Code documentation
   - Experimental logs

## 🎓 Academic Context

This system is designed for the "인공지능을 통한 자연어 처리" course project at Seoul National University, implementing research on music-visual art alignment through multimodal language models.

## 📞 Support & Contact

For issues or questions:
- Check README.md
- Review config.yaml comments
- Examine logs in ./logs/
- Inspect vector DB artifacts

---

**Version**: 1.0.0  
**Last Updated**: October 28, 2025  
**Status**: Ready for Deployment 🚀
