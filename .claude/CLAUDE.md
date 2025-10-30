# SuperClaude Framework Configuration for Linguistic Bridges

This file serves as the entry point for the SuperClaude Framework, configured for the Linguistic Bridges Multi-Agent System.

The SuperClaude framework components will be automatically imported and applied to all interactions.

---

# ===================================================
# SuperClaude Framework Components
# ===================================================

## Core Framework
@PRINCIPLES.md
@RULES.md
@FLAGS.md
@SYMBOLS.md

## Behavioral Modes
@MODE_Brainstorming.md
@MODE_Introspection.md
@MODE_Orchestration.md
@MODE_Task_Management.md
@MODE_Token_Efficiency.md
@MODE_Deep_Research.md
@MODE_Business_Panel.md

## Specialized Agents
@AGENTS_Research.md
@AGENTS_Implementation.md
@AGENTS_Documentation.md

## MCP Documentation
@MCP_Context7.md
@MCP_Sequential.md
@MCP_Serena.md
@MCP_Morphllm.md
@MCP_Playwright.md
@MCP_Tavily.md
@MCP_ARXIV_SCHOLAR.md

## Advanced Patterns
@PATTERNS_Parallel_Execution.md
@PATTERNS_Confidence_Scoring.md
@PATTERNS_Research_Methodology.md

# ===================================================
# LINGUISTIC BRIDGES - SUPERCLAUSE CONFIGURATION
# ===================================================

## Global Default: SuperClaude Framework Enabled

**Status**: ACTIVE
**Scope**: All Claude Code sessions for this project
**Version**: 2.0+ compatibility

The SuperClaude Framework is now your default reasoning engine for all work on the Linguistic Bridges Multi-Agent System.

### Auto-Activation Triggers

SuperClaude framework automatically activates for:
- **Research Phase**: Hypothesis generation, debate, evolution
- **Implementation Phase**: Parallel track execution, progress monitoring
- **Documentation Phase**: Report synthesis, clarity optimization
- **Complex Analysis**: Multi-component reasoning, system design
- **Cross-Guild Coordination**: Supervisor orchestration, conflict resolution

### Default Behavioral Modes

| Phase | Default Mode | Purpose |
|-------|--------------|---------|
| Research | Deep Research + Business Panel | Multi-hop hypothesis generation with expert debate |
| Implementation | Orchestration + Token Efficiency | Parallel execution with resource optimization |
| Documentation | Task Management + Token Efficiency | Structured synthesis with clarity |
| General | Introspection + Brainstorming | Continuous learning and discovery |

### Execution Principles

1. **Parallel-First**: Default to concurrent operations, sequential only when dependencies require
2. **Confidence Scoring**: All outputs include quality metrics (min 0.7 threshold)
3. **Session Persistence**: Use Serena MCP for cross-session learning
4. **Evidence-Based**: All claims verifiable through testing or documentation
5. **Token Efficiency**: Use symbol communication for 30-50% compression
6. **Quality Gates**: Validate before execution, verify after completion

---

## ===================================================
## MCP Server Configuration
## ===================================================

### Primary Integrations
- **Sequential**: Multi-step reasoning for hypothesis evolution and system design
- **Context7**: Official documentation for frameworks and libraries
- **Serena**: Semantic code understanding and session persistence
- **Tavily**: Web search for research phase information gathering

### Academic Research Integrations (DEFAULT FOR LITERATURE SEARCH)
- **Google Scholar MCP**: Citation analysis, foundational papers, author research
- **ArXiv MCP**: Latest preprints, technical papers, PDF downloads

**Research Workflow**: Google Scholar (foundation) → ArXiv (latest) → Tavily (practical)

### Secondary Integrations
- **Morphllm**: Pattern-based code transformations
- **Playwright**: E2E testing and validation

### Auto-Activation Rules

```yaml
mcp_activation:
  research_phase:
    primary: [tavily, sequential]
    academic_research: [google-scholar, arxiv]  # DEFAULT FOR LITERATURE SEARCH
    secondary: [context7]

    # Academic research workflow
    academic_workflow:
      1_foundation: google-scholar    # Foundational papers, citations
      2_latest: arxiv                 # Recent preprints, technical details
      3_practical: tavily             # Implementations, tutorials
      rate_limiting:
        google_scholar: "10-15s delay between requests"
        arxiv: "2-3s delay (generous)"
      max_per_session:
        google_scholar: 5  # Max searches due to strict rate limits
        arxiv: unlimited

  implementation_phase:
    primary: [serena, sequential]
    academic_reference: [arxiv]
    secondary: [morphllm]

  documentation_phase:
    primary: [serena, context7]
    academic_reference: [google-scholar, arxiv]
    secondary: [morphllm, playwright]

performance_optimization:
  parallel_execution: true
  token_efficiency: aggressive
  caching_enabled: true
  batch_operations: true

academic_research_optimization:
  google_scholar_rate_limiting: "CRITICAL - 10-15s min delay"
  arxiv_parallelization: "Safe for rapid searches (2-3s delay)"
  search_planning: "Always plan searches before execution"
  caching: "Store results locally (Scholar cache, ArXiv PDFs)"
```

---

## ===================================================
## Linguistic Bridges Customizations
## ===================================================

### Agent Mapping to Guilds

**Research Guild**:
- Research Agent (Tavily integration)
- Hypothesis Evolution Agent (Sequential reasoning)
- Meta-Review Agent (Business panel debate)

**Forge Guild**:
- Implementation Expert (Parallel execution)
- Performance Engineer (Optimization focus)
- Quality Engineer (Testing strategy)

**Chroniclers Guild**:
- Technical Writer (Documentation focus)
- Architect (System design documentation)
- Learning Guide (Onboarding documentation)

**Supervisor**:
- System Architect (Overall orchestration)
- PM Agent (Project management)
- Root Cause Analyst (Conflict resolution)

### Project-Specific Flags

**Research Phase Flags**:
- `--brainstorm` - Hypothesis exploration mode
- `--research` - Deep investigation with multi-hop reasoning
- `--business-panel` - Expert debate for hypothesis evaluation

**Implementation Phase Flags**:
- `--orchestrate` - Parallel track execution planning
- `--think-hard` - Complex reasoning for implementation strategy
- `--token-efficient` - Resource optimization

**Documentation Phase Flags**:
- `--task-manage` - Hierarchical document organization
- `--uc` - Ultra-compressed synthesis
- `--document` - Focused documentation generation

---

## ===================================================
## Slash Commands for Linguistic Bridges
## ===================================================

### Research Phase
- `/sc:brainstorm` - Hypothesis exploration and requirement discovery
- `/sc:research` - Deep investigation with web search and multi-hop reasoning
- `/sc:spec-panel` - Expert panel evaluation of hypotheses

### Implementation Phase
- `/sc:implement` - Track implementation with validation
- `/sc:design` - Architecture and design system
- `/sc:analyze` - Code quality analysis

### Documentation Phase
- `/sc:document` - Generate focused documentation
- `/sc:index` - Create project documentation index
- `/sc:improve` - Enhance documentation clarity

### Session Management
- `/sc:load` - Load Linguistic Bridges project context
- `/sc:save` - Save session state and learnings
- `/sc:task` - Delegate complex tasks to appropriate agents

---

## ===================================================
## Performance & Quality Standards
## ===================================================

### Quality Metrics

**Hypothesis Quality**:
- Novelty: 0.7+ score
- Feasibility: 0.8+ score
- Research backing: 3+ sources minimum
- Overall confidence: 0.75+ threshold

**Implementation Quality**:
- Test coverage: 80%+ minimum
- Code review: Passing quality gates
- Performance: Within baseline targets
- Security: Zero critical vulnerabilities

**Documentation Quality**:
- Coverage: All major components documented
- Clarity: Accessible to intended audience
- Correctness: Verified against code
- Completeness: 0.85+ coverage score

### Execution Standards

1. **Before Starting**: Load project context with `/sc:load`
2. **During Work**: Regular checkpoints with `/sc:save`
3. **After Completion**: Verify quality gates before marking done
4. **Discovery**: Always use introspection for learning insights

---

## ===================================================
## Token Efficiency Configuration
## ===================================================

### Symbol System (30-50% Compression)

**Enabled by Default**: `--uc` / `--ultracompressed`

Benefits:
- Research symbols: `🔍`, `📚`, `💡`, `⚠️`
- Implementation symbols: `⚡`, `🛡️`, `🎨`, `🏗️`
- Status symbols: `✅`, `❌`, `🔄`, `⏳`
- Flow symbols: `→`, `⇒`, `∴`, `∵`

### Abbreviation System

Standard technical abbreviations enabled:
- `auth` ← authentication
- `perf` ← performance
- `sec` ← security
- `qual` ← quality
- `impl` ← implementation
- `req` ← requirements

### Batch Operations

- **Multiple file reads**: Use parallel Read calls
- **Multiple edits**: Use batch operations
- **Multiple analyses**: Execute in parallel

---

## ===================================================
## Session Lifecycle Pattern
## ===================================================

### Session Start
```bash
/sc:load
# Load Linguistic Bridges project context
# Restore previous session state if available
# Initialize MCP servers
```

### During Work
```
1. Choose appropriate behavioral mode for task
2. Use relevant slash commands (`/sc:*`)
3. Leverage MCP integrations
4. Track progress with TodoWrite
5. Checkpoint every 30 minutes with /sc:save
```

### Session End
```bash
/sc:save
# Save session state
# Document learnings and patterns
# Update project memory
# Clean up temporary resources
```

### Example Session
```
Session Start:
  /sc:load → Load Linguistic Bridges context

Research Task:
  /sc:brainstorm → Explore hypothesis ideas
  /sc:research → Deep investigation
  /sc:spec-panel → Expert evaluation

Checkpoint:
  /sc:save → Save progress and learnings

Implementation Task:
  /sc:design → Architecture planning
  /sc:implement → Implementation with validation

Final Checkpoint:
  /sc:save → Save final state
```

---

## ===================================================
## Troubleshooting & Fallbacks
## ===================================================

### If MCP Servers Unavailable
- `--no-mcp` flag activates native reasoning fallback
- Core SuperClaude framework remains active
- Configuration and principles still apply

### If Configuration Not Loading
- Verify `.claude/` directory exists
- Check all @include files are present
- Restart Claude Code session

### Performance Tuning
- Use `--uc` for token-constrained tasks
- Use `--think-hard` for complex reasoning
- Use `--orchestrate` for resource optimization

---

## ===================================================
## Framework Version & Status
## ===================================================

**Framework**: SuperClaude v2.0+
**Configuration Date**: October 28, 2025
**Project**: Linguistic Bridges Multi-Agent System
**Status**: ACTIVE - All systems enabled

**Last Updated**: When new modes or agents are added
**Maintainer**: Claude Code with SuperClaude Framework

---

## Quick Reference

### Most Used Commands
- `/sc:load` - Start session
- `/sc:brainstorm` - Explore ideas
- `/sc:research` - Investigate deeply
- `/sc:implement` - Build features
- `/sc:save` - End session

### Most Used Flags
- `--brainstorm` - Discovery mode
- `--orchestrate` - Parallel execution
- `--think-hard` - Deep analysis
- `--uc` - Token efficiency
- `--research` - Web research

### Most Used Modes
- **Research**: Multi-hop reasoning with expert debate
- **Implementation**: Parallel-first execution
- **Documentation**: Clarity-focused synthesis

---

**SuperClaude Framework is now your default reasoning engine for Linguistic Bridges. All interactions will leverage the framework's capabilities for enhanced productivity, quality, and intelligent automation.**
