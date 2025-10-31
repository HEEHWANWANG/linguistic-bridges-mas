# HarmonicVisuals: NLP Coursework Project Design

Repositioning HarmonicVisuals as a Natural Language Processing coursework project with emphasis on language understanding, linguistic analysis, and semantic processing.

---

## Executive Summary

HarmonicVisuals can be framed as an **NLP-focused project** where the primary research contribution is on **understanding how language (lyrics) relates to music structure and visual narrative**, with the thumbnail generation serving as the concrete application of NLP insights.

**Core NLP Question**: How can NLP techniques extract meaning from song lyrics and map that meaning to both audio structure and visual representation?

**Coursework Context**: Advanced NLP project demonstrating semantic understanding, information extraction, and multimodal grounding.

---

## Part 1: Repositioning as NLP Project

### Shift in Focus

**Traditional HarmonicVisuals**:
- Primary: Multi-agent coordination + visual generation
- Secondary: Language understanding (just one component)

**NLP-Focused HarmonicVisuals**:
- Primary: Language understanding + semantic mapping
- Secondary: Visual generation (application of NLP insights)
- Focus: How lyrics + song structure reveal narrative

### New Research Questions (NLP-Centric)

**RQ1**: How can NLP extract semantic meaning from lyrics to understand song's narrative arc?

**RQ2**: How does linguistic sentiment/emotion align with musical structure?

**RQ3**: What techniques best ground language meaning to multimodal phenomena (music + visual)?

**RQ4**: Can NLP identify thematic elements that correspond to musical form?

**RQ5**: How do lyrics structure (verse patterns, chorus repetition) map to expected visual narratives?

---

## Part 2: NLP Coursework Alignment

### Mapping to Typical NLP Coursework Topics

| NLP Topic | How HarmonicVisuals Uses It | Depth |
|-----------|---------------------------|-------|
| **Text Processing & Tokenization** | Parse song lyrics, extract key phrases | Foundational |
| **Sentiment Analysis** | Analyze emotional tone of lyrics | Core |
| **Named Entity Recognition (NER)** | Extract themes, characters, objects from lyrics | Intermediate |
| **Semantic Role Labeling (SRL)** | Understand who does what in song narrative | Intermediate |
| **Word Embeddings** | Semantic similarity between lyric concepts | Core |
| **Topic Modeling** | Extract main themes from lyrics | Intermediate |
| **Text Classification** | Classify song sections (verse/chorus/bridge) | Foundational |
| **Sequence Labeling (NER/POS)** | Tag lyrics by semantic role | Intermediate |
| **Coreference Resolution** | Track characters/themes across verses | Advanced |
| **Relationship Extraction** | Understand connections between themes | Advanced |
| **Question Answering** | Answer questions about song narrative | Advanced |
| **Text Summarization** | Summarize song's key narrative elements | Advanced |
| **Semantic Similarity** | Compare lyric meaning to visual concepts | Advanced |
| **Multimodal Grounding** | Ground language meaning to music + visual | Advanced |

### Coursework Learning Objectives Addressed

#### Foundational NLP (CS224N / similar):
- ✅ Text preprocessing (clean, tokenize lyrics)
- ✅ Sentiment analysis (emotional content)
- ✅ Word embeddings (semantic meaning)
- ✅ Basic classification (verse vs. chorus)

#### Intermediate NLP (Advanced electives):
- ✅ Named entity recognition (extract themes)
- ✅ Semantic role labeling (understand narrative)
- ✅ Topic modeling (dominant themes)
- ✅ Information extraction (story elements)

#### Advanced NLP (Research seminars):
- ✅ Coreference resolution (track narrative elements)
- ✅ Relationship extraction (connect themes)
- ✅ Semantic similarity (ground to visuals)
- ✅ Multimodal learning (language + audio + visual)

---

## Part 3: NLP-Centric Research Design

### Core NLP Pipeline

```
Song Lyrics Input
    ↓
Step 1: Text Preprocessing
  - Tokenization
  - Lowercasing
  - Remove punctuation (preserve structure)
  - POS tagging
    ↓
Step 2: Semantic Understanding
  - Sentiment analysis (positive/negative, arousal)
  - Emotion detection (joy, sadness, anger, etc.)
  - Named entity recognition (themes, characters, places)
  - Topic modeling (main subjects)
    ↓
Step 3: Narrative Structure Extraction
  - Semantic role labeling (who, what, when, where, why)
  - Coreference resolution (track entities across verses)
  - Relationship extraction (how concepts connect)
  - Story arc identification (exposition, rising action, climax, resolution)
    ↓
Step 4: Lyric-Music Alignment
  - Map lyric sentiment to musical intensity
  - Match lyric themes to music structure
  - Identify lyric-chorus correspondence
    ↓
Step 5: Visual Narrative Generation
  - Convert linguistic meaning to visual concepts
  - Ground abstract language to concrete images
  - Generate prompts for image generation
    ↓
Image Output
```

### NLP Components (Detailed)

#### Component 1: Lyric Sentiment & Emotion Analysis
**NLP Techniques**:
- Sentiment lexicons (VADER, TextBlob)
- Fine-tuned models (BERT, RoBERTa on sentiment data)
- Emotion detection models (plutchik emotions, basic emotions)

**Input**: Raw lyrics
**Output**: Emotion trajectory throughout song
```json
{
  "verse_1": {
    "sentiment": "neutral_to_positive",
    "emotions": ["nostalgia", "hope"],
    "arousal": 0.4,
    "valence": 0.6
  },
  "chorus": {
    "sentiment": "highly_positive",
    "emotions": ["joy", "triumph"],
    "arousal": 0.9,
    "valence": 0.95
  }
}
```

**NLP Learning**: Train sentiment/emotion models on song lyrics, evaluate on human annotations

---

#### Component 2: Named Entity Recognition (NER)
**NLP Techniques**:
- Standard NER (spaCy, transformers)
- Domain-specific NER fine-tuned on lyrics
- Custom tagset for music domain

**Input**: Lyrics with entities
**Output**: Extracted themes, characters, places, emotions
```
Lyrics: "In the city where dreams come alive,
         I found you under neon lights"

NER Output:
- LOCATION: "city", "neon lights"
- EMOTION_TARGET: "dreams"
- CHARACTER: "you" (implied person)
- SETTING: "neon city atmosphere"
```

**NLP Learning**: Train NER model on annotated song lyrics, handle domain-specific terms

---

#### Component 3: Semantic Role Labeling (SRL)
**NLP Techniques**:
- Semantic role labeling (BERT-based models)
- Predicate-argument structures
- Event extraction

**Input**: Lyric sentences
**Output**: Semantic roles (WHO does WHAT)
```
Sentence: "I chase the horizon where sky meets sea"

SRL Output:
- Agent: "I"
- Predicate: "chase"
- Theme: "horizon"
- Location: "where sky meets sea"
- Aspect: "movement toward goal"
```

**NLP Learning**: Understand predicate-argument relationships, extract semantic roles

---

#### Component 4: Coreference Resolution
**NLP Techniques**:
- Coreference resolution models (AllenNLP, spaCy)
- Pronoun resolution
- Entity linking

**Input**: Full lyrics with pronouns
**Output**: Resolved entity references
```
Verse 1: "She walks alone down empty streets"
Chorus: "And in her heart, she finds the light"

Resolution:
- "She" → main character (consistent across verses)
- "her heart" → psychological/emotional space
- Track character consistency across song
```

**NLP Learning**: Understand discourse structure, track entities, resolve ambiguity

---

#### Component 5: Relationship Extraction
**NLP Techniques**:
- Relation extraction models
- Pattern-based extraction
- Semantic role labeling + relation detection

**Input**: Lyrics with entities
**Output**: Relationships between concepts
```
Entities: "dreams" "city" "neon lights"

Relationships:
- dreams LOCATED_IN city
- city HAS_FEATURE neon lights
- dreams REALIZED_BY movement_to_city
```

**NLP Learning**: Extract semantic relationships, understand narrative connections

---

#### Component 6: Discourse & Narrative Structure
**NLP Techniques**:
- Rhetorical Structure Theory (RST)
- Narrative arc detection
- Story grammars

**Input**: Full lyrics
**Output**: Narrative structure
```
Opening: Establish setting + character
Build: Develop conflict/emotion
Climax: Peak moment (usually chorus)
Resolution: Conclusion or reflection

Map to song structure:
- Intro → Setting establishment
- Verse 1-2 → Character/conflict development
- Chorus → Emotional climax
- Bridge → Complication/variation
- Final chorus → Resolution emphasis
```

**NLP Learning**: Understand discourse structure, narrative arcs, storytelling

---

### Integration: Language Understanding Pipeline

```
Raw Lyrics
    ↓
[Sentiment/Emotion Analysis] → Emotional trajectory
    ↓
[Named Entity Recognition] → Themes, characters, places
    ↓
[Semantic Role Labeling] → Who does what, when, where
    ↓
[Coreference Resolution] → Track consistent entities
    ↓
[Relationship Extraction] → How concepts connect
    ↓
[Narrative Structure] → Overall story arc
    ↓
Unified Semantic Representation
    ↓
Visual Narrative Generation
    ↓
Image Prompt Creation
```

---

## Part 4: NLP-Specific Contributions

### Contribution 1: Multimodal Language Grounding
**What**: Techniques for grounding abstract language (lyrics) to concrete multimodal representations (music + visual)

**NLP Innovation**:
- Establish correspondence between linguistic sentiment and audio features
- Map semantic roles to visual objects/composition
- Link emotional language to perceptual concepts

**Technical Approach**:
```
Linguistic Level: "I soar beyond the clouds"
  ↓
Semantic Analysis: Agent = "I", Action = "soar", Location = "beyond clouds"
  ↓
Emotion Analysis: uplifting, expansive, hopeful
  ↓
Music Correlation: high pitch, ascending melody, major key
  ↓
Visual Grounding: sky imagery, upward composition, bright colors
  ↓
Image Prompt: "Soaring figure transcending boundaries, upward movement,
               clear sky, expansive perspective"
```

**Why Novel in NLP**:
- Most NLP work treats language in isolation
- Multimodal grounding underexplored in music domain
- First systematic framework connecting lyrics → audio → visual

---

### Contribution 2: Domain-Specific NLP Pipeline for Song Analysis
**What**: Specialized NLP pipeline optimized for song lyrics

**Key Challenges**:
- Song lyrics != news articles or other text
- Repetition (chorus repeats), poetic structure matter
- Metaphors and abstract language common
- Non-standard grammar acceptable

**NLP Innovation**:
```
Custom preprocessing:
  - Preserve repetition structure (important for song form)
  - Handle metaphors (map to emotional/visual concepts)
  - Understand poetic devices (rhyme, rhythm influence meaning)
  - Section-aware processing (verse/chorus/bridge separately)

Custom NER:
  - Domain terms: music genre references, emotion words
  - Characters: unnamed pronouns with emotional significance
  - Abstract entities: dreams, fears, hopes (not standard NER)

Custom sentiment:
  - Song-specific lexicons
  - Context-dependent emotion (same word different in verse vs. chorus)
  - Intensity tracks over sections (emotional arc)
```

**Why Valuable for Coursework**:
- Demonstrates domain adaptation
- Shows how to handle non-standard language
- Practical application of NLP techniques

---

### Contribution 3: Lyric-Music Structure Alignment
**What**: Model how lyrics correspond to musical form

**NLP + Music Analysis**:
```
Linguistic Structure          Musical Structure
─────────────────────         ──────────────────
Verse 1 (narrative setup) ←→ Intro section (musical setup)
Verse 2 (develop plot)    ←→ Developing melody
Chorus (emotional peak)   ←→ Harmonic climax
Bridge (complication)     ←→ Modulation / key change
Final chorus (resolution) ←→ Harmonic resolution
```

**NLP Methods**:
- Text analysis: Identify narrative progression
- Repetition tracking: Chorus == key message
- Density analysis: Important concepts repeated
- Structure correlation: Align lyric structure to music structure

**Why Important**:
- Shows how language structure reflects musical structure
- Demonstrates understanding of narrative
- Grounds linguistic concepts to real-world structure

---

### Contribution 4: Sentiment-Visual Correspondence Learning
**What**: Learn how linguistic sentiment maps to visual concepts

**Approach**:
```
Step 1: Extract sentiment from lyrics
  "bright", "light" → positive, illuminated
  "dark", "cold" → negative, isolated

Step 2: Extract visual concepts from reference images
  bright image → "illuminated space", "vivid colors"
  dark image → "shadows", "muted tones"

Step 3: Learn correspondence
  positive_sentiment → bright_colors, expansive_composition
  negative_sentiment → dark_tones, constrained_composition
  energetic_sentiment → dynamic_movement, bold_lines
  calm_sentiment → balanced_composition, soft_tones

Step 4: Apply to new lyrics
  "I soar beyond the clouds" (positive, expansive)
  → Predict visual: bright sky, upward movement
```

**NLP Learning**:
- Semantic similarity in language space
- Cross-modal embeddings
- Transfer learning between modalities

---

## Part 5: NLP Coursework Implementation

### Project Phases

#### Phase 1: Text Processing & Analysis (Foundational)
**Learning Objectives**:
- Tokenization, POS tagging, basic parsing
- Text preprocessing for domain-specific data
- Building pipelines

**Deliverables**:
- Clean lyrics dataset (50 songs)
- Text preprocessing pipeline
- Basic statistics (word frequency, structure analysis)
- Report: Language patterns in pop music

**NLP Tools**:
- NLTK, spaCy, TextBlob
- Custom preprocessing for song lyrics

**Coursework Credit**: 25% of project

---

#### Phase 2: Sentiment & Emotion Analysis (Core NLP)
**Learning Objectives**:
- Sentiment analysis models
- Emotion detection
- Lexicon-based vs. neural approaches
- Evaluation metrics

**Deliverables**:
- Sentiment analysis pipeline
- Emotion detection model (trained on song lyrics)
- Emotional trajectory for 50 songs
- Comparison: rule-based vs. neural models
- Analysis: How does emotion align with music?

**NLP Tools**:
- VADER, TextBlob (lexicon-based)
- BERT, RoBERTa fine-tuned on emotion data
- Hugging Face transformers

**Coursework Credit**: 25% of project

---

#### Phase 3: Information Extraction (Intermediate NLP)
**Learning Objectives**:
- Named entity recognition
- Semantic role labeling
- Information extraction
- Handling domain-specific NER

**Deliverables**:
- Custom NER model trained on song lyrics
- Semantic role labeling pipeline
- Extracted entities: themes, characters, locations
- Relationship extraction between entities
- Analysis: What narrative elements emerge?

**NLP Tools**:
- spaCy (NER training)
- Transformers (BERT-based SRL)
- Pattern-based extraction

**Coursework Credit**: 25% of project

---

#### Phase 4: Semantic Understanding & Multimodal Grounding (Advanced NLP)
**Learning Objectives**:
- Semantic similarity
- Multimodal embeddings
- Cross-modal grounding
- Advanced language understanding

**Deliverables**:
- Semantic representation of lyrics
- Coreference resolution system
- Narrative structure extraction
- Lyric-music-visual grounding
- Visual prompt generation from lyrics

**NLP Tools**:
- Word2Vec, GloVe embeddings
- CLIP embeddings (text-image similarity)
- Semantic role labeling models
- Custom alignment models

**Coursework Credit**: 25% of project

---

### Project Evaluation Rubric (NLP Focused)

| Component | Excellent | Good | Satisfactory | Needs Work |
|-----------|-----------|------|--------------|-----------|
| **NLP Pipeline Implementation** | All components working, well-integrated | Most components working, minor issues | Basic pipeline works | Incomplete implementation |
| **Sentiment/Emotion Analysis** | Models trained, evaluated, compared | One approach implemented well | Basic sentiment extraction | No proper evaluation |
| **Information Extraction** | Domain-adapted NER, SRL working | Standard NER implemented | Basic entity extraction | Limited extraction |
| **Semantic Understanding** | Advanced techniques, proper grounding | Good semantic representation | Basic understanding | Shallow analysis |
| **Multimodal Integration** | Language-music-visual aligned | Language and music connected | Language analyzed | No integration |
| **Documentation** | Clear explanations, theory + practice | Well-documented, mostly clear | Documented but unclear | Minimal documentation |
| **Evaluation** | Rigorous metrics, human study | Automatic metrics, baseline comparison | Basic evaluation | No proper evaluation |
| **Code Quality** | Clean, well-organized, reproducible | Functional, generally clean | Works but messy | Doesn't run reliably |

---

## Part 6: NLP-Centric Experimental Design

### Evaluation Focus Shift

**Traditional HarmonicVisuals**:
- Primary metric: Visual-musical alignment (how good is image?)
- Secondary metric: Narrative coherence (does image sequence tell story?)

**NLP Coursework**:
- Primary metric: NLP accuracy (how well do we understand lyrics?)
- Secondary metric: Lyric-music alignment (does NLP match music structure?)
- Tertiary metric: Visual grounding quality (does language map correctly to visuals?)

### Evaluation Metrics (NLP-Focused)

#### Metric 1: Sentiment Prediction Accuracy
**Measure**: How well does sentiment analysis align with human sentiment judgments?

```
Test: 50 songs × 5 sections = 250 lyric segments
Human annotation: Sentiment label (positive/negative/neutral) + arousal level
Model prediction: Sentiment score
Evaluation: Accuracy, F1-score, correlation with human labels
Baseline: VADER lexicon-based
Model: Fine-tuned BERT, transformer-based
```

**NLP Learning**: Sentiment analysis evaluation, domain-specific challenges

---

#### Metric 2: Emotion Detection F1-Score
**Measure**: Can model identify correct emotions from lyrics?

```
Emotions to detect:
  - Joy, Sadness, Anger, Fear, Surprise, Trust (Plutchik)
  - Or: Positive, Negative, Neutral + arousal/valence dimensions

Test set: 100 annotated lyric snippets
Evaluation: Per-emotion F1-score, confusion matrix
Comparison: Rule-based, BERT-based, fine-tuned models
```

**NLP Learning**: Multi-class classification, emotion detection, evaluation

---

#### Metric 3: Named Entity Recognition (NER) Performance
**Measure**: Does NER correctly extract themes, characters, places?

```
Custom tagset:
  - CHARACTER: People, pronouns with emotional significance
  - THEME: Abstract concepts (dreams, love, journey)
  - PLACE: Locations (city, sky, road)
  - EMOTION_WORD: Words indicating emotion state
  - ACTION: Verbs showing narrative movement

Test: Annotated corpus of 50 songs (full lyrics)
Evaluation: Precision, Recall, F1 per entity type
Baseline: Standard spaCy NER
Model: Fine-tuned NER on song lyrics
```

**NLP Learning**: NER evaluation, domain adaptation, custom entity types

---

#### Metric 4: Lyric-Music Structure Alignment
**Measure**: Does linguistic analysis correctly identify song sections?

```
Task: Classify each line of lyrics as:
  - INTRO: Opening, setting stage
  - VERSE: Narrative development
  - CHORUS: Emotional peak, key message
  - BRIDGE: Complication, variation
  - OUTRO: Resolution

Approach 1 (Rule-based):
  - Chorus: Repeated lines
  - Verse: Unrepeated lines
  - Accuracy: Measure against manual annotation

Approach 2 (Learning-based):
  - Train classifier on annotated lyrics
  - Features: Repetition, position, sentiment trajectory
  - Evaluate: Classification accuracy
```

**NLP Learning**: Text classification, feature engineering for songs

---

#### Metric 5: Semantic Similarity (Lyric-Visual Correspondence)
**Measure**: Does extracted lyric meaning map correctly to visual concepts?

```
Pipeline:
1. Extract semantic meaning from lyrics (NLP pipeline)
2. Extract visual concepts from reference images (CLIP embeddings)
3. Compute semantic similarity between lyric meaning and image

Evaluation:
  - Does semantic meaning match visual concept?
  - Measure using CLIP similarity scores
  - Compare to random baselines
  - Human evaluation: Does mapping make sense?
```

**NLP Learning**: Semantic similarity, multimodal embeddings, grounding

---

#### Metric 6: Human Evaluation (NLP Understanding)
**Measure**: Do humans agree that NLP-extracted meanings are correct?

```
Participants: 20-30 people (not required to be musicians)

Task A: Does sentiment match lyrics?
  - Show: Lyric segment + NLP sentiment label
  - Rate: 1-5 agreement scale
  - Metric: Mean agreement score

Task B: Are extracted entities correct?
  - Show: Lyric passage + extracted NER labels
  - Rate: Correctness of entity identification
  - Metric: Agreement percentage

Task C: Is narrative structure correctly identified?
  - Show: Lyrics with section labels (verse/chorus/bridge)
  - Rate: Correctness of section classification
  - Metric: Agreement percentage

Task D: Does visual mapping make sense?
  - Show: Lyric → semantic meaning → visual concept
  - Rate: Coherence of mapping
  - Metric: Agreement percentage
```

**NLP Learning**: Evaluation methodology, human annotation, agreement metrics

---

## Part 7: NLP Coursework Alignment Summary

### Which NLP Concepts Are Covered?

#### ✅ **Definitely Covered** (Foundational + Core)
- Text preprocessing and tokenization
- Sentiment analysis (lexicon and neural)
- Word embeddings and semantic similarity
- Text classification (song section identification)
- Named entity recognition
- Emotion detection
- Evaluation metrics (precision, recall, F1)

#### ✅ **Well Covered** (Intermediate)
- Semantic role labeling
- Information extraction
- Domain-specific NLP adaptation
- Fine-tuning transformers (BERT)
- Lexicon building
- Feature engineering
- Multi-class classification

#### ✅ **Partially Covered** (Advanced)
- Coreference resolution
- Relationship extraction
- Discourse analysis (narrative structure)
- Multimodal learning (language-vision grounding)
- Question answering (implicit in understanding)
- Transfer learning (across domains/modalities)

#### ⚠️ **Not Heavily Emphasized** (But not required)
- Machine translation
- Parsing and syntax
- Morphological analysis
- Speech recognition
- Dialog systems

---

## Part 8: Revised Research Contributions (NLP-Focused)

### Contribution 1: Domain-Adapted NLP Pipeline for Music Analysis
**What**: NLP pipeline specialized for song lyrics, handling unique linguistic properties

**Technical Details**:
- Custom preprocessing: preserve song structure (repetition, verse/chorus distinction)
- Domain-specific NER: recognizes music-domain entities (emotions, abstract concepts)
- Contextual understanding: same word means different things in verse vs. chorus
- Metaphor handling: maps poetic language to semantic meaning

**NLP Value**:
- Demonstrates domain adaptation
- Shows how to handle non-standard text
- Addresses challenge of repetition in lyrics
- Handles poetic vs. literal language

**Coursework Relevance**: ⭐⭐⭐⭐⭐ (Core NLP skill)

---

### Contribution 2: Multimodal Semantic Grounding
**What**: Framework for grounding abstract linguistic meaning to music structure and visual concepts

**Technical Details**:
- Sentiment analysis → Musical intensity/dynamics
- Emotional language → Arousal/valence dimensions
- Narrative progression → Song structure (verse/chorus/bridge)
- Visual metaphors → Image composition and color

**NLP Value**:
- Connects language to non-linguistic modalities
- Shows how semantics manifest across domains
- Demonstrates practical grounding

**Coursework Relevance**: ⭐⭐⭐⭐ (Advanced topic)

---

### Contribution 3: Lyric-Based Narrative Structure Extraction
**What**: NLP techniques to extract narrative arc and story structure from lyrics

**Technical Details**:
- Named entity recognition: extract characters, places, themes
- Coreference resolution: track entities across verses
- Semantic role labeling: understand narrative events (who did what)
- Discourse analysis: identify story arc (exposition → climax → resolution)

**NLP Value**:
- Applies discourse analysis to creative writing
- Shows how to extract narrative from text
- Demonstrates understanding of story structure

**Coursework Relevance**: ⭐⭐⭐⭐ (Advanced skill)

---

### Contribution 4: Emotion Trajectory Modeling
**What**: Model how emotional content changes throughout song using NLP

**Technical Details**:
- Sentiment analysis at line/section level
- Emotion detection (multiple emotion dimensions)
- Arousal/valence tracking over time
- Correlation with musical intensity

**NLP Value**:
- Sentiment analysis in temporal context
- Understanding emotional narrative
- Multi-dimensional emotion modeling

**Coursework Relevance**: ⭐⭐⭐⭐ (Core NLP)

---

### Contribution 5: Language-Music Structure Correspondence
**What**: Establish correspondence between linguistic structure and musical form

**Technical Details**:
- Identify repeated linguistic patterns (chorus vs. verses)
- Map semantic density to musical complexity
- Correlate emotional peaks to harmonic tension
- Align narrative structure to song form

**NLP Value**:
- Cross-domain structure analysis
- Shows how language structure reflects content
- Practical application of linguistic analysis

**Coursework Relevance**: ⭐⭐⭐ (Intermediate)

---

## Part 9: Course Integration Examples

### Integration with CS224N (NLP with Deep Learning)

**Unit: Word Embeddings**
- Use project: Train embeddings on song lyrics
- Analyze: Word similarities in music context
- Assignment: "Do embeddings capture emotional meaning of lyrics?"

**Unit: Sequence Labeling (NER/POS)**
- Use project: Implement NER for music entities
- Analyze: Named entity patterns in songs
- Assignment: "Build domain-specific NER for song lyrics"

**Unit: Sentiment Analysis**
- Use project: Sentiment analysis of lyrics
- Analyze: Emotion trajectories across songs
- Assignment: "Compare lexicon-based vs. neural sentiment models"

**Unit: Advanced Topics**
- Use project: Multimodal grounding
- Analyze: Language-music-visual correspondence
- Assignment: "Ground linguistic meaning to music features"

---

### Integration with Information Extraction Course

**Topic: Named Entity Recognition**
- Project: Build custom NER for song themes
- Deliverable: Annotated corpus, trained model, evaluation

**Topic: Relationship Extraction**
- Project: Extract relationships between song themes
- Deliverable: Relationship patterns, analysis

**Topic: Slot Filling**
- Project: Fill narrative slots from lyrics
- Deliverable: Extracted narrative elements per song

**Topic: Event Extraction**
- Project: Extract narrative events from lyrics
- Deliverable: Event timeline, causality analysis

---

### Integration with Semantic Analysis Course

**Topic: Word Sense Disambiguation**
- Project: Determine emotional sense of words in song context
- Deliverable: Context-aware emotion mappings

**Topic: Semantic Role Labeling**
- Project: Extract who-does-what from lyrics
- Deliverable: SRL-based narrative understanding

**Topic: Discourse Analysis**
- Project: Analyze narrative structure of songs
- Deliverable: Discourse trees, rhetorical relations

**Topic: Coreference Resolution**
- Project: Track characters across song verses
- Deliverable: Character tracking system

---

## Part 10: Sample Assignments for NLP Coursework

### Assignment 1: Lyric Text Processing Pipeline (Week 1-2)
**Objective**: Build foundational text processing for songs

**Tasks**:
1. Collect 50 pop songs with lyrics
2. Implement tokenization, POS tagging, lemmatization
3. Analyze: Common words, POS patterns, repetition patterns
4. Report: 2 pages with examples, analysis, findings

**Learning**: Text preprocessing, handling non-standard text

---

### Assignment 2: Sentiment & Emotion Analysis (Week 3-4)
**Objective**: Analyze emotional content of lyrics

**Tasks**:
1. Implement lexicon-based sentiment (VADER)
2. Fine-tune transformer-based model (BERT) on emotion data
3. Compare approaches on test set
4. Analyze: Emotion patterns by song genre, section type
5. Create visualization: Emotion trajectory per song
6. Report: Which approach is better? Why?

**Learning**: Sentiment analysis, emotion detection, model comparison

---

### Assignment 3: Named Entity Recognition (Week 5-6)
**Objective**: Extract entities from song lyrics

**Tasks**:
1. Design custom tagset for music domain (THEME, CHARACTER, PLACE, EMOTION)
2. Annotate 10 songs with custom entities
3. Train NER model on annotated data
4. Evaluate on held-out test set
5. Analyze: What entities are most common? By genre?
6. Report: Domain-specific challenges, solutions

**Learning**: NER, domain adaptation, annotation protocols

---

### Assignment 4: Narrative Structure Analysis (Week 7-8)
**Objective**: Extract and analyze narrative from lyrics

**Tasks**:
1. Implement semantic role labeling
2. Extract narrative elements: who (characters), what (actions), where (settings)
3. Implement coreference resolution (track entities)
4. Analyze: Narrative patterns across genres
5. Create narrative summaries for 5 songs
6. Report: How does narrative structure reflect song form?

**Learning**: Narrative analysis, semantic understanding, discourse analysis

---

### Assignment 5: Multimodal Grounding (Week 9-10)
**Objective**: Ground language meaning to music and visual concepts

**Tasks**:
1. Extract semantic meaning from lyrics (using NLP pipeline)
2. Extract music features (tempo, dynamics, harmonics)
3. Extract visual concepts from reference images
4. Learn correspondence between layers
5. Generate predictions: Given lyrics → visual concepts
6. Evaluate with human judgment
7. Report: How well does language ground to other modalities?

**Learning**: Multimodal learning, semantic grounding, evaluation

---

### Final Project: Full NLP-to-Visual Pipeline (Week 11-12)
**Objective**: Integrate all components into end-to-end system

**Deliverables**:
1. Complete NLP pipeline for lyric analysis
2. Sentiment/emotion trajectory modeling
3. Narrative structure extraction
4. Visual concept generation
5. Prompt generation for image creation
6. Full paper (8-10 pages) describing pipeline, evaluation, results
7. GitHub repository with code and documentation

**Evaluation**:
- NLP accuracy (sentiment, emotion, NER, etc.)
- Multimodal grounding quality (human evaluation)
- Overall system coherence
- Code quality and documentation
- Paper clarity and technical depth

**Learning**: Integration, system design, research communication

---

## Part 11: NLP vs. Multi-Agent Positioning

### Original Positioning (AAMAS Conference)
| Aspect | Focus |
|--------|-------|
| **Primary contribution** | Multi-agent coordination |
| **Novelty** | Artistic outlier preservation |
| **Unique value** | Creative disagreement mechanism |
| **Application** | Thumbnail generation via agents |
| **Target audience** | Multi-agent systems researchers |

### NLP Coursework Positioning
| Aspect | Focus |
|--------|-------|
| **Primary contribution** | Language understanding pipeline |
| **Novelty** | Domain-adapted NLP for song analysis |
| **Unique value** | Multimodal semantic grounding |
| **Application** | Understand lyrics + extract narrative |
| **Target audience** | NLP students and practitioners |

### Complementary, Not Competing

**Both are true and valuable**:
- **NLP perspective**: How can NLP understand song lyrics and extract meaning?
- **MARL perspective**: How can agents coordinate diverse perspectives into creative outputs?

**Relationship**:
- NLP pipeline → produces semantic understanding (needed for narrative agent)
- Multi-agent coordination → synthesizes diverse NLP outputs into creative visual narrative

---

## Part 12: Assessment for NLP Coursework

### Grading Rubric (NLP Focus)

**NLP Pipeline & Implementation (30%)**
- Technical correctness
- Feature engineering quality
- Model selection and justification
- Evaluation methodology

**Sentiment & Emotion Analysis (20%)**
- Accuracy of sentiment/emotion predictions
- Model comparison (rule-based vs. neural)
- Error analysis and insights
- Domain-specific challenges addressed

**Information Extraction (20%)**
- Named entity recognition performance
- Semantic role labeling quality
- Relationship extraction completeness
- Handling of poetic/metaphorical language

**Semantic Understanding & Grounding (20%)**
- Quality of semantic representations
- Multimodal grounding effectiveness
- Language-music-visual correspondence
- Creative insights

**Documentation & Communication (10%)**
- Clear technical writing
- Literature review adequacy
- Visual presentation (figures, examples)
- Code documentation and reproducibility

**Total: 100%**

---

## Conclusion

HarmonicVisuals works excellently as an **NLP coursework project** when repositioned with focus on:

1. **Language Understanding**: How to extract meaning from non-standard (song) text
2. **Semantic Analysis**: Domain-adapted NLP for music-specific challenges
3. **Multimodal Grounding**: Connecting language meaning to other modalities
4. **Narrative Extraction**: Understanding story structure in creative writing
5. **Practical Application**: Real-world use of NLP techniques

### Coursework Alignment Summary
✅ Covers foundational NLP concepts (sentiment, NER, classification)
✅ Demonstrates intermediate skills (SRL, information extraction, domain adaptation)
✅ Introduces advanced topics (coreference, discourse, multimodal learning)
✅ Provides practical experience with state-of-the-art tools
✅ Results in tangible, interesting application

### Both Perspectives Valid

The project serves **both** as:
1. **NLP coursework**: Understanding lyrics and narrative through language processing
2. **AAMAS research**: Multi-agent coordination for creative synthesis

The NLP perspective is primary for coursework; the multi-agent perspective can be secondary/future work.

---

*NLP Coursework Alignment: October 30, 2025*
*Status: Ready for coursework implementation*
*Recommended for: CS224N (NLP), Information Extraction, Semantic Analysis courses*
