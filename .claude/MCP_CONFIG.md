# Linguistic Bridges - MCP Server Configuration

Model Context Protocol (MCP) server integration for enhanced capabilities.

## Quick Reference

| Server | Purpose | When to Use |
|--------|---------|------------|
| **Tavily** | Web search & research | Research phase, literature gathering |
| **Sequential** | Complex reasoning | Hypothesis evolution, system design |
| **Serena** | Code understanding & memory | Session persistence, refactoring |
| **Context7** | Official documentation | Framework API lookup, best practices |
| **Morphllm** | Pattern-based editing | Bulk code transformations |
| **Playwright** | Browser testing | E2E testing, visual validation |

---

## 1. TAVILY - Web Search & Research

**Purpose**: Real-time web search with AI-powered ranking and content extraction

**Integration Level**: Primary for Research Guild

**Use Cases**:
- Finding recent papers on music-visual alignment
- Gathering state-of-the-art benchmarks
- Identifying related work and comparisons
- Literature review for hypothesis grounding

**Configuration**:
```yaml
tavily:
  enabled: true
  priority: high
  auto_activate:
    - research_phase: true
    - literature_review: true
    - benchmark_gathering: true

  search_settings:
    depth: advanced  # For comprehensive searches
    include_raw_content: true  # For full text extraction
    max_results: 10
    freshness: current  # Recent sources prioritized
```

**Example Commands**:
```bash
/sc:research "recent advances in visual-musical alignment"
/sc:research "state-of-the-art music generation methods 2024"
```

**Output**: Ranked search results, extracted content, source credibility scores

---

## 2. SEQUENTIAL - Multi-Step Reasoning

**Purpose**: Structured multi-step thinking for complex analysis

**Integration Level**: Primary for Research evolution, hypothesis ranking

**Use Cases**:
- Hypothesis generation and evaluation
- Hypothesis evolution debates
- System design for implementation
- Complex problem-solving

**Configuration**:
```yaml
sequential:
  enabled: true
  priority: high
  auto_activate:
    - hypothesis_evolution: true
    - system_design: true
    - complex_analysis: true

  reasoning_settings:
    default_depth: 5
    max_thoughts: 10
    confidence_threshold: 0.7
```

**Example Usage**:
```
/sc:think "Evaluate these 5 hypotheses for novelty and feasibility"
→ Multi-step reasoning through each hypothesis
→ Comparative analysis
→ Confidence scoring
→ Recommendation with reasoning
```

**Output**: Structured reasoning chains, intermediate insights, confidence metrics

---

## 3. SERENA - Code Understanding & Session Memory

**Purpose**: Semantic code analysis, symbol operations, cross-session persistence

**Integration Level**: Primary for session management, code refactoring

**Use Cases**:
- Symbol renaming and refactoring
- Code navigation and understanding
- Session context persistence
- Cross-session learning and pattern reuse

**Configuration**:
```yaml
serena:
  enabled: true
  priority: high
  auto_activate:
    - session_start: true
    - code_navigation: true
    - refactoring: true

  memory_settings:
    persistence_enabled: true
    cross_session: true
    retention_days: 90
    auto_save_interval: 30min
```

**Session Lifecycle**:
```
Session Start:
  /sc:load → Serena loads previous context

During Work:
  Serena tracks symbols, references, architecture

Periodic Checkpoint (30min):
  /sc:save → Save to Serena memory

Session End:
  /sc:save → Persist learnings and patterns

Next Session:
  /sc:load → Resume with context
```

**Output**: Project context, learned patterns, previous discoveries

---

## 4. CONTEXT7 - Official Documentation

**Purpose**: Access to official, curated library documentation

**Integration Level**: Secondary, on-demand for implementation details

**Use Cases**:
- PyTorch/TensorFlow API reference
- Model architecture best practices
- Framework-specific patterns
- Version-specific implementation details

**Configuration**:
```yaml
context7:
  enabled: true
  priority: medium
  auto_activate:
    - code_implementation: on_demand
    - api_lookup: on_demand

  library_focus:
    - pytorch
    - transformers
    - numpy
    - scipy
```

**Example Usage**:
```bash
"How do I implement custom PyTorch layers?"
→ Context7 returns official PyTorch patterns
```

**Output**: Official examples, best practices, version-specific guidance

---

## 5. MORPHLLM - Pattern-Based Editing

**Purpose**: Efficient bulk code transformations using patterns

**Integration Level**: Secondary, for implementation phase

**Use Cases**:
- Apply coding standards across codebase
- Refactor code patterns systematically
- Update imports and dependencies
- Code style enforcement

**Configuration**:
```yaml
morphllm:
  enabled: true
  priority: medium
  auto_activate:
    - bulk_refactoring: true
    - style_enforcement: true

  edit_settings:
    scope: linguistic_bridges/
    verify_before_apply: true
    rollback_on_error: true
```

**Example Usage**:
```bash
"Convert all Type[X] hints to use | operator (Python 3.10+)"
→ Morphllm analyzes patterns
→ Applies transformation systematically
→ Reports changes
```

**Output**: Systematic code transformations, change reports

---

## 6. PLAYWRIGHT - Browser Testing

**Purpose**: E2E testing, visual regression, accessibility validation

**Integration Level**: Secondary, for implementation validation

**Use Cases**:
- E2E test development for web interfaces
- Visual regression testing
- Accessibility (WCAG) compliance checking
- Performance testing

**Configuration**:
```yaml
playwright:
  enabled: true
  priority: medium
  auto_activate:
    - e2e_testing: on_demand
    - accessibility_validation: on_demand

  browser_settings:
    browsers: [chromium]
    headless: true
    timeout: 30000
```

**Example Usage**:
```bash
/sc:test "Validate accessibility compliance of documentation UI"
→ Playwright navigates and tests
→ Reports WCAG compliance
```

**Output**: Test results, accessibility reports, visual diffs

---

## MCP Auto-Activation Rules

### Research Phase
```yaml
auto_activate:
  primary: [tavily, sequential]
  triggers:
    - hypothesis_generation: true
    - literature_review: true
    - hypothesis_evolution: true

  parallel_execution:
    - tavily searches: batch 5
    - sequential reasoning: per hypothesis
```

### Implementation Phase
```yaml
auto_activate:
  primary: [serena]
  secondary: [morphllm, context7]
  triggers:
    - code_implementation: true
    - refactoring: true
    - testing: true

  parallel_execution:
    - serena symbol analysis: continuous
    - morphllm transformations: batched
```

### Documentation Phase
```yaml
auto_activate:
  primary: [serena, context7]
  secondary: [morphllm]
  triggers:
    - documentation_writing: true
    - code_documentation: true
    - api_docs: true

  parallel_execution:
    - serena context retrieval: batched
```

---

## Performance Optimization

### Token Efficiency
- Default to Serena symbol operations (more efficient than native search)
- Use Morphllm for bulk edits (batch operations save tokens)
- Cache Context7 documentation lookups (90-day retention)
- Batch Tavily searches (5 parallel max)

### Execution Speed
- Sequential reasoning enables 2-3x faster complex analysis
- Parallel-first MCP execution (never sequential unless dependent)
- Serena memory persistence eliminates re-analysis overhead
- Morphllm batching reduces individual edit overhead

### Resource Management
```yaml
resource_limits:
  tavily:
    max_parallel: 5
    results_per_search: 10
    daily_limit: 100  # If applicable

  sequential:
    max_depth: 10
    timeout_per_thought: 2min

  serena:
    memory_cache: enabled
    auto_save: 30min intervals

  morphllm:
    batch_size: 10 files
    verify_mode: on
```

---

## Troubleshooting

### If MCP Server Unavailable
Use `--no-mcp` flag to fall back to native reasoning:
```bash
/sc:research --no-mcp "Research topic"
```

### If Token Budget Exceeded
Enable ultra-compression:
```bash
/sc:task --uc "Task description"
```

### If Serena Memory Corrupted
Force fresh session:
```bash
/sc:load --force-new
```

---

## Integration Best Practices

1. **Start with Primary MCPs**: Get core research and implementation working
2. **Add Secondary MCPs**: Enhance with documentation and testing
3. **Monitor Performance**: Track token usage and execution time
4. **Optimize Iteratively**: Batch operations, cache results, parallelize

2. **Always Use Context7**: For framework-specific patterns
3. **Leverage Serena Memory**: Build cross-session learning
4. **Batch Operations**: Use Morphllm for >1 file changes

---

**MCP Integration transforms Linguistic Bridges from isolated AI into connected intelligent system with external knowledge, reasoning, and tools.**
