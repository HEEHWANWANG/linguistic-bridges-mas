# Music-to-Image System: Complete Guide

**Purpose**: Generate high-quality SDXL images from audio samples using the music-to-image paper replication system.

**Status**: ✅ Production Ready | **Date**: November 6, 2025

---

## 📊 System Overview

This system replicates the paper pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MUSIC-TO-IMAGE PIPELINE                      │
└─────────────────────────────────────────────────────────────────┘

1. AUDIO INPUT
   └─ 100 audio samples (16 kHz, 10-second clips)
      File: dataset/label_data_with_16kHz_audio.npy

2. FEATURE EXTRACTION (Music Analysis)
   └─ Extract 8 musical features per sample
      - Key, Tonality, Tempo, Time Signature
      - Mood, Melody Contour, Harmonic Progression, Dynamic Intensity

3. VISUAL PROMPT GENERATION
   └─ Generate 5 prompts per sample (500 total)
      - 3 convergent prompts (T=0.4, consistent)
      - 2 divergent prompts (T=0.8, creative)
      Output: generated_prompts/visual_prompts_complete.json

4. CREATIVITY EVALUATION
   └─ Score each prompt on 4 metrics
      - Originality, Elaboration, Alignment, Coherence
      Output: creativity_scores/*.json

5. IMAGE GENERATION (SDXL)
   └─ Generate high-quality PNG images
      - 1 image per prompt (500 total)
      - Resolution: 512×512 to 1024×1024
      Output: images/sample_XXX/sample_XXX_prompt_YY.png

6. ANALYSIS & EXPORT
   └─ Compare convergent vs divergent results
   └─ Extract statistics and metadata
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Generate Visual Prompts (50-70 minutes)

```bash
python3 generate_visual_prompts_batch.py
```

**Output**:
- `generated_prompts/visual_prompts_complete.json` - All 500 prompts with features
- `generated_prompts/prompts_for_image_generation.json` - Flat format ready for images
- `generated_prompts/generation_summary.json` - Statistics

### Step 2: Evaluate Creativity (2-5 minutes)

```bash
python3 calculate_batch_creativity_scores.py
```

**Output**:
- `creativity_scores/creativity_prompt_scores.json` - Individual scores (500 entries)
- `creativity_scores/creativity_sample_summaries.json` - Per-sample analysis (100 entries)
- `creativity_scores/creativity_dataset_stats.json` - Overall statistics
- `creativity_scores/creativity_comparison_report.json` - Convergent vs divergent comparison

### Step 3: Generate Images (2-6 hours depending on GPU)

```bash
python3 generate_images_from_prompts.py
```

**Output**:
- `images/sample_000/` through `images/sample_099/` - 500 PNG images total
- `images/image_generation_log.json` - Detailed metadata for all images
- `images/image_generation_summary.json` - Generation statistics

---

## 📖 Detailed Workflow

### Phase 1: Visual Prompt Generation

**Script**: `generate_visual_prompts_batch.py` (700+ lines)

**What it does**:
1. Loads 100 audio samples from dataset
2. Extracts 8 musical features for each sample
3. Generates ABC music notation from features
4. Uses LLM (Claude/Ollama) to create visual prompts
5. Saves 5 prompts per sample (3 convergent + 2 divergent)

**Key Features**:
- Async/await for efficient batch processing
- Checkpointing every 10 samples for fault recovery
- Multiple LLM provider support (Claude API, Ollama)
- Mel-spectrogram enhancement option
- Full feature extraction pipeline included

**Dependencies**:
- `music_to_image_paper_pipeline.py` - Core audio analysis
- `music_analyzer.py` - Musical feature extraction
- `llm_client.py` - LLM abstraction layer
- `prompt_builder.py` - Prompt construction

**Output Files**:
```
generated_prompts/
├── visual_prompts_complete.json          # Nested: samples → prompts
├── prompts_for_image_generation.json     # Flat: array of prompt objects
└── generation_summary.json               # Statistics
```

**Time**: 50-70 minutes for 100 samples with Claude API, 90-200 minutes with Ollama

---

### Phase 2: Creativity Evaluation

**Script**: `calculate_batch_creativity_scores.py` (600+ lines)

**What it does**:
1. Loads all 500 prompts from `visual_prompts_complete.json`
2. Scores each prompt on 4 dimensions:
   - **Originality**: Uniqueness and novelty
   - **Elaboration**: Detail and specificity
   - **Alignment**: Fidelity to audio features
   - **Coherence**: Internal consistency
3. Aggregates statistics by mode (convergent vs divergent)
4. Generates comparison analysis

**Key Features**:
- Automated scoring using linguistic analysis
- Multi-level aggregation (prompt → sample → dataset)
- Convergent vs divergent comparison
- Detailed JSON reports with all metrics
- Summary statistics and distributions

**Dependencies**:
- `creativity_evaluator.py` - Scoring implementation

**Output Files**:
```
creativity_scores/
├── creativity_prompt_scores.json         # All 500 individual scores
├── creativity_sample_summaries.json      # 100 per-sample aggregations
├── creativity_dataset_stats.json         # Overall statistics
└── creativity_comparison_report.json     # Mode comparison
```

**Time**: 2-5 minutes for 500 prompts

---

### Phase 3: Image Generation

**Script**: `generate_images_from_prompts.py` (600+ lines)

**What it does**:
1. Loads 500 visual prompts from `visual_prompts_complete.json`
2. Uses SDXL (Stable Diffusion XL) to generate images
3. Organizes output in sample directories
4. Saves detailed metadata and statistics
5. Implements checkpointing for fault recovery

**Key Features**:
- Configurable resolution (512×512 to 1024×1024)
- Optional refiner model for enhanced quality
- GPU/CPU device selection with auto-detection
- Error recovery with graceful continuation
- Checkpointing every 50 images
- Comprehensive metadata in JSON format

**Dependencies**:
- `image_generator.py` - SDXL generator implementation

**Output Files**:
```
images/
├── sample_000/
│   ├── sample_000_prompt_00.png          # 768×768 PNG
│   ├── sample_000_prompt_01.png
│   ├── sample_000_prompt_02.png
│   ├── sample_000_prompt_03.png
│   └── sample_000_prompt_04.png
├── sample_001/ through sample_099/       # Similar structure
├── image_generation_log.json             # All 500 image metadata
└── image_generation_summary.json         # Statistics
```

**Time Estimates**:
- 512×512, 20 steps: ~45 minutes
- 768×768, 30 steps (default): ~2-3 hours
- 768×768, 40 steps + refiner: ~4-6 hours
- 1024×1024, 50 steps + refiner: ~8+ hours

---

## ⚙️ Configuration & Options

### Environment Setup

**Python Version**: 3.8+

**Install Dependencies**:
```bash
pip install -r requirements.txt
```

**Key Libraries**:
- `transformers` - Hugging Face models
- `diffusers` - SDXL image generation
- `numpy` - Numerical operations
- `pydantic` - Data validation
- `librosa` - Audio analysis
- `anthropic` (optional) - Claude API
- `ollama` (optional) - Local LLM

### LLM Provider Configuration

**Claude API (Recommended - Fastest)**:
```bash
export ANTHROPIC_API_KEY="your-api-key"
python3 generate_visual_prompts_batch.py
# Time: 50-70 minutes
```

**Ollama (Free, Local)**:
```bash
# In another terminal, start Ollama server
ollama serve

# In your terminal
export LLM_PROVIDER=ollama
python3 generate_visual_prompts_batch.py
# Time: 90-200 minutes
```

### Image Generation Configuration

**Default (Balanced Quality & Speed)**:
```bash
python3 generate_images_from_prompts.py
# 768×768, 30 steps, 2-3 hours
```

**Fast Mode (Lower Quality)**:
```bash
python3 generate_images_from_prompts.py --width 512 --height 512 --steps 20
# 512×512, 20 steps, 45 minutes
```

**High Quality Mode**:
```bash
python3 generate_images_from_prompts.py --refiner --steps 40 --width 768 --height 768
# 768×768, 40 steps + refiner, 4-6 hours
```

**CPU Only** (Very Slow):
```bash
python3 generate_images_from_prompts.py --device cpu --width 512 --height 512
# 512×512, CPU only, 12-24 hours
```

---

## 📊 Output Analysis

### Prompt Statistics

Check how many convergent vs divergent prompts were generated:

```bash
python3 << 'EOF'
import json

with open('generated_prompts/generation_summary.json') as f:
    summary = json.load(f)

print(f"Total samples: {summary['total_samples']}")
print(f"Total prompts: {summary['total_prompts']}")
print(f"Convergent: {summary['convergent_prompts']}")
print(f"Divergent: {summary['divergent_prompts']}")
EOF
```

### Creativity Analysis

Compare convergent vs divergent creativity:

```bash
python3 << 'EOF'
import json

with open('creativity_scores/creativity_comparison_report.json') as f:
    report = json.load(f)

print(f"Convergent avg originality: {report['convergent_metrics']['originality_avg']:.3f}")
print(f"Divergent avg originality: {report['divergent_metrics']['originality_avg']:.3f}")
print(f"\nConvergent avg elaboration: {report['convergent_metrics']['elaboration_avg']:.3f}")
print(f"Divergent avg elaboration: {report['divergent_metrics']['elaboration_avg']:.3f}")
EOF
```

### Image Generation Summary

View image generation statistics:

```bash
python3 << 'EOF'
import json

with open('images/image_generation_summary.json') as f:
    summary = json.load(f)

print(f"Total images generated: {summary['total_images_generated']}")
print(f"Success rate: {summary['success_rate']:.1f}%")
print(f"Resolution: {summary['image_dimensions']}")
print(f"Device used: {summary['device']}")
EOF
```

---

## 🔧 Troubleshooting

### Error: "CUDA out of memory"

**Solution 1**: Reduce resolution
```bash
python3 generate_images_from_prompts.py --width 512 --height 512
```

**Solution 2**: Reduce inference steps
```bash
python3 generate_images_from_prompts.py --steps 20
```

**Solution 3**: Use CPU (slower but will work)
```bash
python3 generate_images_from_prompts.py --device cpu --width 512 --height 512
```

### Error: "Prompts file not found"

**Solution**: Generate prompts first
```bash
python3 generate_visual_prompts_batch.py
python3 calculate_batch_creativity_scores.py
python3 generate_images_from_prompts.py
```

### Error: LLM connection failed

**For Claude API**:
```bash
# Check if API key is set
echo $ANTHROPIC_API_KEY

# If empty, set it
export ANTHROPIC_API_KEY="sk-ant-..."
```

**For Ollama**:
```bash
# Check if Ollama is running
curl http://localhost:11434

# If not, start it in another terminal
ollama serve
```

### Generation is very slow

**Cause 1**: Using CPU instead of GPU
```bash
# Check device in logs or use explicit GPU
python3 generate_images_from_prompts.py --device cuda
```

**Cause 2**: Too many inference steps
```bash
# Use fewer steps for faster generation
python3 generate_images_from_prompts.py --steps 20
```

**Cause 3**: Image resolution too high
```bash
# Use lower resolution
python3 generate_images_from_prompts.py --width 512 --height 512
```

---

## 📁 Project Structure

```
FA_project/project/
│
├─ 🔵 Core Scripts
│  ├─ generate_visual_prompts_batch.py      # Generate 500 prompts from audio
│  ├─ calculate_batch_creativity_scores.py  # Score prompts (4 dimensions)
│  └─ generate_images_from_prompts.py       # Generate images from prompts
│
├─ 🟢 Support Scripts
│  ├─ music_to_image_paper_pipeline.py      # Audio analysis pipeline
│  ├─ music_analyzer.py                      # Feature extraction
│  ├─ creativity_evaluator.py                # Scoring implementation
│  ├─ llm_client.py                          # LLM provider abstraction
│  ├─ image_generator.py                     # SDXL generator API
│  ├─ prompt_builder.py                      # Prompt construction
│  └─ mel_spectrogram_converter.py           # Audio preprocessing
│
├─ 📚 Documentation
│  ├─ SYSTEM_GUIDE.md                        # This file (complete overview)
│  ├─ RUNNING_COMMANDS.md                    # All executable commands
│  ├─ BATCH_GENERATION_GUIDE.md              # Prompt generation detailed guide
│  ├─ CREATIVITY_SCORING_GUIDE.md            # Scoring detailed guide
│  └─ IMAGE_GENERATION_GUIDE.md              # Image generation detailed guide
│
├─ 🛠️ Configuration & Dependencies
│  ├─ config.yaml                            # System configuration
│  ├─ requirements.txt                       # Python dependencies
│  └─ run_batch_generation.sh                # Shell wrapper script
│
└─ 📊 Data & Output
   ├─ dataset/                               # Input audio data
   ├─ generated_prompts/                     # Step 1 output (500 prompts)
   ├─ creativity_scores/                     # Step 2 output (scores)
   └─ images/                                # Step 3 output (500 PNG images)
```

---

## 🎯 Use Cases

### Use Case 1: Quick Test (5 minutes)

Want to verify everything works?

```bash
# Generate 2 samples (10 prompts) instead of 100
python3 generate_visual_prompts_batch.py --samples 2

# Score just those prompts
python3 calculate_batch_creativity_scores.py

# Generate images from just those prompts
python3 generate_images_from_prompts.py --limit 10 --width 512 --height 512
```

### Use Case 2: Full Production Run (3-4 hours total)

```bash
# Step 1: Generate all prompts (50-70 min)
python3 generate_visual_prompts_batch.py

# Step 2: Score all prompts (2-5 min)
python3 calculate_batch_creativity_scores.py

# Step 3: Generate all images (2-3 hours)
python3 generate_images_from_prompts.py
```

### Use Case 3: High-Quality Images (4-6 hours)

```bash
python3 generate_visual_prompts_batch.py  # 50-70 min
python3 calculate_batch_creativity_scores.py  # 2-5 min
python3 generate_images_from_prompts.py --refiner --steps 40  # 4-6 hours
```

### Use Case 4: Analyze Results

```bash
# Compare convergent vs divergent prompts
python3 << 'EOF'
import json
from pathlib import Path

# Load creativity scores
with open('creativity_scores/creativity_comparison_report.json') as f:
    report = json.load(f)

# Compare metrics
conv = report['convergent_metrics']
div = report['divergent_metrics']

print("CONVERGENT vs DIVERGENT COMPARISON")
print(f"Originality: {conv['originality_avg']:.3f} vs {div['originality_avg']:.3f}")
print(f"Elaboration: {conv['elaboration_avg']:.3f} vs {div['elaboration_avg']:.3f}")
print(f"Alignment: {conv['alignment_avg']:.3f} vs {div['alignment_avg']:.3f}")
print(f"Coherence: {conv['coherence_avg']:.3f} vs {div['coherence_avg']:.3f}")
EOF
```

---

## 🔍 Advanced Topics

### Using the Python API Directly

Instead of command-line, you can use the classes directly:

```python
import asyncio
from generate_visual_prompts_batch import BatchPromptGenerator

async def main():
    # Create generator
    generator = BatchPromptGenerator(
        dataset_path="dataset/label_data_with_16kHz_audio.npy",
        output_dir="generated_prompts",
        use_mel_spectrogram=False,
        batch_size=5
    )

    # Generate prompts for specific samples only
    sample_indices = [0, 1, 2, 3, 4]  # First 5 samples
    results = await generator.generate_all_prompts(sample_indices)

    # Save results
    generator.save_results()
    generator.save_summary_stats()

asyncio.run(main())
```

### Custom Scoring

```python
from calculate_batch_creativity_scores import BatchCreativityCalculator

# Load and score specific samples
calculator = BatchCreativityCalculator(
    prompts_file="generated_prompts/visual_prompts_complete.json"
)

scores = calculator.calculate_all_scores()
calculator.save_results()
```

### Batch Image Generation with Custom Config

```python
from generate_images_from_prompts import BatchImageGenerator

generator = BatchImageGenerator(
    prompts_file="generated_prompts/visual_prompts_complete.json",
    output_dir="custom_output",
    image_height=1024,
    image_width=1024,
    num_inference_steps=50,
    use_refiner=True,
    device="cuda"
)

results = asyncio.run(generator.generate_all_images())
generator.save_results()
```

---

## 📝 Citation

If using this implementation in research, please cite:

```
Music-to-Image System Implementation
Based on: [Original Paper Citation]
Implementation: 2025
```

---

## ✅ Verification Checklist

Before running, verify you have:

- [ ] Python 3.8 or higher
- [ ] 16GB+ system RAM
- [ ] GPU with 6GB+ VRAM (or use CPU mode)
- [ ] 20GB+ free disk space
- [ ] Dataset file: `dataset/label_data_with_16kHz_audio.npy`
- [ ] All dependencies: `pip install -r requirements.txt`
- [ ] LLM configured (Claude API key or Ollama running)

---

## 📞 Support

### Common Questions

**Q: How long will it take?**
A: 3-4 hours total: 50-70 min (prompts) + 2-5 min (scoring) + 2-3 hours (images)

**Q: Can I run on CPU?**
A: Yes, but image generation will take 12-24 hours instead of 2-6 hours.

**Q: Do I need a GPU?**
A: Not required, but strongly recommended for practical use.

**Q: Can I stop and resume?**
A: Yes, the system checkpoints every 10-50 items depending on the phase.

**Q: What if it fails partway through?**
A: Resume from checkpoint files and rerun the command.

---

**Last Updated**: November 6, 2025
**Status**: ✅ Production Ready
