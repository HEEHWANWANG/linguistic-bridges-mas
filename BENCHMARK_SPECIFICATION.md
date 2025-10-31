# Linguistic Bridges: Benchmark Specification

**Date**: October 30, 2025
**Phase**: Q4 2025 Foundation (Week 3-4)
**Responsible Guilds**: Research Guild + Forge Guild (Data Engineering)
**Status**: Specification Complete - Ready for Data Collection

---

## Executive Summary

This document specifies the **PopMusic-Narrative Benchmark** - a comprehensive dataset for training and evaluating multimodal music understanding systems.

**Benchmark Overview**:
- **50 diverse pop songs** with professional annotations
- **3 modalities**: Audio (music), Language (lyrics), Visual (reference images)
- **Multi-task dataset**: Supports sentiment analysis, NER, narrative extraction, visual grounding
- **Open for research**: Available for community use
- **Reproducible**: All data sources documented and licensable

---

## Part 1: Dataset Overview

### 1.1 Core Specifications

| Aspect | Specification |
|--------|---------------|
| **Total Songs** | 50 songs |
| **Total Duration** | 200-250 minutes (avg 4-5 min per song) |
| **Audio Format** | MP3 320kbps, .wav at 44.1kHz |
| **Lyrics Format** | Plain text, timestamped (line-level) |
| **Visual Annotations** | 5 professional reference images per song (one per section) |
| **Annotation Set Size** | 250 total reference images (50 songs × 5 sections) |
| **Metadata Richness** | Genre, artist, release year, emotional descriptor, narrative theme |
| **Split Ratios** | Train 60% (30), Val 20% (10), Test 20% (10) |

### 1.2 Data Collection Phases

**Phase 1: Pilot PoC (Q4 2025)**
- 10 songs with full annotation
- Validate annotation process
- Test data collection pipeline
- Estimate time/cost for full dataset

**Phase 2: Main Dataset (Q1 2026)**
- Remaining 40 songs
- Finalize annotation guidelines
- Quality assurance pass
- Community release

---

## Part 2: Song Selection Strategy

### 2.1 Diversity Criteria

**By Genre** (5 songs each):
- Pop (mainstream, radio-friendly)
- Indie Pop (alternative, artistic)
- Hip-Hop (narrative-rich, rhythmic)
- R&B/Soul (emotional depth)
- Electronic/Synthpop (experimental)
- Alternative (diverse sub-genres)
- Rock/Pop-Rock (dynamic range)
- Ballads (emotional concentration)
- Funk/Disco (rhythmically complex)
- Other (user requests, emerging genres)

**By Narrative Theme** (5 songs each):
- Love/Romance (8 songs)
- Journey/Quest (8 songs)
- Self-Discovery/Growth (8 songs)
- Celebration/Party (6 songs)
- Struggle/Hardship (6 songs)
- Social Commentary (5 songs)
- Abstract/Poetic (3 songs)

**By Complexity Level**:
- Simple narrative (15 songs): Clear story arc, easy to visualize
- Moderate narrative (20 songs): Multiple themes, some ambiguity
- Complex narrative (15 songs): Abstract, layered, metaphorical

**By Duration**:
- <3 minutes (10 songs): Pop singles, radio format
- 3-5 minutes (30 songs): Standard song length
- >5 minutes (10 songs): Extended pieces, build-ups

### 2.2 Artist & Licensing Considerations

**Preferred Artists/Catalogs**:
- Independent artists (easier licensing)
- Creative Commons licensed music
- Royalty-free artist partnerships
- Emerging/unsigned artists (promotional value)

**Licensing Strategy**:
- Secure proper music licensing for dataset use
- Attribution to artists (CV benefit)
- Possible artist compensation
- Open-source music sources (e.g., Free Music Archive)

---

## Part 3: Song Section Definitions

### 3.1 Standard Song Structure

Each song divided into **5 sections** (typical pop format):

```
INTRO (0:00 - 0:20)
├─ Musical introduction
├─ Sets mood and atmosphere
└─ Often instrumental or minimal vocals

VERSE 1 (0:20 - 1:00)
├─ Story exposition / Setup
├─ Introduces characters, setting, problem
└─ Narrative foundation

CHORUS (1:00 - 1:25)
├─ Emotional peak / Theme statement
├─ Repeating key message
└─ Highest emotional intensity

BRIDGE/VERSE 2 (1:25 - 2:20)
├─ Narrative development / Twist
├─ Character development
├─ Emotional evolution

OUTRO (2:20 - end)
├─ Resolution / Conclusion
├─ Emotional resolution or open ending
└─ Musical fade or dramatic ending
```

### 3.2 Song Structure Annotation

For each section, annotate:

**Structural Markers**:
- Start time (MM:SS)
- End time (MM:SS)
- Section type (Intro/Verse/Chorus/Bridge/Outro)
- Duration in seconds

**Audio Features**:
- Tempo (BPM)
- Loudness/Intensity (0-10 scale)
- Rhythmic complexity (0-10 scale)
- Instrumental density (0-10 scale)
- Dynamics (static/building/peaked/fading)

**Lyrical Markers**:
- Key lyrics (important lines)
- Narrative function (exposition/conflict/climax/resolution)
- Emotional valence (negative/neutral/positive)
- Emotional arousal (low/medium/high)

---

## Part 4: Linguistic Annotations

### 4.1 Lyric-Level Annotations

**Format**: Line-by-line annotation of lyrics

**For each lyric line**:

```
Line text: "I've been walking down this broken road"
Section: VERSE 1
Timestamp: 0:25 - 0:30

Sentiment:
  - Valence: -0.6 (negative)
  - Arousal: 0.5 (moderate)

Emotions (Plutchik):
  - Primary: sadness, trust
  - Secondary: anticipation

Entities:
  - Type: METAPHOR
  - Span: "broken road"
  - Referent: life journey (difficult)

Roles:
  - Agent: I (protagonist)
  - Action: walking
  - Location: broken road

Narrative Function:
  - Exposition (setting up story)
  - Emotional tone: melancholic
```

### 4.2 Song-Level Linguistic Annotations

**Overall Narrative**:
```
Title: [Song name]
Artist: [Artist name]
Genre: [Genre]
Duration: [MM:SS]

Story Summary (1-3 sentences):
[Concise summary of narrative arc]

Narrative Arc:
  - Exposition: [What happens in verses]
  - Climax: [Peak moment, usually chorus]
  - Resolution: [How story ends]
  - Type: complete_arc | open_ending | cyclical | metaphorical

Main Characters:
  1. Name/Role: [e.g., "I/Narrator - seeking]
  2. Name/Role: [e.g., "They/Love interest - absent"]

Key Themes:
  - Primary: [e.g., heartbreak, personal growth]
  - Secondary: [e.g., hope, resilience]

Abstract Concepts:
  - [e.g., "broken road = life difficulty"]
  - [e.g., "light = hope/guidance"]

Emotional Journey:
  - Start: [emotion] (intensity 0-10: ____)
  - Middle: [emotion] (intensity 0-10: ____)
  - End: [emotion] (intensity 0-10: ____)
```

### 4.3 Annotation Tool & Process

**Tool**: Custom web interface for efficient annotation

**Workflow**:
1. Display song metadata and audio player
2. Show lyrics with timestamps
3. Annotators select line(s) and assign labels
4. Real-time sentiment/emotion visualization
5. Save and export to JSON

**Estimated Time**:
- Per song: 45-60 minutes (including listening, re-reading)
- Per line: 1-2 minutes on average
- Full dataset: 45-50 hours of annotation work

---

## Part 5: Visual Annotations

### 5.1 Reference Images

**Concept**: Professional visual designers create reference images for each section

**Process**:
1. Designers read lyrics and narrative analysis
2. Listen to song section (audio + lyrics)
3. Create visual representation
   - Digital illustration
   - Photo composition
   - Abstract visual
4. Document design rationale

**Image Per Section**:
- 1 primary reference image (high quality)
- Dimensions: 512×512 pixels (standard for image models)
- Format: PNG with transparency or JPG
- Artistic style: Varied (realism, abstract, digital, photographic)

**Design Guidelines**:
- Reflect narrative meaning, not just surface-level matching
- Include emotional tone (color palette, composition)
- Suggest visual metaphors found in lyrics
- Consider musical intensity in visual weight/saturation
- Balance literal interpretation with creative freedom

### 5.2 Visual Design Documentation

**For each image**:

```
Section: CHORUS
Song: [Title]
Timestamp: 1:00 - 1:25

Design Rationale:
[1-3 sentences explaining design choices]

Visual Elements:
- Primary subject: [e.g., figure silhouette]
- Color palette: [e.g., deep blues, warm oranges]
- Composition: [e.g., centered, rule of thirds]
- Style: [e.g., abstract watercolor]
- Emotional tone: [e.g., triumphant, melancholic]

Connection to Lyrics:
- Key lyric reference: [e.g., "reach for the stars"]
- Metaphor implementation: [e.g., stars = dreams]
- Narrative function: [e.g., shows climactic moment]

Musical Alignment:
- Intensity mapping: [Lyric intensity → Visual weight]
- Rhythm reflection: [How rhythm influences composition]
- Dynamic expression: [How musical changes shown visually]
```

### 5.3 Professional Designer Involvement

**Timeline**:
- **Q4 2025**: Recruit 3-5 professional designers
- **Q1 2026**: Create images for all 50 songs (250 images)
- **Budget**: $20-30 per image ($5,000-7,500 total)

**Recruitment**:
- Art schools / design programs
- Freelance platforms (Upwork, Fiverr)
- Independent artists
- Faculty/student incentives

**Quality Control**:
- Rubric for evaluation (alignment, creativity, technical quality)
- Independent review by 2 judges per image
- Minimum score: 7/10 for inclusion in benchmark
- Revision process for below-threshold images

---

## Part 6: Metadata Schema

### 6.1 Complete Data Structure

```json
{
  "song_id": "pop_001",
  "metadata": {
    "title": "Song Title",
    "artist": "Artist Name",
    "genre": ["pop", "indie"],
    "subgenre": "indie-pop",
    "year_released": 2023,
    "duration_seconds": 245,
    "bpm": 120,
    "key": "C major",
    "time_signature": "4/4",
    "composer": "Artist Name",
    "lyricist": "Artist Name"
  },

  "narrative_info": {
    "story_summary": "...",
    "narrative_arc": "complete_arc",
    "main_characters": [...],
    "key_themes": [...],
    "abstract_concepts": {...},
    "emotional_journey": {...}
  },

  "sections": [
    {
      "section_id": "pop_001_intro",
      "section_type": "intro",
      "start_time": 0,
      "end_time": 20,
      "duration": 20,

      "audio_features": {
        "loudness": 0.3,
        "intensity": 3,
        "rhythmic_complexity": 2,
        "instrumental_density": 0.8
      },

      "lyrical_content": {
        "lines": [
          {
            "text": "...",
            "timestamp_start": 0,
            "timestamp_end": 5,
            "sentiment": {
              "valence": -0.3,
              "arousal": 0.5
            },
            "emotions": ["sadness", "trust"],
            "entities": [...],
            "narrative_function": "exposition"
          }
        ]
      },

      "visual_reference": {
        "image_id": "pop_001_intro_img_001",
        "image_path": "images/pop_001_intro.png",
        "design_rationale": "...",
        "visual_elements": {
          "primary_subject": "...",
          "color_palette": [...],
          "style": "abstract"
        },
        "designer": "Designer Name",
        "quality_score": 8.5,
        "review_date": "2026-01-15"
      }
    },
    // ... 4 more sections
  ],

  "splits": {
    "train": true,
    "validation": false,
    "test": false
  }
}
```

### 6.2 File Organization

```
dataset/
├── metadata.json          # Master metadata file
├── README.md              # Dataset documentation
├── LICENSE                # Licensing info
│
├── audio/
│   ├── pop_001.mp3
│   ├── pop_002.mp3
│   └── ...
│
├── lyrics/
│   ├── pop_001.txt        # Plain text lyrics
│   ├── pop_001.json       # Annotated lyrics (JSON)
│   └── ...
│
├── images/
│   ├── pop_001_intro.png
│   ├── pop_001_verse1.png
│   ├── pop_001_chorus.png
│   ├── pop_001_bridge.png
│   ├── pop_001_outro.png
│   └── ...
│
└── annotations/
    ├── pop_001_narrative.json
    ├── pop_001_sentiment.json
    ├── pop_001_entities.json
    └── ...
```

---

## Part 7: Annotation Guidelines

### 7.1 Sentiment & Emotion Annotation

**Sentiment Labels**:
- **Valence** (-1.0 to 1.0):
  - -1.0: Very negative (sad, angry, frustrated)
  - 0.0: Neutral (factual, descriptive)
  - 1.0: Very positive (happy, excited, triumphant)

- **Arousal** (0.0 to 1.0):
  - 0.0: Calm, peaceful, passive
  - 0.5: Moderate energy
  - 1.0: Excited, energetic, intense

**Emotion Labels** (Plutchik Wheel):
- Primary: Joy, Trust, Fear, Surprise, Sadness, Disgust, Anger, Anticipation
- Secondary: Combinations (optimism, love, remorse, etc.)

**Annotator Instructions**:
- Consider both explicit (word choice) and implicit (context) emotional content
- Account for irony/sarcasm (literal word vs. intended meaning)
- Mark ambiguous lines for human review
- Inter-annotator agreement target: >0.75 Krippendorff's α

### 7.2 Named Entity Recognition

**Entity Types for Music Domain**:
- **PERSON**: Characters, referenced individuals
- **LOCATION**: Places mentioned in lyrics
- **EMOTION**: Emotional states or abstract feelings
- **CONCEPT**: Abstract ideas (e.g., "broken dreams")
- **OBJECT**: Physical things with narrative significance
- **TIME**: Temporal references
- **METAPHOR**: Figure of speech with special meaning
- **ACTION**: Significant actions/events

**Annotation Format**:
```
Text: "I walked through the city alone"
Entities:
- "city": LOCATION
- "alone": EMOTION
- "walked": ACTION
```

### 7.3 Narrative Function Annotation

**Function Labels** (per line):
- **EXPOSITION**: Introduces characters, setting, background
- **RISING_ACTION**: Develops plot, complications emerge
- **CLIMAX**: Emotional peak, major turning point
- **FALLING_ACTION**: Resolution beginning, tension decreasing
- **RESOLUTION**: Conclusion, final emotional state

**Annotator Task**:
- Classify each lyrical section by narrative function
- Identify climactic moments
- Map story structure across song

---

## Part 8: Task Definitions

### 8.1 Supported Tasks

The benchmark supports multiple downstream tasks:

#### Task 1: Sentiment Analysis
- **Input**: Lyric lines
- **Output**: Valence & Arousal scores
- **Metric**: MSE between predicted and annotated scores
- **Baseline**: VADER (pre-trained) + Fine-tuned BERT

#### Task 2: Emotion Classification
- **Input**: Lyric lines
- **Output**: Emotion labels (multi-label)
- **Metric**: F1-score (macro)
- **Baseline**: TextBlob + Fine-tuned RoBERTa

#### Task 3: Named Entity Recognition
- **Input**: Lyric text
- **Output**: Entity spans and types
- **Metric**: Token-level F1 (micro)
- **Baseline**: spaCy en_core_web_lg + Fine-tuned BERT-BiLSTM-CRF

#### Task 4: Semantic Role Labeling
- **Input**: Lyric sentences
- **Output**: Predicate-argument structures
- **Metric**: F1 on argument spans
- **Baseline**: AllenNLP SRL + Domain fine-tuning

#### Task 5: Coreference Resolution
- **Input**: Song lyrics (full text)
- **Output**: Coreference chains
- **Metric**: CoNLL F1
- **Baseline**: e2e-coref + Domain fine-tuning

#### Task 6: Narrative Structure Extraction
- **Input**: Song lyrics + melody
- **Output**: Story arc (exposition → climax → resolution)
- **Metric**: Human evaluation (story coherence)
- **Baseline**: Rule-based heuristics + LLM-based

#### Task 7: Visual Grounding
- **Input**: Lyric + audio features
- **Output**: Visual elements (objects, colors, style)
- **Metric**: Human evaluation (alignment to reference images)
- **Baseline**: CLIP + Prompt engineering

#### Task 8: Image Generation & Refinement
- **Input**: Narrative description + lyrics
- **Output**: Generated image
- **Metric**: Human evaluation (narrative alignment, creativity)
- **Baseline**: DALL-E 3 / Midjourney + Iterative refinement

---

## Part 9: Evaluation Metrics

### 9.1 Automatic Metrics

| Task | Metric | Target | Rationale |
|------|--------|--------|-----------|
| Sentiment | MSE (Valence, Arousal) | <0.15 | Continuous prediction quality |
| Emotion | F1 (macro) | >0.75 | Classification accuracy |
| NER | F1 (token-level) | >0.78 | Entity boundary accuracy |
| SRL | F1 (arguments) | >0.72 | Predicate-argument accuracy |
| Coreference | CoNLL F1 | >0.65 | Chain resolution difficulty |
| Narrative | BLEU score | >0.60 | Story summary similarity |
| Visual Grounding | CLIP Score | >0.75 | Image-text alignment |
| Image Generation | FID Score | <50 | Image quality |

### 9.2 Human Evaluation Metrics

**For narrative understanding**:
- Story coherence (1-5 scale): Can humans follow narrative?
- Emotional accuracy (1-5 scale): Does extraction capture emotional tone?
- Character understanding (1-5 scale): Correctly identified protagonist?

**For visual generation**:
- Narrative alignment (1-5 scale): Does image match lyric meaning?
- Emotional resonance (1-5 scale): Does image convey correct emotion?
- Artistic quality (1-5 scale): Is image creative and well-executed?
- Creativity (1-5 scale): Is approach novel/unexpected?

**Evaluation protocol**:
- 5-10 expert evaluators per song
- Double-blinded (don't know which system generated)
- Inter-rater agreement >0.70 required
- Aggregation: Mean ± std

---

## Part 10: Data Release Strategy

### 10.1 Release Timeline

**Phase 1: Private (Q4 2025 - Q1 2026)**
- 10 songs (pilot dataset)
- Team access only
- For validation and method development

**Phase 2: Closed Access (Q2 2026)**
- Full 50 songs
- Request-based access for academic research
- Attribution required
- No commercial use

**Phase 3: Open Release (Q3 2026)**
- Full benchmark public
- Documentation complete
- Leaderboard infrastructure
- Community contributions encouraged

### 10.2 Licensing Model

**Audio**:
- Creative Commons or original artist licensing
- Attribution required
- Non-commercial research use permitted

**Lyrics**:
- Original artist attribution
- Educational use permitted
- Research publication allowed

**Reference Images**:
- Designer attribution
- Creative Commons-compatible or custom license
- Commercial derivatives require permission

**Annotations**:
- Open CC-BY license
- Free to use/modify/distribute
- Attribution appreciated

### 10.3 Citation Format

```bibtex
@dataset{linguisticbridges_benchmark_2026,
  title={PopMusic-Narrative Benchmark: Multimodal Music Understanding Dataset},
  author={HEEHWANWANG},
  year={2026},
  url={https://github.com/HEEHWANWANG/linguistic-bridges-mas},
  note={50 songs with linguistic, audio, and visual annotations}
}
```

---

## Part 11: Quality Assurance

### 11.1 Validation Checklist

**Per Song**:
- [ ] Audio quality verified (clear, <50dB noise)
- [ ] Lyrics verified against source (>99% accuracy)
- [ ] Section boundaries accurate (±1 second)
- [ ] All linguistic annotations complete
- [ ] Reference images high quality (>7/10)
- [ ] Metadata complete and accurate
- [ ] File organization correct

**Per Dataset**:
- [ ] Genre distribution balanced
- [ ] Narrative theme coverage adequate
- [ ] Difficulty levels distributed
- [ ] Train/val/test splits stratified
- [ ] Inter-annotator agreement >0.70
- [ ] No personally identifiable information
- [ ] License compliance verified

### 11.2 Documentation Completeness

**Required Documentation**:
- [ ] Dataset paper (1-2 pages)
- [ ] Detailed README
- [ ] Annotation guidelines
- [ ] Data schema documentation
- [ ] Sample annotations (3 songs)
- [ ] Usage examples
- [ ] License and attribution guide
- [ ] Known limitations

---

## Part 12: Expected Baseline Performance

### 12.1 NLP Task Baselines

**Task**: Sentiment Analysis
- VADER (rule-based): F1 ≈ 0.62
- BERT (fine-tuned): F1 ≈ 0.81
- Proposed system: F1 ≈ 0.85

**Task**: Named Entity Recognition
- spaCy: F1 ≈ 0.70
- BERT-BiLSTM-CRF (fine-tuned): F1 ≈ 0.80
- Proposed system: F1 ≈ 0.84

**Task**: Coreference Resolution
- e2e-coref: CoNLL F1 ≈ 0.62
- Fine-tuned on music domain: CoNLL F1 ≈ 0.71
- Proposed system: CoNLL F1 ≈ 0.75

### 12.2 Multimodal Task Baselines

**Task**: Visual Grounding (CLIP)
- CLIP (zero-shot): CLIP Score ≈ 0.68
- CLIP + Prompt engineering: CLIP Score ≈ 0.76
- Proposed system: CLIP Score ≈ 0.82

**Task**: Image Generation
- DALL-E 3 (generic prompt): FID ≈ 65, human eval ≈ 3.2/5
- DALL-E 3 (music-aware prompt): FID ≈ 58, human eval ≈ 3.8/5
- Proposed system (iterative): FID ≈ 48, human eval ≈ 4.3/5

---

## Part 13: FAQ & Known Limitations

### 13.1 Known Limitations

1. **Language**: English lyrics only (first version)
   - *Plan*: Multi-language version in follow-up work

2. **Genre Bias**: Pop-focused (by design)
   - *Rationale*: High narrative content in pop
   - *Mitigation*: Broad sub-genre coverage

3. **Western Perspective**: Primarily Western pop music
   - *Plan*: Expand to K-pop, J-pop, Bollywood in future

4. **Subjectivity**: Visual design is subjective
   - *Mitigation*: Multiple reference images possible; use as inspiration, not ground truth

5. **Dataset Size**: 50 songs is moderate (larger would be better)
   - *Rationale*: Quality > Quantity; 50 high-quality is better than 500 low-quality
   - *Plan*: Expand if community contributes annotations

### 13.2 Frequently Asked Questions

**Q: Can I use this for commercial purposes?**
A: No, research use only. Commercial requests reviewed case-by-case.

**Q: Will you add more languages?**
A: Yes, follow-up work planned for multi-language support.

**Q: How can I contribute annotations?**
A: Contact us for contribution guidelines. Contributor credits given.

**Q: What if I disagree with an annotation?**
A: We welcome constructive feedback. Report via GitHub issues.

---

## Part 14: Implementation Timeline

### Q4 2025 (Pilot - 10 Songs)

**Week 1-2**:
- [ ] Select 10 pilot songs
- [ ] Secure music licensing
- [ ] Record audio, obtain lyrics

**Week 3**:
- [ ] Set up annotation tools
- [ ] Recruit pilot annotators
- [ ] Create annotation guidelines v1

**Week 4**:
- [ ] Conduct annotations (10 songs)
- [ ] Quality review & revisions
- [ ] Extract metrics & document learnings

### Q1 2026 (Full Dataset - 50 Songs)

**Jan** (Weeks 1-2):
- [ ] Recruit professional designers (5)
- [ ] Recruit additional annotators (3-4)
- [ ] Finalize annotation guidelines

**Feb** (Weeks 3-4):
- [ ] Select remaining 40 songs
- [ ] Conduct linguistic annotations
- [ ] Begin visual design process

**Mar** (Weeks 5-6):
- [ ] Complete visual annotations
- [ ] Quality assurance pass
- [ ] Metadata finalization
- [ ] Documentation completion

---

## Part 15: Resource & Cost Estimate

### 15.1 Data Collection Costs

| Item | Quantity | Cost/Unit | Total |
|------|----------|-----------|-------|
| Music licensing | 50 songs | $10-20 | $500-1,000 |
| Lyric verification | 50 songs | $5 | $250 |
| Linguistic annotation | 50 songs | $15/song | $750 |
| Professional design | 250 images | $20-30 | $5,000-7,500 |
| QA & Documentation | 50 songs | $10 | $500 |
| **Total** | | | **$6,000-9,500** |

### 15.2 Time Investment

| Task | Hours | Team |
|------|-------|------|
| Song selection & licensing | 20 | Research Guild |
| Annotation tool setup | 10 | Forge Guild |
| Linguistic annotations | 40-50 | 3-4 annotators |
| Visual design | 100-125 | 5 designers |
| QA & revision | 30 | Research + Forge |
| Documentation | 20 | Chroniclers Guild |
| **Total** | 220-255 | Multi-guild |

---

## Conclusion

The **PopMusic-Narrative Benchmark** will be:
- ✅ **High-quality**: Professional annotations, careful curation
- ✅ **Comprehensive**: Multiple modalities, diverse music
- ✅ **Reproducible**: Clear documentation, open design
- ✅ **Useful**: Support 8+ downstream tasks
- ✅ **Community-friendly**: Open-source release planned

**This benchmark will enable**:
1. Training robust music understanding models
2. Evaluating multimodal MARL systems
3. Future research on music-visual synthesis
4. Educational use in courses

**Status**: ✅ READY FOR DATA COLLECTION (Q4 2025)

---

**Document Status**: ✅ COMPLETE & APPROVED
**Next Phase**: Begin Pilot Collection (Oct 30 - Nov 30, 2025)
**Gate Criteria**: 10-song pilot complete with validation
**Target Completion**: March 31, 2026 (Full dataset)

