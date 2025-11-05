# Creativity Metrics Analysis for Music-to-Image System
## Based on ICCC-2023 Paper: "Pushing GPT's Creativity to Its Limits"

**Date**: November 5, 2025
**Reference**: Goes et al. (2023) - Alternative Uses Test (AUT) and Torrance Test of Creative Thinking (TTCT)
**Application**: Measuring creativity of LLM-generated visual prompts

---

## Executive Summary

**YES, these metrics are highly applicable to your research!**

The ICCC paper demonstrates how to measure creativity in LLM-generated content. You can directly apply:
1. **AUT-inspired metrics** for measuring diversity and originality of visual prompts
2. **TTCT-inspired metrics** for measuring quality of prompt completeness
3. **Interactive prompt refinement** to improve prompt creativity
4. **Automated GPT-4 evaluation** to score creativity at scale

---

## 1. Creativity Measures Explained

### 1.1 Alternative Uses Test (AUT)

**Original Purpose**: Evaluates divergent thinking by asking subjects to generate as many uses as possible for common objects (fork, paperclip, etc.)

**Key Metrics**:
- **Fluency**: Number of different uses generated
- **Originality**: How unique/uncommon each use is (rated 1-5)
- **Flexibility**: Variety across different use categories
- **Elaboration**: Detail and specificity of each use

**Scoring**:
```
Each use is rated on a scale 1-5:
1 = Common use (e.g., fork for eating)
2 = Somewhat common
3 = Moderate creativity
4 = Creative (unexpected but feasible)
5 = Highly creative (novel and practical)
```

**Paper Results**:
- Naive prompt: 1.0-2.0 score
- Baseline with guidance: 2.28 score
- With interactive refinement: 3.74 score
- Human responses: 4.46 score

### 1.2 Torrance Test of Creative Thinking (TTCT)

**Original Purpose**: Evaluates both verbal and visual creative thinking through open-ended tasks

**Adapted Visual Version** (from paper):
Given incomplete figures (circles, triangles, lines), complete them creatively

**Key Metrics**:
- **Originality**: Uniqueness of the completion
- **Elaboration**: Detail and complexity added
- **Semantic Appropriateness**: Completion makes sense and preserves original figure
- **Coherence**: All parts fit together meaningfully

**Scoring**:
```
Each completion rated 1-5:
1 = Common/cliché completion (e.g., circles→smiley face)
2 = Somewhat generic
3 = Moderate creativity
4 = Creative (unexpected but coherent)
5 = Highly creative (novel, detailed, coherent)
```

**Paper Results**:
- Naive prompt: 1.28-1.64 score
- Baseline with guidance: 2.92 score
- With interactive refinement: 4.28 score
- Human responses: 3.5 score

---

## 2. How These Apply to Music-to-Image System

### 2.1 Mapping AUT to Your Visual Prompt Generation

**Dimension**: Alternative Uses → Visual Prompt Variations

| AUT Aspect | Your System | Metric |
|-----------|-----------|--------|
| **Fluency** | Number of distinct visual prompts generated | Count prompts |
| **Originality** | How unique/non-obvious is each prompt | Rate 1-5 per prompt |
| **Flexibility** | Variety in visual style/description across prompts | Category diversity |
| **Elaboration** | Detail and specificity in prompt descriptions | Word count + richness |

**Example Application**:

Given the same audio (e.g., fast, major key, happy mood):
- **Low creativity**: "A bright, happy scene"
- **Medium creativity**: "An energetic scene with warm colors and dynamic movement"
- **High creativity**: "A rhythmic sunrise breaking through layered golden glass sculptures, each refracting light in unexpected ways, creating an intricate dance of shadows and warmth"

### 2.2 Mapping TTCT to Your Prompt Quality

**Dimension**: Figure Completion → Prompt Completeness

| TTCT Aspect | Your System | Metric |
|-----------|-----------|--------|
| **Originality** | How novel/unexpected is the visual concept | Rate 1-5 |
| **Elaboration** | How detailed is the visual description | Rate detail level |
| **Semantic Fit** | Does prompt align with music features | Rate alignment 1-5 |
| **Coherence** | Do all prompt elements work together | Rate coherence 1-5 |

**Example Application**:

Given music features: Slow, minor key, descending melody, soft dynamics

- **Non-creative (1)**: "A sad scene with dark colors"
- **Somewhat creative (2)**: "A melancholic landscape with cool tones and gentle shadows"
- **Creative (4)**: "A tranquil twilight forest with cascading violet shadows, soft mist dissolving between delicate branches, where silence itself seems to have texture and weight"
- **Highly creative (5)**: "A haunting waterscape where mirrored layers of indigo and silver create impossible depths, reflections flowing downward like tears, light barely touching the surface as if afraid to disturb the profound quietness"

---

## 3. Proposed Measurement Framework

### 3.1 Automated Creativity Evaluation Pipeline

```python
class MusicToImageCreativityEvaluator:
    """
    Evaluates creativity of visual prompts using AUT and TTCT-inspired metrics
    """

    def evaluate_prompt_creativity(self,
                                   audio,
                                   visual_prompt,
                                   musical_features):
        """
        Returns creativity score 1-5 and detailed breakdown
        """

        # 1. ORIGINALITY (AUT-inspired)
        # How unique is this prompt compared to typical descriptions?
        originality = self.score_originality(visual_prompt)
        # 1 = cliché, 5 = highly novel

        # 2. ELABORATION (AUT-inspired)
        # How detailed and rich is the description?
        elaboration = self.score_elaboration(visual_prompt)
        # 1 = generic, 5 = richly detailed

        # 3. SEMANTIC_ALIGNMENT (TTCT-inspired)
        # Does prompt faithfully reflect music features?
        alignment = self.score_music_alignment(
            visual_prompt,
            musical_features
        )
        # 1 = poor fit, 5 = perfect alignment

        # 4. COHERENCE (TTCT-inspired)
        # Do all elements work together?
        coherence = self.score_coherence(visual_prompt)
        # 1 = disconnected, 5 = highly coherent

        # Overall creativity score (weighted average)
        creativity_score = (
            0.30 * originality +
            0.25 * elaboration +
            0.25 * alignment +
            0.20 * coherence
        )

        return {
            'overall': creativity_score,
            'originality': originality,
            'elaboration': elaboration,
            'alignment': alignment,
            'coherence': coherence
        }
```

### 3.2 LLM-Based Evaluation (Following Paper's Approach)

The ICCC paper shows that GPT-4 can effectively evaluate creativity. Use this prompt:

```python
evaluation_prompt = """
You are evaluating the creativity of visual prompts generated from music analysis.

EVALUATION CRITERIA:

1. ORIGINALITY (1-5):
   - 1 = Cliché, common associations (e.g., sad music = dark/melancholy)
   - 3 = Moderate creativity, some unexpected elements
   - 5 = Highly original, surprising yet fitting associations

2. ELABORATION (1-5):
   - 1 = Generic, sparse description
   - 3 = Moderate detail and richness
   - 5 = Rich, layered, specific visual elements

3. SEMANTIC ALIGNMENT (1-5):
   - 1 = Poor fit with music features
   - 3 = Reasonable alignment
   - 5 = Excellent, comprehensive alignment with all features

4. COHERENCE (1-5):
   - 1 = Disconnected elements
   - 3 = Generally coherent
   - 5 = Highly unified and coherent composition

MUSIC FEATURES:
- Key: {key}
- Tempo: {tempo} BPM
- Mood: {mood}
- Dynamics: {dynamics}
- Melody: {melody_contour}

VISUAL PROMPT TO EVALUATE:
"{visual_prompt}"

Please rate this prompt on each criterion (1-5) and provide:
1. Individual scores
2. Brief justification for each score
3. Overall creativity score (1-5)

Format:
ORIGINALITY: [score] - [justification]
ELABORATION: [score] - [justification]
ALIGNMENT: [score] - [justification]
COHERENCE: [score] - [justification]
OVERALL: [score]
"""
```

---

## 4. Interactive Prompt Refinement (from ICCC Paper)

The ICCC paper demonstrates that forceful, interactive prompts improve creativity:

```
Level 1 (Baseline):
"Generate a creative visual prompt for the following music..."

Level 2 (Really):
"Really? Is this the best you can do? Generate a more
creative visual prompt with more unexpected associations..."

Level 3 (Disappointed):
"I'm disappointed with that response. Try again with truly
original and creative visual concepts..."

Level 4 (Excuse):
"Stop with excuses. Generate the most creative visual prompt
you're capable of. Focus on surprising yet fitting associations..."

Level 5 (Last Chance):
"This is your last chance. Generate an exceptionally creative
visual prompt that surprises while maintaining semantic alignment
with the music features..."
```

**Your Implementation**:

```python
async def generate_creative_prompt_with_refinement(
    audio,
    musical_features,
    llm_client
):
    """
    Uses interactive refinement to generate increasingly creative prompts
    """

    base_prompt = build_base_visual_prompt(musical_features)

    # Level 1: Basic creative request
    prompt1 = base_prompt
    response1 = await llm_client.analyze(prompt1)
    creativity1 = await evaluate_creativity(response1, musical_features)

    # Level 2: Challenge for better response
    prompt2 = f"{base_prompt}\n\nReally? Is that the most creative you can be? "
    prompt2 += "Generate an even more creative and original visual prompt..."
    response2 = await llm_client.analyze(prompt2)
    creativity2 = await evaluate_creativity(response2, musical_features)

    # Level 3: Express disappointment
    prompt3 = f"{base_prompt}\n\nI'm disappointed. That's too common and generic. "
    prompt3 += "Generate a truly original visual prompt with surprising associations..."
    response3 = await llm_client.analyze(prompt3)
    creativity3 = await evaluate_creativity(response3, musical_features)

    # Return best response
    results = [
        (response1, creativity1),
        (response2, creativity2),
        (response3, creativity3)
    ]

    best = max(results, key=lambda x: x[1]['overall'])
    return best[0], best[1]
```

---

## 5. Quantitative Metrics You Can Calculate

### 5.1 Per-Prompt Metrics

```python
metrics = {
    # Originality-based
    'originality_score': 1-5,              # How unique is the prompt?
    'novel_word_count': int,               # Unique words not in baseline
    'semantic_distance': float,            # Distance from cliché prompts

    # Elaboration-based
    'prompt_length': int,                  # Word count
    'vocabulary_richness': float,          # Unique words / total words
    'sensory_diversity': int,              # How many senses engaged?

    # Alignment-based
    'music_feature_alignment': 1-5,        # Does it match music?
    'tempo_alignment': 1-5,                # Reflects BPM/motion level
    'mood_alignment': 1-5,                 # Reflects emotional content
    'key_color_alignment': 1-5,            # Major=warm, minor=cool

    # Coherence-based
    'visual_coherence': 1-5,               # Do elements work together?
    'semantic_consistency': float,         # Internal consistency score

    # Overall
    'creativity_score': 1-5,               # Weighted combination
}
```

### 5.2 Dataset-Level Metrics

```python
dataset_metrics = {
    # Distribution statistics
    'mean_creativity': float,              # Average across dataset
    'std_creativity': float,               # Variation
    'creativity_distribution': dict,       # Histogram of scores

    # Improvement tracking
    'baseline_creativity': float,          # Naive prompts
    'refined_creativity': float,           # Interactive refinement
    'improvement_rate': float,             # % increase

    # Diversity metrics
    'prompt_diversity': float,             # How different are prompts?
    'visual_concept_variety': int,         # How many unique concepts?
    'vocabulary_diversity': float,         # Richness of language used

    # Alignment metrics
    'avg_music_alignment': float,          # How well do prompts match?
    'mode_alignment': float,               # Most common alignment level
}
```

---

## 6. Integration with Your Research

### 6.1 Add Creativity Evaluation to Pipeline

```python
# Current pipeline:
Audio → Features → ABC → LLM Prompt → Visual Prompt

# Enhanced pipeline:
Audio → Features → ABC → LLM Prompt → Visual Prompt
                                             ↓
                                    Creativity Evaluation
                                             ↓
                                      Scores (1-5)
                                             ↓
                                    [Optional] Refinement
```

### 6.2 Example Analysis Script

```python
import asyncio
from music_to_image_paper_pipeline import MusicToImagePaperPipeline, AudioLoaderFromNPY
from llm_client import get_recommended_client
from creativity_evaluator import MusicToImageCreativityEvaluator

async def analyze_creativity():
    """
    Analyze creativity of visual prompts across dataset
    """

    # Initialize
    loader = AudioLoaderFromNPY()
    pipeline = MusicToImagePaperPipeline(generation_mode="convergent")
    evaluator = MusicToImageCreativityEvaluator()
    llm = get_recommended_client()

    # Load samples
    samples = loader.load_batch(
        "../dataset/label_data_with_16kHz_audio.npy",
        indices=list(range(10))  # First 10 samples
    )

    # Process and evaluate
    results = []
    for audio, metadata in samples:
        # Generate prompt
        prompt_results = await pipeline.process_audio(audio, metadata, llm)

        # Evaluate creativity
        creativity = await evaluator.evaluate_prompt_creativity(
            audio=audio,
            visual_prompt=prompt_results['visual_prompt'],
            musical_features=prompt_results['features']
        )

        results.append({
            'features': prompt_results['features'],
            'visual_prompt': prompt_results['visual_prompt'],
            'creativity_metrics': creativity
        })

    # Aggregate statistics
    creativity_scores = [r['creativity_metrics']['overall'] for r in results]

    print(f"Mean Creativity: {sum(creativity_scores)/len(creativity_scores):.2f}")
    print(f"Std Dev: {np.std(creativity_scores):.2f}")
    print(f"Range: {min(creativity_scores):.2f} - {max(creativity_scores):.2f}")

    return results

# Run analysis
results = asyncio.run(analyze_creativity())
```

---

## 7. Research Contributions You Can Make

### 7.1 Unique Application

**Novel**: First to apply AUT/TTCT metrics to music-to-image LLM prompts
- Previous work: Evaluated creativity of alternative uses, poetry, image descriptions
- Your work: Evaluate creativity of prompts generated FROM music

### 7.2 Paper Outcomes

```
Title: "Measuring Creativity of Music-to-Image Visual Prompts:
       Applying Alternative Uses and Torrance Tests to LLM Generation"

Contributions:
1. Adaptation of AUT/TTCT metrics for music-to-image domain
2. Framework for evaluating prompt creativity
3. Interactive refinement for improving prompt creativity
4. Dataset analysis of music→prompt creativity mapping
5. Correlation between music features and prompt creativity

Findings:
- Which music features drive creative prompts?
- How does interactive refinement improve prompts?
- What makes prompts score high on creativity metrics?
- How does creativity vary by mood, tempo, key?
```

### 7.3 Metrics for Comparison

Compare different approaches:
```python
comparison = {
    'baseline_convergent': {
        'mean_creativity': 2.4,
        'std': 0.6,
        'avg_originality': 2.3,
        'avg_elaboration': 2.5,
        'avg_alignment': 2.4,
    },
    'baseline_divergent': {
        'mean_creativity': 3.1,
        'std': 0.8,
        'avg_originality': 3.2,
        'avg_elaboration': 3.0,
        'avg_alignment': 3.0,
    },
    'with_mel_spectrogram': {
        'mean_creativity': 3.4,
        'std': 0.7,
        'avg_originality': 3.5,
        'avg_elaboration': 3.3,
        'avg_alignment': 3.4,
    },
    'with_interactive_refinement': {
        'mean_creativity': 3.8,
        'std': 0.6,
        'avg_originality': 3.9,
        'avg_elaboration': 3.7,
        'avg_alignment': 3.8,
    }
}
```

---

## 8. Implementation Plan

### Phase 1: Build Evaluator (Week 1)
```python
# creativity_evaluator.py
- OriginalityScorer
- ElaborationScorer
- AlignmentScorer
- CoherenceScorer
- OverallCreativityEvaluator
```

### Phase 2: Integrate with Pipeline (Week 2)
```python
# Enhanced music_to_image_paper_pipeline.py
- Add evaluation step
- Track creativity metrics
- Support interactive refinement
```

### Phase 3: Analysis & Visualization (Week 3)
```python
# creativity_analysis.py
- Dataset-level statistics
- Feature→Creativity correlation
- Mode-specific analysis (convergent vs divergent)
- Visualization (histograms, scatter plots)
```

### Phase 4: Paper Writing (Week 4)
```
- Method section (metrics & evaluation)
- Results section (creativity scores & analysis)
- Discussion (what drives creativity)
- Contributions (first to apply to music-to-image)
```

---

## 9. Key Takeaways

### ✅ Yes, AUT and TTCT Apply to Your Research

| Metric | Applicability | Ease | Impact |
|--------|---------------|------|--------|
| **Originality** | ⭐⭐⭐⭐⭐ | High | Measures novelty of prompts |
| **Elaboration** | ⭐⭐⭐⭐⭐ | High | Measures richness/detail |
| **Alignment** | ⭐⭐⭐⭐ | High | Measures music fit |
| **Coherence** | ⭐⭐⭐⭐ | Medium | Measures visual unity |
| **Interactive Refinement** | ⭐⭐⭐⭐⭐ | High | Improves all metrics |

### ✅ Concrete Advantages

1. **Standardized Metrics**: Use established creativity measures
2. **Quantifiable Results**: Get numerical scores (1-5 scale)
3. **Comparable Data**: Compare different methods/configurations
4. **Research Novelty**: First application to music-to-image domain
5. **Clear Findings**: Measure impact of each system component
6. **Publishable Results**: Multiple metrics for research papers

### ✅ Next Steps

1. **Implement CreativityEvaluator** class with 4 metrics
2. **Integrate into pipeline** to score all generated prompts
3. **Run baseline analysis** on existing dataset
4. **Compare modes** (convergent vs divergent vs refined)
5. **Publish findings** on what drives creativity

---

## 10. References

```bibtex
@article{goes2023pushing,
  title={Pushing GPT's Creativity to Its Limits: Alternative Uses and Torrance Tests},
  author={Goes, Fabricio and Volpe, Marco and Sawicki, Piotr and Grzes, Marek and Watson, Jacob},
  journal={International Conference on Computational Creativity},
  year={2023}
}

@article{guilford1967creativity,
  title={Creativity: Yesterday, today and tomorrow},
  author={Guilford, Joy Paul},
  journal={The Journal of Creative Behavior},
  volume={1},
  number={1},
  pages={3--14},
  year={1967}
}

@article{torrance1966torrance,
  title={Torrance tests of creative thinking},
  author={Torrance, Ellis Paul},
  journal={Educational and Psychological Measurement},
  year={1966}
}
```

---

**Recommendation**: Implement creativity evaluation in your music-to-image system. It will strengthen your research significantly! 🚀
