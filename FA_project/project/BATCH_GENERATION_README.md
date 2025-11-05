# Batch Visual Prompt Generation System

## Overview

Complete system to generate **5 visual prompts for each of your 100 audio samples** (500 prompts total), ready for downstream image generation with SDXL.

**Key Features**:
- ✅ Processes all 100 samples automatically
- ✅ Generates 3 convergent (consistent) + 2 divergent (creative) prompts per sample
- ✅ Automatic checkpointing every 10 samples
- ✅ Multiple output formats for different use cases
- ✅ Comprehensive error handling and logging
- ✅ Command-line and Python API
- ✅ Well-documented with examples

---

## Quick Start

### 1️⃣ Run Batch Generation

```bash
# Option A: Python directly
python3 generate_visual_prompts_batch.py

# Option B: Shell script
./run_batch_generation.sh

# Option C: Run tests first
python3 test_batch_generation.py
```

### 2️⃣ Wait for Completion
- **Time**: 40-67 minutes (Claude API) or up to 200+ min (Ollama)
- **Checkpoints**: Auto-saved every 10 samples
- **Output**: 3 JSON files in `generated_prompts/` directory

### 3️⃣ Use the Results

**For image generation**:
```python
import json
with open('generated_prompts/prompts_for_image_generation.json') as f:
    prompts = json.load(f)
# Feed to SDXL image generator
```

**For analysis**:
```python
import json
with open('generated_prompts/visual_prompts_complete.json') as f:
    data = json.load(f)
# Analyze features, prompts, evaluate creativity
```

---

## Files Delivered

### Core Scripts

| File | Purpose | Lines |
|------|---------|-------|
| `generate_visual_prompts_batch.py` | Main batch generator | 500+ |
| `example_batch_generation.py` | 5 working examples | 350+ |
| `test_batch_generation.py` | Test suite (verify setup) | 300+ |
| `run_batch_generation.sh` | Bash wrapper script | 40 |

### Documentation

| File | Content |
|------|---------|
| `BATCH_GENERATION_GUIDE.md` | Comprehensive guide (400+ lines) |
| `BATCH_QUICK_REFERENCE.md` | Quick reference card |
| `BATCH_GENERATION_README.md` | This file |
| `BATCH_GENERATION_IMPLEMENTATION_SUMMARY.md` | Technical summary |

### Output Files (Generated)

| File | Size | Format | Use For |
|------|------|--------|---------|
| `visual_prompts_complete.json` | 2-5 MB | Nested JSON | Full analysis |
| `prompts_for_image_generation.json` | 2-5 MB | Flat list JSON | SDXL images |
| `generation_summary.json` | ~100 KB | JSON | Statistics |

---

## What Gets Generated

### Per Audio Sample
- **Musical Features** (extracted): key, tempo, tonality, melody, harmony, dynamics, mood
- **ABC Notation**: Text representation for LLM
- **5 Visual Prompts**:
  - 3 convergent (T=0.4) - consistent, reproducible
  - 2 divergent (T=0.8) - creative, exploratory

### Total Output
- **100 samples** × **5 prompts** = **500 visual prompts**
- Each prompt: 100-300 words
- Format: Text descriptions for SDXL image generation

### Example Generated Prompt

**Input**:
- Audio: Upbeat pop song, 120 BPM, major key, happy mood

**Generated Prompt** (convergent, T=0.4):
> "A vibrant pop concert stage with bright stage lighting, golden and cyan neon lights illuminating an energetic performer dancing dynamically on stage, with pulsing rhythm matching the upbeat tempo"

**Generated Prompt** (divergent, T=0.8):
> "Kaleidoscopic mandala patterns expanding outward, iridescent particles flowing in ascending spirals, electric cyan and magenta gradients pulsing at 120 BPM, hypnotic visual rhythm"

---

## How to Use

### Method 1: Python (Recommended)

```bash
python3 generate_visual_prompts_batch.py
```

**Options**:
```bash
python3 generate_visual_prompts_batch.py \
  --dataset dataset/label_data_with_16kHz_audio.npy \
  --output-dir generated_prompts \
  --samples 100 \
  --start-idx 0 \
  --mel-spectrogram \
  --batch-size 5
```

### Method 2: Shell Script

```bash
./run_batch_generation.sh
```

**Options**:
```bash
./run_batch_generation.sh <dataset> <output_dir> <samples> <start_idx> <mel_spec>

# Examples:
./run_batch_generation.sh                    # All defaults
./run_batch_generation.sh "" "" 20            # First 20 samples
./run_batch_generation.sh "" "" "" 50         # Start from sample 50
./run_batch_generation.sh "" "" "" "" true    # With mel-spectrogram
```

### Method 3: Python API

```python
import asyncio
from generate_visual_prompts_batch import BatchPromptGenerator

async def generate():
    generator = BatchPromptGenerator(
        dataset_path="dataset/label_data_with_16kHz_audio.npy",
        output_dir="generated_prompts",
        batch_size=5
    )

    # Generate all prompts
    results = await generator.generate_all_prompts()

    # Save outputs
    generator.save_results()
    generator.save_summary_stats()
    generator.export_for_image_generation()
    generator.print_summary()

asyncio.run(generate())
```

### Method 4: Run Examples

```bash
# Run all 5 examples
python3 example_batch_generation.py

# Or specific examples
python3 example_batch_generation.py 1  # Full batch
python3 example_batch_generation.py 2  # Partial (10 samples)
python3 example_batch_generation.py 3  # With mel-spectrogram
python3 example_batch_generation.py 4  # Load and inspect
python3 example_batch_generation.py 5  # For image generation
```

---

## Output Files

### File 1: `visual_prompts_complete.json`

**Complete dataset** with all information.

```json
{
  "metadata": {
    "dataset_path": "...",
    "generation_timestamp": "2025-11-05T...",
    "total_samples": 100,
    "prompts_per_sample": 5,
    "llm_provider": "OllamaClient",
    "sample_rate": 16000
  },
  "samples": [
    {
      "sample_idx": 0,
      "musical_features": {
        "key": "C",
        "tonality": "major",
        "tempo": 120.5,
        "mood": "happy",
        // ... 5 more features
      },
      "abc_notation": "X:1\nT:...",
      "prompts": [
        {
          "prompt_id": 0,
          "mode": "convergent",
          "temperature": 0.4,
          "visual_prompt": "A bright, energetic..."
        },
        // ... 4 more prompts
      ]
    },
    // ... 99 more samples
  ]
}
```

**Use For**:
- Complete analysis and research
- Creativity evaluation
- Feature correlation studies
- Detailed investigation

**Size**: 2-5 MB

---

### File 2: `prompts_for_image_generation.json`

**Optimized format** for image generation pipeline.

```json
[
  {
    "sample_idx": 0,
    "prompt_id": 0,
    "mode": "convergent",
    "temperature": 0.4,
    "visual_prompt": "A bright, energetic...",
    "features": { "key": "C", "tempo": 120.5, ... },
    "abc_notation": "X:1\nT:..."
  },
  {
    "sample_idx": 0,
    "prompt_id": 1,
    "mode": "convergent",
    "temperature": 0.4,
    "visual_prompt": "An uplifting, joyful..."
  },
  // ... 498 more (flat list, one per prompt)
]
```

**Use For**:
- Direct input to SDXL image generator
- Simple iteration over all prompts
- Image generation pipeline

**Size**: 2-5 MB

**Example Usage**:
```python
import json
with open('generated_prompts/prompts_for_image_generation.json') as f:
    prompts = json.load(f)

for p in prompts:
    images = generator.generate(prompt=p['visual_prompt'])
```

---

### File 3: `generation_summary.json`

**Statistics and metadata**.

```json
{
  "total_samples": 100,
  "total_prompts": 500,
  "convergent_prompts": 300,
  "divergent_prompts": 200,
  "generation_timestamp": "...",
  "samples_with_errors": 0,
  "sample_summary": [
    {
      "sample_idx": 0,
      "features": { ... },
      "prompt_count": 5,
      "modes": ["convergent", "divergent"]
    },
    // ... 99 more
  ]
}
```

**Use For**:
- Quick statistics
- Quality assurance
- Error tracking
- Summary reporting

**Size**: ~100 KB

---

## Integration Examples

### Use with Image Generator

```python
import json
from image_generator import create_image_generator

# Load prompts
with open('generated_prompts/prompts_for_image_generation.json') as f:
    prompts = json.load(f)

# Create generator
gen = create_image_generator(device='cuda', use_refiner=True)

# Generate images
for i, p in enumerate(prompts):
    print(f"Generating {i+1}/{len(prompts)}")
    images = gen.generate(prompt=p['visual_prompt'], seed=i)

    # Save
    images[0].save(f"image_{i:04d}.png")
```

### Use with Creativity Evaluator

```python
import json
from creativity_evaluator import MusicToImageCreativityEvaluator

# Load complete data
with open('generated_prompts/visual_prompts_complete.json') as f:
    data = json.load(f)

# Evaluate each prompt
evaluator = MusicToImageCreativityEvaluator()
results = []

for sample in data['samples']:
    for prompt in sample['prompts']:
        metrics = evaluator.evaluate(
            prompt['visual_prompt'],
            sample['musical_features']
        )
        results.append({
            'sample_idx': sample['sample_idx'],
            'prompt_id': prompt['prompt_id'],
            'mode': prompt['mode'],
            'creativity_score': metrics.overall,
            'originality': metrics.originality,
            'elaboration': metrics.elaboration
        })

# Analyze
convergent = [r for r in results if r['mode'] == 'convergent']
divergent = [r for r in results if r['mode'] == 'divergent']

avg_conv = sum(r['creativity_score'] for r in convergent) / len(convergent)
avg_div = sum(r['creativity_score'] for r in divergent) / len(divergent)

print(f"Convergent avg: {avg_conv:.2f}")
print(f"Divergent avg: {avg_div:.2f}")
```

### Use for Research Analysis

```python
import json
import numpy as np

# Load
with open('generated_prompts/visual_prompts_complete.json') as f:
    data = json.load(f)

# Analyze by music features
tempos = [s['musical_features']['tempo'] for s in data['samples']]
moods = [s['musical_features']['mood'] for s in data['samples']]

print(f"Tempo range: {min(tempos):.1f} - {max(tempos):.1f} BPM")
print(f"Mood distribution: {set(moods)}")

# Correlation analysis
fast_samples = [s for s in data['samples'] if s['musical_features']['tempo'] > 120]
slow_samples = [s for s in data['samples'] if s['musical_features']['tempo'] < 80]

print(f"Fast samples: {len(fast_samples)}")
print(f"Slow samples: {len(slow_samples)}")
```

---

## Performance

### Generation Time

| Provider | Per Sample | 100 Samples |
|----------|-----------|-------------|
| Claude API | 15-25s | 40-67 min |
| Ollama (mistral) | 25-75s | 67-200 min |
| Mock (test) | <1s | <2 min |

### Storage

| File | Size |
|------|------|
| `visual_prompts_complete.json` | 2-5 MB |
| `prompts_for_image_generation.json` | 2-5 MB |
| `generation_summary.json` | ~100 KB |
| **Total** | **~5-10 MB** |

### Checkpointing

Automatic saves every 10 samples:
- `prompts_checkpoint_010.json`
- `prompts_checkpoint_020.json`
- etc.

Can resume from last checkpoint if interrupted.

---

## Verification

### Test Setup

```bash
python3 test_batch_generation.py
```

Tests:
- ✅ All imports
- ✅ Dataset loading
- ✅ Feature extraction
- ✅ LLM connection
- ✅ Batch generator initialization
- ✅ Single sample generation
- ✅ All required files present

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Module not found" | Run from `FA_project/project/` directory |
| "Connection refused" | Start Ollama: `ollama serve` |
| Too slow | Use Claude API or fewer samples |
| Interrupted | Restart with `--start-idx` to resume from checkpoint |
| Out of memory | Process fewer samples at a time |

---

## Documentation

- **BATCH_GENERATION_GUIDE.md** - Comprehensive guide (400+ lines)
- **BATCH_QUICK_REFERENCE.md** - Quick reference
- **BATCH_GENERATION_IMPLEMENTATION_SUMMARY.md** - Technical details
- **This file** - Overview and getting started

---

## Workflow

```
1. [Setup Check]
   python3 test_batch_generation.py

2. [Run Generation]
   python3 generate_visual_prompts_batch.py
   (or ./run_batch_generation.sh)

3. [Verify Output]
   ls -lh generated_prompts/

4. [Use Results]
   - Image generation: prompts_for_image_generation.json
   - Analysis: visual_prompts_complete.json
   - Statistics: generation_summary.json

5. [Optional]
   - Evaluate creativity: creativity_evaluator.py
   - Generate images: image_generator.py
   - Analyze data: Python/Jupyter
```

---

## Next Steps

1. **Run tests** (optional):
   ```bash
   python3 test_batch_generation.py
   ```

2. **Generate prompts**:
   ```bash
   python3 generate_visual_prompts_batch.py
   ```

3. **Check results**:
   ```bash
   ls -lh generated_prompts/
   ```

4. **Use in downstream tasks**:
   - Image generation with SDXL
   - Creativity evaluation
   - Research analysis

---

## Summary

✅ **Complete, production-ready batch generation system**
- Processes all 100 audio samples
- Generates 5 prompts per sample (500 total)
- Multiple output formats
- Automatic checkpointing
- Comprehensive error handling
- Well-documented with examples

**Ready to run**: `python3 generate_visual_prompts_batch.py`
