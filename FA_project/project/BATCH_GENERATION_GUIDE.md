# Batch Visual Prompt Generation Guide

**Purpose**: Generate 5 visual prompts (3 convergent + 2 divergent) for each of your 100 audio samples and save them for downstream image generation.

**Status**: ✅ Production-ready implementation

---

## Quick Start

### Simplest Usage: Generate All Prompts

```bash
python3 generate_visual_prompts_batch.py
```

This will:
- Process all 100 audio samples
- Generate 5 prompts per sample (500 total)
- Save results to `generated_prompts/` directory

### Using the Shell Script

```bash
# Generate all prompts
./run_batch_generation.sh

# Generate first 20 samples
./run_batch_generation.sh dataset/label_data_with_16kHz_audio.npy generated_prompts 20

# With mel-spectrogram enhancement
./run_batch_generation.sh dataset/label_data_with_16kHz_audio.npy generated_prompts "" 0 true
```

### Python API (Programmatic)

```python
import asyncio
from generate_visual_prompts_batch import BatchPromptGenerator

async def main():
    generator = BatchPromptGenerator(
        dataset_path="dataset/label_data_with_16kHz_audio.npy",
        output_dir="generated_prompts",
        use_mel_spectrogram=False,
        batch_size=5
    )

    # Generate prompts
    results = await generator.generate_all_prompts()

    # Save outputs
    generator.save_results()
    generator.save_summary_stats()
    generator.export_for_image_generation()

asyncio.run(main())
```

---

## Command-Line Options

```bash
python3 generate_visual_prompts_batch.py \
    --dataset <path>                # Default: dataset/label_data_with_16kHz_audio.npy
    --output-dir <dir>              # Default: generated_prompts
    --samples <num>                 # Default: all (processes all samples)
    --start-idx <idx>               # Default: 0 (start from sample 0)
    --mel-spectrogram               # Enable mel-spectrogram enhancement (flag)
    --batch-size <num>              # Default: 5 (prompts per sample)
```

### Examples

```bash
# Generate all 100 samples
python3 generate_visual_prompts_batch.py

# Generate first 20 samples
python3 generate_visual_prompts_batch.py --samples 20

# Generate samples 50-70
python3 generate_visual_prompts_batch.py --start-idx 50 --samples 20

# Use mel-spectrogram enhancement
python3 generate_visual_prompts_batch.py --mel-spectrogram

# Custom output directory
python3 generate_visual_prompts_batch.py --output-dir my_prompts

# All options combined
python3 generate_visual_prompts_batch.py \
    --dataset dataset/label_data_with_16kHz_audio.npy \
    --output-dir generated_prompts \
    --samples 50 \
    --start-idx 0 \
    --mel-spectrogram \
    --batch-size 5
```

---

## Output Files

### 1. `visual_prompts_complete.json` (Main Output)

Complete dataset with all features and prompts:

```json
{
  "metadata": {
    "dataset_path": "dataset/label_data_with_16kHz_audio.npy",
    "generation_timestamp": "2025-11-05T14:30:45.123456",
    "total_samples": 100,
    "prompts_per_sample": 5,
    "mel_spectrogram": false,
    "llm_provider": "OllamaClient",
    "sample_rate": 16000
  },
  "samples": [
    {
      "sample_idx": 0,
      "metadata": { ... },
      "musical_features": {
        "key": "C",
        "tonality": "major",
        "tempo": 120.5,
        "time_signature": "4/4",
        "mood": "happy",
        "melody_contour": "ascending",
        "harmonic_progression": "simple",
        "dynamic_intensity": "intense"
      },
      "abc_notation": "X:1\nT:...\nM:4/4\n...",
      "prompts": [
        {
          "prompt_id": 0,
          "mode": "convergent",
          "temperature": 0.4,
          "visual_prompt": "A bright, energetic visual..."
        },
        {
          "prompt_id": 1,
          "mode": "convergent",
          "temperature": 0.4,
          "visual_prompt": "An uplifting, joyful scene..."
        },
        // ... 3 more prompts
      ]
    },
    // ... 99 more samples
  ]
}
```

**Size**: ~2-5 MB (depending on prompt length)

**Usage**: Complete dataset for analysis, creativity evaluation, research

### 2. `prompts_for_image_generation.json` (Image Pipeline Format)

Optimized format for image generation pipeline:

```json
[
  {
    "sample_idx": 0,
    "prompt_id": 0,
    "mode": "convergent",
    "temperature": 0.4,
    "visual_prompt": "A bright, energetic visual...",
    "features": { ... },
    "abc_notation": "X:1\nT:..."
  },
  {
    "sample_idx": 0,
    "prompt_id": 1,
    "mode": "convergent",
    "temperature": 0.4,
    "visual_prompt": "An uplifting, joyful scene...",
    "features": { ... },
    "abc_notation": "X:1\nT:..."
  },
  // ... 498 more prompts
]
```

**Format**: Flat list, one entry per prompt (500 total)

**Usage**: Feed directly into SDXL image generation pipeline

### 3. `generation_summary.json` (Statistics)

Summary statistics:

```json
{
  "total_samples": 100,
  "total_prompts": 500,
  "convergent_prompts": 300,
  "divergent_prompts": 200,
  "generation_timestamp": "2025-11-05T14:30:45.123456",
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

**Usage**: Quick statistics, quality assurance, error tracking

---

## Prompt Generation Details

### What Gets Generated

**For Each Audio Sample**:
1. **Musical Feature Extraction**: Key, tempo, tonality, melody, harmony, dynamics, mood
2. **ABC Notation**: Text representation for LLM understanding
3. **5 Visual Prompts**:
   - **3 Convergent Prompts** (Temperature = 0.4)
     - Consistent, reproducible results
     - Suitable for baseline, reference
     - Good for controlled experiments
   - **2 Divergent Prompts** (Temperature = 0.8)
     - Creative, exploratory results
     - More variation and novelty
     - Good for diversity assessment

### Prompt Generation Process

```
Audio (16kHz)
    ↓
[Feature Extraction] → Key, Tempo, Tonality, Melody, etc.
    ↓
[ABC Notation Generation] → Text representation for LLM
    ↓
[Prompt Building] → Music-to-visual mapping from paper
    ↓
[LLM Processing] → Claude/Ollama generates visual description
    ↓
[5 Prompts] → 3 convergent + 2 divergent variations
```

### Example Generated Prompts

**Input**:
- Audio: Upbeat pop song, 120 BPM, major key
- Extracted: Tempo=120, Tonality=major, Mood=happy, Melody=ascending

**Generated Prompts**:

1. **Convergent (T=0.4) - Prompt 1**:
   "A vibrant pop concert stage with bright stage lighting, golden and cyan neon lights illuminating an energetic performer dancing dynamically on stage, with pulsing rhythm matching the upbeat tempo"

2. **Convergent (T=0.4) - Prompt 2**:
   "Sunlit outdoor festival scene with colorful flags and banners, happy crowd dancing rhythmically, golden hour lighting creating warm glowing atmosphere, synchronized movement with upbeat musical tempo"

3. **Convergent (T=0.4) - Prompt 3**:
   "Modern dance studio with dynamic lighting effects, performers moving with ascending motion patterns, major chord progressions visualized as ascending color gradients from warm yellow to bright orange"

4. **Divergent (T=0.8) - Prompt 1**:
   "Kaleidoscopic mandala patterns expanding outward, iridescent particles flowing in ascending spirals, electric cyan and magenta gradients pulsing at 120 BPM, hypnotic visual rhythm"

5. **Divergent (T=0.8) - Prompt 2**:
   "Ethereal garden with floating geometric crystals, luminescent flowers blooming in synchronization with tempo, golden sunlight refracted through prismatic elements creating ascending rainbow waves"

---

## Processing Information

### Performance Characteristics

| Component | Time per Sample | Total for 100 |
|-----------|-----------------|---------------|
| Feature Extraction | ~100ms | ~10s |
| Each LLM Prompt | 3-5s (Claude) | - |
| 5 Prompts per Sample | 15-25s | 25-40 min |
| **Total for 100 Samples** | - | **40-67 minutes** |

**Factors**:
- LLM provider (Claude API: ~3-5s, Ollama: ~5-15s)
- Network latency
- Model complexity
- System load

### Checkpointing

The generator automatically saves checkpoint files every 10 samples:
- `prompts_checkpoint_010.json` (after 10 samples)
- `prompts_checkpoint_020.json` (after 20 samples)
- etc.

If generation is interrupted, you can resume from the last checkpoint.

### Error Handling

The generator:
- ✅ Catches and logs all errors per sample
- ✅ Continues processing remaining samples if one fails
- ✅ Saves results even if some samples have errors
- ✅ Reports error count in summary
- ✅ Maintains sample_idx for error traceability

---

## Using Generated Prompts

### For Image Generation (SDXL)

```python
import json
from image_generator import create_image_generator

# Load prompts
with open('generated_prompts/prompts_for_image_generation.json') as f:
    prompts = json.load(f)

# Create image generator
generator = create_image_generator(device='cuda', use_refiner=True)

# Generate images
results = []
for i, prompt_data in enumerate(prompts):
    print(f"Generating {i+1}/{len(prompts)}")

    images = generator.generate(
        prompt=prompt_data['visual_prompt'],
        num_images=1,
        seed=i  # For reproducibility
    )

    results.append({
        'sample_idx': prompt_data['sample_idx'],
        'prompt_id': prompt_data['prompt_id'],
        'mode': prompt_data['mode'],
        'image': images[0]
    })

# Save images
for result in results:
    filename = f"image_sample{result['sample_idx']:03d}_prompt{result['prompt_id']}.png"
    result['image'].save(filename)
```

### For Creativity Evaluation

```python
import json
from creativity_evaluator import MusicToImageCreativityEvaluator

# Load prompts
with open('generated_prompts/visual_prompts_complete.json') as f:
    data = json.load(f)

# Evaluate creativity
evaluator = MusicToImageCreativityEvaluator()
results = []

for sample in data['samples']:
    for prompt_data in sample['prompts']:
        metrics = evaluator.evaluate(
            prompt=prompt_data['visual_prompt'],
            musical_features=sample['musical_features']
        )

        results.append({
            'sample_idx': sample['sample_idx'],
            'prompt_id': prompt_data['prompt_id'],
            'mode': prompt_data['mode'],
            'originality': metrics.originality,
            'elaboration': metrics.elaboration,
            'alignment': metrics.alignment,
            'coherence': metrics.coherence,
            'overall': metrics.overall
        })

# Analyze results
convergent_scores = [r['overall'] for r in results if r['mode'] == 'convergent']
divergent_scores = [r['overall'] for r in results if r['mode'] == 'divergent']

print(f"Convergent average: {sum(convergent_scores)/len(convergent_scores):.2f}")
print(f"Divergent average: {sum(divergent_scores)/len(divergent_scores):.2f}")
```

### For Research Analysis

```python
import json
import numpy as np

# Load complete data
with open('generated_prompts/visual_prompts_complete.json') as f:
    data = json.load(f)

# Analyze by music features
tempo_data = []
for sample in data['samples']:
    tempo = sample['musical_features']['tempo']
    num_prompts = len(sample['prompts'])

    tempo_data.append({
        'tempo': tempo,
        'prompt_count': num_prompts,
        'features': sample['musical_features']
    })

# Sort by tempo
tempo_data.sort(key=lambda x: x['tempo'])

# Find patterns
slow_samples = [t for t in tempo_data if t['tempo'] < 80]
medium_samples = [t for t in tempo_data if 80 <= t['tempo'] <= 120]
fast_samples = [t for t in tempo_data if t['tempo'] > 120]

print(f"Slow tempo (<80 BPM): {len(slow_samples)} samples")
print(f"Medium tempo (80-120 BPM): {len(medium_samples)} samples")
print(f"Fast tempo (>120 BPM): {len(fast_samples)} samples")
```

---

## Examples

### Run All Examples

```bash
python3 example_batch_generation.py
```

### Run Specific Example

```bash
# Example 1: Full batch (all 100 samples)
python3 example_batch_generation.py 1

# Example 2: Partial batch (first 10)
python3 example_batch_generation.py 2

# Example 3: With mel-spectrogram
python3 example_batch_generation.py 3

# Example 4: Load and inspect
python3 example_batch_generation.py 4

# Example 5: Access for image generation
python3 example_batch_generation.py 5
```

---

## Troubleshooting

### Issue: "No module named 'music_to_image_paper_pipeline'"

**Solution**: Ensure you're in the correct directory:
```bash
cd /path/to/FA_project/project
python3 generate_visual_prompts_batch.py
```

### Issue: "OLLAMA_HOST refused connection"

**Solution**: Start Ollama server first:
```bash
ollama serve
# In another terminal, run batch generation
```

### Issue: "Out of memory" or very slow

**Solution**: Process fewer samples at a time:
```bash
# Process 20 samples per run
python3 generate_visual_prompts_batch.py --samples 20 --start-idx 0
python3 generate_visual_prompts_batch.py --samples 20 --start-idx 20
# ... repeat
```

### Issue: Generation interrupted

**Solution**: Resume from checkpoint:
```bash
# Find the latest checkpoint
ls -lt generated_prompts/prompts_checkpoint_*.json | head -1

# Continue from there
python3 generate_visual_prompts_batch.py --start-idx 50
```

---

## File Structure

```
FA_project/
├── project/
│   ├── generate_visual_prompts_batch.py  # Main batch generator
│   ├── example_batch_generation.py       # Examples
│   ├── run_batch_generation.sh           # Shell script
│   └── BATCH_GENERATION_GUIDE.md         # This file
│
└── generated_prompts/
    ├── visual_prompts_complete.json      # Full dataset
    ├── prompts_for_image_generation.json # Image pipeline format
    ├── generation_summary.json           # Statistics
    └── prompts_checkpoint_*.json         # Checkpoint files
```

---

## Next Steps

1. **Generate Prompts**: Run batch generation on all 100 samples
2. **Evaluate Creativity**: Use `creativity_evaluator.py` to measure prompt quality
3. **Generate Images**: Use `image_generator.py` to create visual outputs
4. **Analyze Results**: Compare convergent vs divergent prompts

---

## Summary

✅ **Complete batch generation pipeline ready**
- Processes all 100 audio samples
- Generates 5 prompts per sample (500 total)
- Saves in multiple formats for different uses
- Includes error handling and checkpointing
- Ready for image generation pipeline

**Time to complete**: 40-67 minutes (depending on LLM provider)

**Storage needed**: ~2-5 MB for prompts, ~100+ GB for generated images (if using SDXL)
