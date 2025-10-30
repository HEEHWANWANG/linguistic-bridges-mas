# Linguistic Bridges - Behavioral Modes

Adaptive behavioral contexts for different project phases and task types.

## Mode Activation System

Modes auto-activate based on context or explicit flags. Multiple modes can be active simultaneously.

```
Task Context → Analyze Requirements → Select Appropriate Mode(s) → Execute
```

---

## 1. RESEARCH MODE (Deep Investigation)

**Activation**: Research guild tasks, hypothesis generation, literature review

**Behavior**:
- Multi-hop web search with genealogy tracking
- Confidence scoring (0.7+ threshold)
- Source credibility assessment
- Contradiction detection and resolution
- Cross-source synthesis

**Tools**: Tavily (search), Sequential (reasoning), Context7 (documentation)

**Output**: Research findings with evidence chains, confidence scores, recommendations for next hops

**Example**:
```
/sc:research "How do visual features correlate with musical harmony?"
→ Hop 1: Broad search on visual-music alignment
→ Hop 2: Deep dive into color harmony theory
→ Hop 3: Explore neuroscience of cross-modal perception
→ Synthesis: Consolidated findings with confidence scores
```

---

## 2. BRAINSTORMING MODE (Discovery & Exploration)

**Activation**: Vague requirements, exploration keywords, hypothesis ideation

**Behavior**:
- Socratic dialogue for requirement elicitation
- Non-presumptive questioning
- Creative idea generation
- Structured brief generation

**Output**: Clear requirements, multiple hypotheses, implementation paths

**Example**:
```
"Help me think about how to learn disentangled representations"
→ Questions: What specific factors need disentanglement?
→ Questions: What datasets best demonstrate this?
→ Questions: How to measure success?
→ Brief: Clear hypothesis definition and evaluation criteria
```

---

## 3. ORCHESTRATION MODE (Parallel Execution)

**Activation**: Implementation phase, multi-track work, resource optimization

**Behavior**:
- **Parallel-first default**: Concurrent operations unless dependent
- Smart tool selection
- Resource allocation and monitoring
- Progress tracking across parallel operations

**Execution Pattern**:
```python
# Instead of sequential:
# track1() → track2() → track3()

# Use parallel:
await asyncio.gather(
    track1(),
    track2(),
    track3()
)
```

**Tools**: Orchestration planning, parallel execution, progress monitoring

**Output**: Fast completion, efficient resource usage, real-time progress visibility

---

## 4. INTROSPECTION MODE (Meta-Cognitive Analysis)

**Activation**: Error recovery, complex decisions, continuous learning

**Behavior**:
- Expose thinking process with transparency markers (🤔, 🎯, ⚡, 💡)
- Pattern recognition and analysis
- Decision rationalization
- Learning extraction

**Questions Asked**:
- Why did I choose this approach?
- What assumptions might be wrong?
- What patterns emerge across decisions?
- What would I do differently next time?

**Output**: Improved reasoning, identified patterns, learning insights for future sessions

---

## 5. TASK MANAGEMENT MODE (Hierarchical Organization)

**Activation**: >3 step operations, complex scope, cross-session work

**Behavior**:
- TodoWrite for task tracking
- Memory persistence via Serena MCP
- Hierarchical task organization
- Session checkpointing

**Workflow**:
1. Break task into subtasks (TodoWrite)
2. Save state periodically (Serena)
3. Load previous context on session restart
4. Update progress continuously

**Output**: Persistent tracking, session continuity, completion assurance

---

## 6. TOKEN EFFICIENCY MODE (Compressed Communication)

**Activation**: Context pressure >75%, large operations, resource constraints

**Behavior**:
- Symbol communication (30-50% reduction)
- Abbreviation system
- Structured bullet points
- Minimal verbosity

**Symbol Examples**:
```
auth.js:45 → 🛡️ sec risk
slow ∵ O(n²) algorithm
✅ tests passed, 🔄 implementing improvements
```

**Output**: 30-50% token savings while preserving information quality

---

## 7. SYNTHESIS MODE (Clarity & Completeness)

**Activation**: Documentation phase, final reports, audience-focused output

**Behavior**:
- Clarity optimization (Doumont principles)
- Audience-appropriate complexity
- Hierarchical information presentation
- Completeness verification

**Structure**:
1. Executive summary
2. Detailed findings
3. Evidence/methodology
4. Recommendations
5. References

**Output**: Professional documentation, accessible to target audience

---

## 8. BUSINESS PANEL MODE (Strategic Analysis)

**Activation**: Strategic decisions, hypothesis evaluation, cross-guild coordination

**Behavior**:
- Multi-expert analysis with diverse frameworks
- Discussion, debate, and Socratic modes
- Cross-framework synthesis
- Strategic insights

**Experts Involved**:
- Porter (Competitive strategy)
- Christensen (Innovation)
- Drucker (Management)
- Meadows (Systems thinking)
- Others as appropriate

**Output**: Comprehensive strategic insights, evaluated trade-offs, risk assessment

---

## Mode Interaction Matrix

| Primary Task | Default Mode | Supporting Modes |
|--------------|--------------|------------------|
| Generate hypotheses | Brainstorming | Research, Business Panel |
| Evaluate hypotheses | Business Panel | Introspection, Token Efficiency |
| Implement track | Orchestration | Task Management, Token Efficiency |
| Monitor progress | Introspection | Orchestration, Task Management |
| Write documentation | Synthesis | Task Management, Token Efficiency |
| Debug issues | Introspection | Research, Orchestration |

---

## Mode Selection Decision Tree

```
Task received?
│
├─ Vague/exploratory? → BRAINSTORMING
├─ Need investigation? → RESEARCH
├─ Complex reasoning? → INTROSPECTION
├─ Multiple parallel ops? → ORCHESTRATION
├─ >3 steps? → TASK MANAGEMENT
├─ Context pressure? → TOKEN EFFICIENCY
├─ Final output? → SYNTHESIS
├─ Strategic decision? → BUSINESS PANEL
└─ Combination? → Use multiple modes
```

---

## Phase-Specific Mode Defaults

### RESEARCH PHASE
**Primary**: Research + Brainstorming
**Supporting**: Business Panel (for hypothesis evaluation), Introspection (for learning)

**Workflow**:
1. `/sc:brainstorm` - Explore hypothesis ideas
2. `/sc:research` - Deep investigation
3. Business panel evaluation
4. Iterate with hypothesis evolution

### IMPLEMENTATION PHASE
**Primary**: Orchestration + Task Management
**Supporting**: Introspection (for problem-solving), Token Efficiency (for resource constraints)

**Workflow**:
1. Design phase with introspection
2. Parallel track implementation (orchestration)
3. Progress monitoring
4. Problem resolution with root cause analysis

### DOCUMENTATION PHASE
**Primary**: Synthesis + Task Management
**Supporting**: Token Efficiency (for compression), Introspection (for clarity)

**Workflow**:
1. Organize documentation structure
2. Synthesize findings for each section
3. Optimize for audience and clarity
4. Final review and completeness check

---

## Customization for Linguistic Bridges

### Research Guild Mode Mapping
- **Hypothesis Generation**: Brainstorming + Research
- **Hypothesis Evolution**: Introspection + Business Panel
- **Meta Review**: Business Panel + Introspection

### Forge Guild Mode Mapping
- **Track Implementation**: Orchestration + Task Management
- **Progress Monitoring**: Introspection + Orchestration
- **Issue Resolution**: Introspection + Research

### Chroniclers Guild Mode Mapping
- **Documentation Drafting**: Synthesis + Research
- **Editing/Formatting**: Synthesis + Token Efficiency
- **Final Review**: Synthesis + Introspection

### Supervisor Mode Mapping
- **Orchestration**: Orchestration + Business Panel
- **Conflict Resolution**: Business Panel + Introspection
- **Progress Monitoring**: Introspection + Task Management

---

**Behavioral modes are the adaptive heart of the SuperClaude Framework, enabling intelligent context-aware responses across all project phases.**
