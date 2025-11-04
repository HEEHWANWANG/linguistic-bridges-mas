# HarmonicVisuals System Architecture for Q1 2026 Implementation

**Date**: November 4, 2025
**Phase**: Forge Guild Implementation (Q1 2026, 7 weeks)
**Purpose**: Complete technical architecture for MAS creativity-grounded music-visual system
**Status**: Implementation-ready specifications

---

## I. Executive Summary

### System Overview
HarmonicVisuals is a **compositional multi-agent system** that generates music video thumbnails by coordinating heterogeneous agents across three modalities:

1. **Linguistic Modality**: Extract narrative, emotion, concepts from lyrics
2. **Visual Modality**: Generate coherent, creative images matching linguistic intent
3. **Multi-Modal Coordination**: Debate and critique across modalities to prevent homogenization

### MAS Creativity Grounding
The architecture implements three core MAS creativity mechanisms:
- **Heterogeneous Specialization**: 5 distinct Designer roles (Narrative, Mood, Style, Conceptual, Commercial)
- **Structured Debate**: Reference search agents ↔ Design agents ↔ Image generation feedback loop
- **Controlled Dissent**: 70% consensus + 30% creative alternatives in final synthesis

### Expected Outcomes (Q1 2026)
- **Novelty**: 0.81 diversity score (vs 0.77 single-agent ceiling)
- **Quality**: 0.90 CLIP semantic alignment (vs 0.78 baseline)
- **Speed**: 3× faster iteration cycles (20 min vs 60 min for refinement)
- **Reusability**: Same architecture transfers to poetry, film scripts, etc.

---

## II. System Architecture (High-Level)

### Three-Layer MAS Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ LAYER 3: SUPERVISOR AGENT                                    │
│ - Orchestrates all phases (research complete)               │
│ - Coordinates linguistic, visual, and debate flows          │
│ - Monitors convergence and triggers refinement loops        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2: GUILD-LEVEL AGENTS (Specialized Expertise)          │
│                                                              │
│ LINGUISTIC GUILD              VISUAL GUILD                  │
│ ├─ Narrative Parser           ├─ Reference Searcher         │
│ ├─ Mood Analyzer              ├─ 5 Designer Agents:         │
│ ├─ Concept Mapper             │  ├─ Narrative Designer       │
│ ├─ Semantic Encoder           │  ├─ Mood Designer           │
│ └─ Evaluation Agent           │  ├─ Style Designer          │
│                               │  ├─ Conceptual Designer     │
│                               │  └─ Commercial Designer     │
│                               ├─ Prompt Generator           │
│                               └─ Image Generator            │
│                                                              │
│ COORDINATION AGENTS                                         │
│ ├─ Debate Moderator                                         │
│ ├─ Consensus Builder                                        │
│ └─ Dissent Preserver (30% creative alternatives)           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: FOUNDATION SERVICES                                │
│ ├─ MCP Manager (Claude API, image generation APIs)         │
│ ├─ Shared Memory (research findings, design decisions)     │
│ ├─ Metrics Engine (CLIP, diversity scoring, human eval)   │
│ └─ Logging & Monitoring                                    │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow: From Lyrics to Thumbnail

```
INPUT: Song Lyrics
  ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: LINGUISTIC UNDERSTANDING (Narrative Guild)         │
│                                                              │
│ Narrative Parser → Extract: story arc, character journey    │
│ Mood Analyzer → Extract: emotional progression, intensity   │
│ Concept Mapper → Map to visual descriptors                 │
│ Semantic Encoder → Create semantic embeddings              │
│                                                              │
│ OUTPUT: Linguistic representations (structured)            │
└─────────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: VISUAL DESIGN PROPOSAL (Visual Guild)             │
│                                                              │
│ 5 Designer Agents propose visual directions:                │
│ • Narrative Designer: How to visualize the story?          │
│ • Mood Designer: Color palette, lighting, intensity?       │
│ • Style Designer: Artistic medium, visual language?        │
│ • Conceptual Designer: Abstract concepts → visual form?    │
│ • Commercial Designer: Appeal, novelty, marketability?     │
│                                                              │
│ OUTPUT: 5 parallel design proposals                        │
└─────────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3: REFERENCE SEARCH & GROUNDING                      │
│                                                              │
│ Reference Searcher queries:                                │
│ • Unsplash/Pexels: Visual references matching proposals    │
│ • Image analysis: Extract dominant patterns                │
│ • Novelty filtering: Avoid clichés                         │
│                                                              │
│ OUTPUT: References + novelty metrics                       │
└─────────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4: DEBATE & CRITIQUE (Multi-Modal)                   │
│                                                              │
│ Linguistic agents evaluate proposals:                       │
│ "Does this design capture the lyrics' meaning?"            │
│ "Is mood consistent with emotional arc?"                   │
│                                                              │
│ Visual agents defend/refine:                               │
│ "Here's how we incorporated your feedback..."              │
│                                                              │
│ Repeat 2-3 rounds until convergence                        │
│                                                              │
│ OUTPUT: Refined design consensus + dissenting views        │
└─────────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 5: PROMPT GENERATION & SYNTHESIS                     │
│                                                              │
│ 70% Consensus Path:                                        │
│ • Merge 70% of agent proposals (most aligned)             │
│ • Generate unified visual prompt                           │
│                                                              │
│ 30% Dissent Paths (Creative Alternatives):                │
│ • Preserve 2-3 dissenting minority views                  │
│ • Generate alternative prompts                             │
│                                                              │
│ OUTPUT: 1 primary prompt + 2-3 alternative prompts        │
└─────────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 6: IMAGE GENERATION                                   │
│                                                              │
│ Image Generator (DALL-E 3 / Midjourney / Flux):            │
│ • Primary: Generate from 70% consensus prompt              │
│ • Alternatives: Generate from 30% dissent prompts          │
│                                                              │
│ OUTPUT: 3 candidate thumbnail images                       │
└─────────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 7: EVALUATION & SELECTION                            │
│                                                              │
│ Metrics calculation:                                        │
│ • CLIP alignment: How well does image match lyrics?        │
│ • Diversity: How different are the 3 candidates?           │
│ • Novelty: How original is the concept?                    │
│                                                              │
│ Selection:                                                  │
│ • If primary image has CLIP > 0.85: Select primary        │
│ • Else: Evaluate alternatives                              │
│ • Human preference (tie-breaker)                           │
│                                                              │
│ OUTPUT: Final thumbnail + metadata                         │
└─────────────────────────────────────────────────────────────┘
```

---

## III. Detailed Agent Specifications

### LAYER 2a: Linguistic Guild

#### 1. Narrative Parser Agent

**Purpose**: Extract narrative structure from song lyrics

**Input**: Raw lyrics text

**Output**: Structured narrative representation
```json
{
  "narrative_arc": {
    "setup": "Describes initial situation",
    "conflict": "Main tension or challenge",
    "climax": "Peak emotional moment",
    "resolution": "How situation concludes"
  },
  "character_journey": {
    "protagonist": "Main character description",
    "transformation": "How character changes",
    "emotional_state": ["initial_emotion", "middle_emotion", "final_emotion"]
  },
  "key_events": [
    {"time_marker": "Verse 1", "event": "Character introduction"},
    {"time_marker": "Chorus", "event": "Theme emphasis"}
  ]
}
```

**Implementation**:
```python
class NarrativeParser(BaseAgent):
    async def extract_narrative(self, lyrics: str) -> Dict:
        # Use Claude/LLM to extract structure
        prompt = f"""Analyze these lyrics and extract:
        1. Narrative arc (setup, conflict, climax, resolution)
        2. Character journey and transformation
        3. Key events by song section

        Lyrics: {lyrics}

        Return JSON with structure..."""

        response = await self.mcp_manager.get_mcp("llm").execute(prompt)
        return json.loads(response)
```

#### 2. Mood Analyzer Agent

**Purpose**: Analyze emotional tone and progression

**Input**: Lyrics + Narrative structure

**Output**: Emotional metadata
```json
{
  "overall_mood": "melancholic, hopeful",
  "intensity_curve": [0.3, 0.5, 0.8, 0.6],  # Verse→Chorus→Chorus→Bridge
  "emotional_arc": [
    {"section": "Verse 1", "emotion": "loneliness", "intensity": 0.3},
    {"section": "Chorus", "emotion": "yearning", "intensity": 0.7}
  ],
  "color_associations": {
    "primary": "cool blues and grays",
    "accent": "warm amber light",
    "overall_palette": "cool-warm contrast"
  }
}
```

**Implementation**:
```python
class MoodAnalyzer(BaseAgent):
    async def analyze_mood(self, lyrics: str, narrative: Dict) -> Dict:
        prompt = f"""Analyze emotional journey:
        - Emotions by song section
        - Intensity progression (0-1 scale)
        - Associated colors and visual moods

        Context: {narrative}
        Lyrics: {lyrics}"""

        response = await self.mcp_manager.get_mcp("llm").execute(prompt)
        return json.loads(response)
```

#### 3. Concept Mapper Agent

**Purpose**: Extract visual concepts from linguistic meaning

**Input**: Lyrics, Narrative, Mood

**Output**: Visual concept list
```json
{
  "visual_concepts": [
    {"concept": "isolation", "visual_forms": ["empty space", "single subject", "high horizon line"]},
    {"concept": "journey", "visual_forms": ["leading lines", "depth", "path/road"]},
    {"concept": "hope", "visual_forms": ["light source", "opening/window", "upward composition"]}
  ],
  "must_include": ["figure walking", "natural lighting"],
  "should_avoid": ["clichéd sunset", "generic close-up"]
}
```

#### 4. Semantic Encoder Agent

**Purpose**: Create numerical embeddings for semantic grounding

**Input**: Concepts, mood, narrative

**Output**: Vector embeddings
```python
# Pseudocode
embeddings = {
    "semantic_vector": embed_text("lonely journey with hope"),  # 768-dim vector
    "emotional_vector": embed_text("melancholic yet uplifting"),
    "visual_intent": embed_text("isolation + light + movement")
}
```

#### 5. Linguistic Evaluation Agent

**Purpose**: Evaluate visual outputs for semantic alignment

**Input**: Original lyrics, Generated image

**Output**: Alignment score + critique
```json
{
  "clip_alignment_score": 0.87,
  "semantic_match": "Strong: captures isolation and light, weak: missing motion",
  "critique": "Good emotional match but too static. Original mentions 'running away'",
  "suggestion": "Add motion blur or dynamic composition"
}
```

---

### LAYER 2b: Visual Guild - Designer Agents

Each of the 5 Designer agents operates on the linguistic representations, proposing different visual interpretations:

#### Design Agent Architecture

```python
class DesignerAgent(BaseAgent):
    """Base class for all designer agents"""

    def __init__(self, designer_type: str, name: str, ...):
        super().__init__(name, ...)
        self.designer_type = designer_type
        self.system_prompt = self.get_designer_prompt()

    def get_designer_prompt(self) -> str:
        """Return role-specific system prompt"""
        if self.designer_type == "narrative":
            return """You are a narrative visual director...
                     Focus on: Story composition, scene structure, visual metaphor"""
        elif self.designer_type == "mood":
            return """You are a mood/aesthetic director...
                     Focus on: Color, lighting, emotional atmosphere"""
        # ... etc for each type

    async def propose_design(self, linguistic_input: Dict) -> Dict:
        """Propose visual direction"""
        prompt = f"""Given these lyrics and analysis:
        {linguistic_input}

        Propose a visual design emphasizing {self.designer_type} aspects.
        Provide: visual description, color palette, composition guidance,
        key elements, and novelty considerations."""

        response = await self.mcp_manager.get_mcp("llm").execute(prompt)
        return {
            "designer_type": self.designer_type,
            "proposal": response,
            "confidence_score": calculate_confidence(response)
        }
```

#### 1. Narrative Designer

**System Prompt**: Visual storyteller focused on narrative visualization
**Focus**: How to compose the story visually
**Output Example**:
```json
{
  "visual_narrative": "Open on isolated figure on road at dusk,
                       establish scale/loneliness, progress with motion",
  "composition": "Leading lines (road) pulling toward horizon,
                  figure positioned off-center for tension",
  "key_elements": ["road/path", "single figure", "expansive landscape"],
  "scene_structure": ["Wide establishing shot", "Detail/emotion", "Resolution"]
}
```

#### 2. Mood Designer

**System Prompt**: Aesthetic mood curator
**Focus**: How to create emotional resonance
**Output Example**:
```json
{
  "color_palette": {
    "primary": "deep twilight blue (#1a2b4d)",
    "secondary": "warm amber (#d4a574)",
    "accent": "pale gold highlights"
  },
  "lighting": "Warm key light (amber) against cool background,
               creating emotional contrast",
  "atmosphere": "Melancholic yet hopeful; cool dominates but warmth
                 emerges from key light"
}
```

#### 3. Style Designer

**System Prompt**: Visual language specialist
**Focus**: Artistic direction and medium
**Output Example**:
```json
{
  "visual_language": "Realistic with painterly treatment",
  "medium_suggestion": "Cinematic photography with digital enhancement",
  "art_direction": "Contemporary realistic but with subtle heightened color",
  "reference_aesthetic": "Nomads documentary meets atmospheric portrait photography"
}
```

#### 4. Conceptual Designer

**System Prompt**: Abstract-to-visual translator
**Focus**: How abstract concepts become visual metaphors
**Output Example**:
```json
{
  "abstract_concepts": {
    "isolation": "Visual: empty negative space, single focal point",
    "journey": "Visual: leading lines, progression, perspective depth",
    "hope": "Visual: light source, opening/window, upward energy"
  },
  "metaphor_suggestions": [
    {"concept": "running away", "visual": "motion blur, dynamic pose"},
    {"concept": "loneliness", "visual": "vast landscape dwarfing subject"}
  ]
}
```

#### 5. Commercial Designer

**System Prompt**: Pragmatic creative director
**Focus**: Appeal, novelty, marketability
**Output Example**:
```json
{
  "appeal_factors": "Relatable (everyone feels loneliness), visually stunning
                    (dramatic lighting), emotionally resonant",
  "novelty": "While loneliness is common theme, specific visual treatment
             (amber light against blue dusk) feels fresh",
  "potential_clichés": ["Generic sunset", "overused silhouette", "symmetrical composition"],
  "differentiation": "Use dynamic motion, asymmetrical composition,
                     unexpected color contrast"
}
```

---

### LAYER 2c: Supporting Visual Agents

#### Reference Searcher Agent

**Purpose**: Find visual references matching designer proposals

**Implementation**:
```python
class ReferenceSearcher(BaseAgent):
    async def search_references(self, design_proposals: List[Dict]) -> Dict:
        """Search Unsplash/Pexels for matching references"""

        for proposal in design_proposals:
            # Extract visual concepts
            concepts = extract_concepts(proposal)

            # Build search query
            query = build_search_query(concepts)
            # e.g., "isolated figure road golden light"

            # Search APIs
            results = await parallel_search([
                search_unsplash(query),
                search_pexels(query)
            ])

            # Analyze results for novelty
            novelty_scores = score_novelty(results)

            # Filter out clichés
            filtered = filter_cliches(results, novelty_scores)

            return {
                "designer_type": proposal["designer_type"],
                "references": filtered,
                "search_query": query,
                "novelty_assessment": "High diversity, avoids common clichés"
            }
```

#### Prompt Generator Agent

**Purpose**: Convert design decisions into detailed image prompts

**Input**: Design proposals + linguistic representations + references

**Output**: Optimized prompts for image generation
```python
class PromptGenerator(BaseAgent):
    async def generate_prompts(self, design_context: Dict) -> Dict:
        """
        Convert design proposals into prompts for DALL-E/Midjourney
        """

        # Merge designs into consensus + alternatives
        consensus = merge_designs_70_percent(design_context["proposals"])
        dissenting = extract_dissenting_views_30_percent(design_context["proposals"])

        # Primary prompt (70% consensus)
        primary_prompt = self.build_prompt(
            narrative=consensus["narrative"],
            mood=consensus["mood"],
            style=consensus["style"],
            concepts=consensus["concepts"],
            commercial=consensus["commercial"],
            references=design_context["references"]
        )

        # Alternative prompts (30% dissent preserved)
        alternative_prompts = [
            self.build_prompt(**dissenting[i]) for i in range(len(dissenting))
        ]

        return {
            "primary_prompt": primary_prompt,
            "alternative_prompts": alternative_prompts,
            "prompt_metadata": {
                "consensus_strength": 0.70,
                "diversity_preserved": 0.30
            }
        }
```

---

### LAYER 2d: Coordination Agents

#### Debate Moderator Agent

**Purpose**: Facilitate multi-modal critique loop

**Process**:
```python
class DebateModerator(BaseAgent):
    async def run_debate_round(self, linguistic_eval: Dict,
                               design_proposals: List[Dict]) -> Dict:
        """
        Round of debate:
        1. Linguistic agents critique designs
        2. Visual agents respond
        3. Evaluate convergence
        """

        # Linguistic critique
        critiques = []
        for designer_output in design_proposals:
            critique = await self.linguistic_guild.evaluate(designer_output)
            critiques.append(critique)

        # Visual defense/refinement
        refinements = []
        for critique, proposal in zip(critiques, design_proposals):
            refinement = await proposal["agent"].refine_based_on_critique(critique)
            refinements.append(refinement)

        # Check convergence
        convergence_score = calculate_convergence(refinements, design_proposals)

        if convergence_score > 0.8 or rounds >= 3:
            return {"status": "converged", "final_proposals": refinements}
        else:
            # Schedule next round
            return {"status": "continue_debate", "round": 2, "refinements": refinements}
```

#### Consensus Builder Agent

**Purpose**: Identify 70% consensus from 5 agents

**Logic**:
```python
def build_consensus_70_percent(proposals: List[Dict]) -> Dict:
    """
    Find common ground among 70% of agents (min 4 of 5)
    """

    # Extract dimensions
    dimensions = {}
    for proposal in proposals:
        for key, value in proposal.items():
            if key not in dimensions:
                dimensions[key] = []
            dimensions[key].append(value)

    # For each dimension, find majority agreement
    consensus = {}
    for dimension, values in dimensions.items():
        # Count agreement (using semantic similarity)
        agreements = count_semantic_agreement(values)

        # If 4+ agents agree, that's consensus
        if len(agreements) >= 4:
            consensus[dimension] = {
                "agreed_value": agreements[0],
                "agreement_count": len(agreements),
                "consensus_strength": len(agreements) / 5
            }

    return consensus
```

#### Dissent Preserver Agent

**Purpose**: Protect 30% dissenting minority views

**Process**:
```python
def preserve_dissent_30_percent(proposals: List[Dict],
                                 consensus: Dict) -> List[Dict]:
    """
    Identify and preserve proposals that disagree with consensus
    """

    dissenting = []
    for i, proposal in enumerate(proposals):
        agreement_score = calculate_agreement_with_consensus(proposal, consensus)

        # If proposal disagrees on major dimensions, it's dissenting
        if agreement_score < 0.7:
            dissenting.append({
                "proposal": proposal,
                "dissent_type": identify_dissent_type(proposal, consensus),
                "uniqueness": 1.0 - agreement_score
            })

    # Keep top 2-3 most unique dissenting views
    return sorted(dissenting, key=lambda x: x["uniqueness"])[:3]
```

---

## IV. Data Structures & Schemas

### Core Data Models

```python
# Language representations
class LinguisticRepresentation:
    narrative_arc: Dict[str, str]
    mood_analysis: Dict[str, Any]
    concepts: List[str]
    semantic_embeddings: np.ndarray  # 768-dim
    confidence_scores: Dict[str, float]

# Design proposals
class DesignProposal:
    designer_type: str  # "narrative", "mood", "style", "conceptual", "commercial"
    visual_description: str
    key_elements: List[str]
    color_palette: Dict[str, str]
    confidence_score: float
    reason: str

# References
class VisualReference:
    source_url: str
    source_platform: str  # "unsplash", "pexels"
    visual_concepts: List[str]
    novelty_score: float
    matches_proposals: List[str]

# Prompts for generation
class GenerationPrompt:
    prompt_text: str
    designer_influences: List[str]  # Which designers influenced this
    consensus_level: float  # 0.70 for consensus, <0.70 for alternatives
    generation_model: str  # "dall-e-3", "midjourney", "flux"
    expected_dimensions: Tuple[int, int]  # Width x Height

# Final output
class ThumbnailOutput:
    image_url: str
    metadata: Dict
    metrics: Dict
    selection_rationale: str
```

---

## V. Implementation Timeline (Q1 2026, 7 weeks)

### Week 1: Foundation & Setup
- [ ] Set up development environment (Python, async framework, MCP integration)
- [ ] Implement BaseAgent class with MCP manager
- [ ] Create shared memory infrastructure
- [ ] Design data schemas and models

**Deliverable**: Project scaffolding, all base classes, data models

### Week 2: Linguistic Guild
- [ ] Implement Narrative Parser Agent
- [ ] Implement Mood Analyzer Agent
- [ ] Implement Concept Mapper Agent
- [ ] Implement Semantic Encoder Agent
- [ ] Create linguistic representation testing suite

**Deliverable**: Linguistic processing pipeline end-to-end

### Week 3: Visual Guild - Designers
- [ ] Implement 5 Designer Agent roles
- [ ] Create designer system prompts
- [ ] Implement proposal generation
- [ ] Create confidence scoring mechanism

**Deliverable**: 5 designer agents generating parallel proposals

### Week 4: Supporting Agents & Refinement
- [ ] Implement Reference Searcher Agent
- [ ] Implement Prompt Generator Agent
- [ ] Integrate Unsplash/Pexels APIs
- [ ] Implement novelty filtering

**Deliverable**: Full visual pipeline from design to generation

### Week 5: Coordination & Debate
- [ ] Implement Debate Moderator Agent
- [ ] Implement Consensus Builder (70%)
- [ ] Implement Dissent Preserver (30%)
- [ ] Create debate loop testing

**Deliverable**: Multi-modal debate mechanism fully functional

### Week 6: Integration & Baselines
- [ ] Integrate all agents with Supervisor
- [ ] Implement monolithic baseline (single model)
- [ ] Implement single-agent baseline
- [ ] Implement homogeneous MAS baseline
- [ ] Create evaluation metrics infrastructure (CLIP, diversity, novelty)

**Deliverable**: 4 implementations ready for comparison

### Week 7: Validation & Analysis
- [ ] Run comparative experiments (4 configurations × 50 songs)
- [ ] Calculate metrics (diversity, novelty, alignment, speed)
- [ ] Statistical analysis (ANOVA, effect sizes)
- [ ] Generate results tables and visualizations
- [ ] Draft method sections for both NLP and MARL papers

**Deliverable**: Complete experimental results with statistical analysis

---

## VI. Validation Plan

### Research Question 1: Heterogeneous Specialization
**Metric**: Diversity Score (Non-Duplicate Ratio)
**Target**: 0.81 (HarmonicVisuals) vs 0.77 (single-agent) vs 0.69 (baseline)
**Method**: CLIP embeddings, clustering analysis
**Samples**: 50 songs × 4 configurations = 200 images

### Research Question 2: Productive Dissent
**Metric**: Coherence-Novelty Pareto frontier
**Target**: 70/30 ratio achieves optimal frontier
**Method**: Measure both CLIP (coherence) and human ratings (novelty)
**Samples**: 50 songs × 4 dissent ratios (0%, 30%, 50%, 100%)

### Research Question 3: Multi-Modal Critique
**Metric**: Semantic Alignment + Error Recovery
**Target**: 0.90 CLIP, 50% error reduction
**Method**: Track alignment scores before/after critique rounds
**Samples**: 50 songs × 3 critique rounds

### Research Question 4: Modular Architecture
**Metric**: Iteration speed, quality, reusability
**Target**: 3× faster, +0.22 novelty, 336× faster domain transfer
**Method**: Time measurements, quality metrics, transfer learning experiments
**Samples**: 50 songs + 2 new domains (poetry, film scripts)

---

## VII. API Integrations Required

### Image Generation APIs
- **DALL-E 3**: Primary generation (best semantic understanding)
- **Midjourney**: Alternative (stronger aesthetic control)
- **Flux**: Open-source fallback

### Reference Search APIs
- **Unsplash**: Primary reference source
- **Pexels**: Secondary reference source

### Claude/LLM APIs
- **Claude 3.5 Sonnet**: Language understanding, design reasoning
- **Claude Vision**: Image analysis for references

### Evaluation Tools
- **OpenAI CLIP**: Image-text semantic alignment
- **Custom metrics**: Diversity (clustering), novelty (human eval)

---

## VIII. Success Criteria

### Performance Targets
- ✅ Diversity score: 0.81 (vs 0.77 single-agent ceiling)
- ✅ CLIP alignment: 0.90 (vs 0.78 baseline)
- ✅ Novelty improvement: +0.18 (measured on 0-100 scale)
- ✅ Iteration speed: 3× faster (20 min vs 60 min)
- ✅ Domain transfer: <1 hour (vs 2 weeks monolithic)

### Research Criteria
- ✅ All 4 research claims validated with p < 0.05
- ✅ Statistical significance confirmed (Cohen's d > 0.8)
- ✅ Results reproducible (code & data shared)
- ✅ Contributions clearly map to MAS creativity theory

### Publication Criteria
- ✅ ACL/EMNLP ready: Results demonstrated + theory grounded
- ✅ AAMAS/IJCAI ready: Novel MAS mechanisms with quantified improvement
- ✅ Dual-track strategy: Both NLP and MARL positioning viable
- ✅ Baseline comparisons: Include monolithic, single-agent, and MAS variants

---

## IX. Risk Mitigation

### Risk 1: API rate limits on image generation
**Mitigation**: Cache generated images, batch processing, fallback to Flux open-source

### Risk 2: CLIP alignment scores plateau
**Mitigation**: Include human evaluators in loop, validate metrics align with preference

### Risk 3: Debate loop fails to converge
**Mitigation**: Hard constraint: max 3 rounds, timeout fallback to consensus only

### Risk 4: 5 designer roles insufficient heterogeneity
**Mitigation**: Pre-planned expansion to 7-8 roles if diversity scores don't reach 0.81

### Risk 5: Multi-modal critique adds too much latency
**Mitigation**: Parallel execution of critique rounds, async processing

---

## X. Conclusion

This architecture instantiates **MAS creativity principles** (heterogeneity, debate, controlled dissent) in concrete implementation, designed for:

1. **Q1 2026 Validation**: 7-week implementation sprint with clear milestones
2. **Publication Readiness**: Both NLP and MARL venues have clear pathways
3. **Scalability**: Modular design enables domain transfer and extension
4. **Reproducibility**: Clear specifications enable peer review and replication

The system is ready for implementation upon approval of this architecture.

