# HarmonicVisuals: Competitive AI Conference Research Design

Quick reference guide for the narrative thumbnail generation research contribution.

---

## What Is HarmonicVisuals?

A **multi-agent system that generates narrative-driven image thumbnails for pop music** by having specialized agents analyze different musical dimensions and collaborate to create coherent visual stories.

**Key Innovation**: Unlike previous music visualization approaches, this system:
1. Uses heterogeneous agents with different expertise
2. Explicitly preserves "artistic outliers" (creative divergence) rather than forcing consensus
3. Iteratively refines prompts based on agent feedback
4. Models narrative arc across entire song sections

---

## The Core Idea

### Problem
Music videos need interesting visual thumbnails, but:
- Current methods don't understand music's narrative structure
- They miss emotional arcs and story progression
- They treat all musical perspectives equally

### Solution
**Four specialized agents analyze the song from different angles**:

1. **Technical Agent**
   - Analyzes rhythm, structure, form (intro, verse, chorus, bridge, outro)
   - Detects pattern changes, intensity curves
   - Output: "This is the climactic chorus moment - maximum intensity"

2. **Emotional Agent**
   - Interprets emotional trajectory (happy→sad, calm→excited)
   - Analyzes psychoacoustic features
   - Output: "This moment is euphoric and triumphant"

3. **Narrative Agent**
   - Extracts story/theme elements from lyrics and genre
   - Identifies narrative themes (love, journey, celebration, etc.)
   - Output: "This is a moment of transformation and achievement"

4. **Artistic Agent**
   - Proposes creative, unconventional interpretations
   - Suggests novel visual metaphors
   - **Special role**: Preserves perspective when creative disagreement exists
   - Output: "Instead of literal triumph, show abstract color flows representing emotional intensity"

### Consensus + Creativity
Normally multi-agent systems force agents to agree. HarmonicVisuals does something different:

```
70% Consensus (what all agents mostly agree on)
30% Creative Outliers (novel ideas from artistic agent that enhance creativity)
↓
Final Visual Narrative (coherent + creative)
```

### Iterative Refinement
The process doesn't stop at one attempt:

```
Agents propose narrative
↓
System generates image from proposed narrative
↓
Agents evaluate: "Does image match narrative?"
↓
If not aligned: Agents refine narrative (more specific, clearer constraints)
↓
System generates new image
↓
Repeat until image matches narrative (or max iterations)
```

---

## Why This Is Competitive

### Research Contributions

#### 1. **Heterogeneous Agent Architecture**
- **What's novel**: Different agents with different knowledge/capabilities
- **Why it matters**: Most MARL assumes all agents are identical; music understanding requires different expertise
- **Evidence**: Ablation studies will show each agent type contributes unique value

#### 2. **Artistic Outlier Preservation**
- **What's novel**: Explicitly preserve creative disagreement (vs. forcing consensus)
- **Why it matters**: Creative tasks benefit from diverse perspectives; challenges core MARL assumptions
- **Evidence**: Human evaluation will show outlier-enhanced images are more creative without losing coherence

#### 3. **Iterative Prompt Refinement**
- **What's novel**: Agents evaluate generated images and refine prompts
- **Why it matters**: Closes feedback loop between symbolic reasoning (agents) and neural generation (diffusion models)
- **Evidence**: Iteration metrics will show alignment improves over refinement rounds

#### 4. **Song Structure Awareness**
- **What's novel**: Models entire song's narrative arc, not just isolated moments
- **Why it matters**: Creates "visual story" with coherent progression
- **Evidence**: Users will perceive stronger narrative coherence across image sequence

### Research Gaps Addressed

From literature analysis:

| Gap | Problem | LB's Solution |
|-----|---------|---------------|
| **#2: Heterogeneous Agents** | All agents identical | Different agents (Technical, Emotional, Narrative, Artistic) |
| **#3: LLM Integration** | Limited MARL+LLM work | Uses LLMs for music understanding |
| **#8: Real-World Apps** | MARL stays in simulation | Actual thumbnail generation for songs |
| **Multimodal (Emerging)** | Music understanding monolithic | Combines music + visual + language |

### Competitive Advantages

1. **Novel application domain** (music-to-visual) - first major work in this area
2. **Addresses multimodal understanding** - increasingly valued by top venues
3. **Clear real-world value** - could deploy for music creators
4. **Challenges fundamental assumptions** - outlier preservation is philosophically interesting
5. **Explainable outputs** - each image has agent-generated narrative rationale

---

## Publication Strategy

### Primary Target: AAMAS 2026
**Why AAMAS**:
- Focuses on agents as first-class entities ✅
- Values multi-agent coordination ✅
- Welcomes real-world applications ✅
- 25% acceptance rate (good for competitive work)

**Paper title**: "HarmonicVisuals: Heterogeneous Multi-Agent Music Analysis for Narrative-Driven Visual Generation"

**Submission deadline**: June 2025
**Decision date**: October 2025

### Backup Venues (in priority order)
1. IJCAI 2026 (15% acceptance, broad technical excellence)
2. AAAI 2026 (20% acceptance, creative AI applications)
3. ICLR 2026 (25% acceptance, if emphasizing architecture)
4. ICML 2026 (22% acceptance, if emphasizing methodology)

### Tier-1 Expansion
After AAMAS publication, develop theoretical extensions for NeurIPS:
- Formal analysis of outlier preservation mechanism
- Convergence guarantees with creative disagreement
- Game-theoretic analysis of agent incentives

---

## Experimental Design

### Dataset: PopMusic-Narrative
- 50 diverse pop songs (various genres, emotions, structures)
- Each song: 5 sections (intro, verse, chorus, bridge, outro)
- Professional annotations: 1-2 reference images per section
- Total: 250 reference images created by professional designers

### Baselines (What We Compare Against)
1. **Single-Agent**: Traditional waveform visualization
2. **LLM-Only**: ChatGPT generates prompts (no agent coordination)
3. **Retrieval**: Find existing images matching themes (no generation)

### Evaluation Metrics

**Automatic Metrics**:
- Alignment score (how well image matches music moment)
- Coherence score (does image sequence tell coherent story?)
- Creativity score (novelty and diversity of image)

**Human Evaluation** (100 participants):
- Rate on 5-point scales: alignment, emotional resonance, narrative fit, artistic quality, creativity
- Comparative: HarmonicVisuals vs. baselines (which is better?)

### Expected Results
- **H1**: HarmonicVisuals > Baselines on alignment (agent coordination helps)
- **H2**: HarmonicVisuals high on both creativity AND coherence (outliers help without breaking structure)
- **H3**: Iterative refinement improves alignment (feedback loop works)
- **H4**: All agents matter (heterogeneity is valuable)

---

## Timeline to Publication

### Q4 2025 (8 weeks): Foundation & Proof-of-Concept
- Finalize agent architecture
- Implement basic system
- Run pilot experiment on 5-10 songs
- Debug and refine

**Gate**: System works end-to-end, pilot results promising

### Q1 2026 (13 weeks): Core Research
- Collect dataset (50 songs + annotations)
- Run full experiments (all methods on all songs)
- Conduct human evaluation (100 participants)
- Analyze results statistically

**Gate**: Clear results showing HarmonicVisuals advantages

### Q2 2026 (13 weeks): Paper Writing & Submission
- Write paper (8 pages for AAMAS format)
- Internal review and revisions
- Prepare supplementary materials
- **Submit to AAMAS** (June 2025 deadline)

**Gate**: Paper meets conference standards

### Q3 2026 (13 weeks): Review Response
- Receive reviewer feedback
- Address concerns / implement revisions
- Prepare response letter
- Resubmit if needed

### Q4 2026 (9 weeks): Publication Finalization
- Camera-ready version
- Plan follow-up work (extensions, new applications)

---

## Why This Research Design Is Strong

### ✅ Technical Soundness
- Clear agent architecture with well-defined roles
- Concrete algorithms (outlier preservation, prompt refinement)
- Rigorous evaluation (automatic + human, multiple baselines)
- Proper controls and ablations

### ✅ Clear Novelty
- First work on music-to-visual with agent coordination
- Outlier preservation is novel mechanism
- Iterative refinement novel for generation task
- Addresses multiple research gaps simultaneously

### ✅ Real-World Value
- Tangible application (thumbnail generation)
- Market potential (music platforms, creators, education)
- Accessibility (democratizes design work)
- Practical deployment path

### ✅ Strategic Positioning
- Perfect fit for AAMAS (agent-centric venue)
- Addresses research gaps identified in literature analysis
- Multimodal work increasingly valued
- Application-focused papers have higher impact

### ✅ Execution Feasibility
- Clear 13-month timeline with milestones
- Guild responsibilities well-defined
- Resources: music features, LLM APIs, image generation APIs (all accessible)
- Pilot experiment early to catch issues

---

## Key Innovations Summary

| Innovation | What's New | Why It Matters |
|-----------|-----------|----------------|
| **Heterogeneous agents** | Different agents with different expertise | Mirrors how humans understand music |
| **Outlier preservation** | Creative disagreement as feature | Enhances creative outcomes |
| **Iterative refinement** | Agents evaluate + improve outputs | Symbolic reasoning meets neural generation |
| **Structure awareness** | Narrative arc across song | Visual storytelling, not isolated frames |

---

## Quick Comparison: HarmonicVisuals vs. Baselines

| Aspect | Single-Agent | LLM-Only | Retrieval | HarmonicVisuals |
|--------|-------------|----------|-----------|-----------------|
| **Musical Understanding** | Shallow | Moderate | Thematic only | Deep (4 dimensions) |
| **Agent Coordination** | N/A | N/A | N/A | Yes |
| **Creative Diversity** | Low | Medium | Limited | High (with outliers) |
| **Narrative Coherence** | Low | Medium | Medium | High |
| **Alignment with Music** | Low | Medium | Medium | High (iterative) |
| **Explainability** | No | Partial | Yes | Full (agent narratives) |

---

## Next Steps

1. **Immediately** (This week):
   - Finalize agent architectures in detail
   - Implement music analysis modules
   - Set up development environment

2. **Q4 2025** (Next 8 weeks):
   - Complete baseline implementations
   - Run pilot experiment (5-10 songs)
   - Refine agent prompts based on pilot

3. **Q1 2026**:
   - Collect full dataset
   - Run comprehensive experiments
   - Conduct human evaluation

4. **Q2 2026**:
   - Write paper
   - Submit to AAMAS (June deadline)

5. **Q3-Q4 2026**:
   - Handle reviewer feedback
   - Finalize publication
   - Plan follow-up work

---

## Expected Impact

### For AI Community
- **Novel perspective**: Creative disagreement in MARL (challenges assumptions)
- **Multimodal innovation**: Integrates music + visual + language
- **Heterogeneous agents**: Shows value of agent specialization
- **Real-world applications**: MARL can solve creative tasks

### For Music Community
- **Accessible tools**: Democratize thumbnail/visualization creation
- **Artist empowerment**: Tools that respect musical understanding
- **Artistic expression**: System that values creative perspectives
- **Educational**: Music understanding through agent specialization

### For Society
- **Accessibility**: Visual content for music (benefits blind/deaf community)
- **Creativity**: AI that enhances human creativity, not replaces it
- **Cultural expression**: Celebrates diverse musical perspectives

---

## Document Reference

- **Full design**: See `NARRATIVE_THUMBNAIL_RESEARCH_DESIGN.md`
- **Publication strategy**: See `LINGUISTIC_BRIDGES_PUBLICATION_STRATEGY.md`
- **Research roadmap**: See `RESEARCH_ROADMAP_2025-2026.md`
- **Literature context**: See `MULTIAGENT_SYSTEMS_LITERATURE_ANALYSIS.md`

---

*Research Design Summary: October 30, 2025*
*Target Publication: AAMAS 2026 (Submission June 2025)*
*Status: Ready for Q4 2025 execution*
*Competitive Level: High (addresses gaps, novel approach, real-world application)*
