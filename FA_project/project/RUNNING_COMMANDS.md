# Running Commands Reference

**Quick reference for all executable commands in the system.**

---

## 🎯 Complete Workflow (Start to Finish)

### Full Production Run

```bash
# Step 1: Generate all 500 prompts from 100 audio samples (50-70 min)
python3 generate_visual_prompts_batch.py

# Step 2: Score all 500 prompts on 4 creativity dimensions (2-5 min)
python3 calculate_batch_creativity_scores.py

# Step 3: Generate 500 SDXL images from prompts (2-6 hours)
python3 generate_images_from_prompts.py
```

### Quick Test Run (5-15 minutes)

```bash
# Generate just 10 prompts (1 sample)
python3 generate_visual_prompts_batch.py --samples 1

# Score those prompts
python3 calculate_batch_creativity_scores.py

# Generate images from those prompts (512×512, fast)
python3 generate_images_from_prompts.py --limit 10 --width 512 --height 512
```

---

## 📝 Step 1: Visual Prompt Generation

### Basic Command

```bash
python3 generate_visual_prompts_batch.py
```

Generates 500 prompts from all 100 audio samples (50-70 minutes with Claude API).

### Common Variations

**Test with fewer samples** (5 samples = 25 prompts):
```bash
python3 generate_visual_prompts_batch.py --samples 5
```

**Start from specific sample** (resume after interruption):
```bash
python3 generate_visual_prompts_batch.py --start-idx 50 --samples 50
```

**Use Ollama instead of Claude** (free, local, slower):
```bash
export LLM_PROVIDER=ollama
python3 generate_visual_prompts_batch.py
```

**Use mel-spectrogram enhancement** (better audio analysis):
```bash
python3 generate_visual_prompts_batch.py --mel-spectrogram
```

**Custom output directory**:
```bash
python3 generate_visual_prompts_batch.py --output-dir my_prompts
```

**Change batch size** (prompts per sample):
```bash
python3 generate_visual_prompts_batch.py --batch-size 10
```

### Environment Variables

```bash
# Set Claude API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Use Ollama as LLM provider
export LLM_PROVIDER=ollama

# Run the script
python3 generate_visual_prompts_batch.py
```

---

## 📊 Step 2: Creativity Scoring

### Basic Command

```bash
python3 calculate_batch_creativity_scores.py
```

Scores all 500 prompts on 4 dimensions (2-5 minutes).

### Common Variations

**Score only first 100 prompts** (test scoring):
```bash
python3 calculate_batch_creativity_scores.py --limit 100
```

**Custom input file** (if prompts saved elsewhere):
```bash
python3 calculate_batch_creativity_scores.py --prompts-file my_prompts/visual_prompts_complete.json
```

**Custom output directory**:
```bash
python3 calculate_batch_creativity_scores.py --output-dir my_scores
```

### Output Files Generated

After running:
- `creativity_scores/creativity_prompt_scores.json` (all 500 individual scores)
- `creativity_scores/creativity_sample_summaries.json` (100 sample aggregations)
- `creativity_scores/creativity_dataset_stats.json` (overall statistics)
- `creativity_scores/creativity_comparison_report.json` (convergent vs divergent)

---

## 🖼️ Step 3: Image Generation

### Basic Command (Recommended)

```bash
python3 generate_images_from_prompts.py
```

Generates 500 images at 768×768 with 30 inference steps (2-3 hours on GPU).

### Common Configurations

**Fast Mode** (lower quality, faster):
```bash
python3 generate_images_from_prompts.py --width 512 --height 512 --steps 20
```
- Time: ~45 minutes
- Quality: Fair
- File size: ~0.5MB per image

**High Quality Mode** (better quality with refiner):
```bash
python3 generate_images_from_prompts.py --refiner --steps 40 --width 768 --height 768
```
- Time: ~4-6 hours
- Quality: Excellent
- File size: ~1MB per image

**Ultra High Quality** (best quality, slowest):
```bash
python3 generate_images_from_prompts.py --width 1024 --height 1024 --steps 50 --refiner
```
- Time: ~8+ hours
- Quality: Outstanding
- File size: ~1.8MB per image

**Test Mode** (generate just 10 images to verify setup):
```bash
python3 generate_images_from_prompts.py --limit 10 --width 512 --height 512
```
- Time: ~5-10 minutes
- Use: Verify everything works before full run

**CPU Only Mode** (no GPU needed, very slow):
```bash
python3 generate_images_from_prompts.py --device cpu --width 512 --height 512
```
- Time: ~12-24 hours
- Use: If GPU not available

**Metadata Only** (no image files, just statistics):
```bash
python3 generate_images_from_prompts.py --no-save --steps 20
```
- Time: ~2-3 hours
- Use: If you only need statistics

### Image Dimension Options

```bash
# 512×512 (Very Fast)
python3 generate_images_from_prompts.py --width 512 --height 512

# 640×640 (Fast)
python3 generate_images_from_prompts.py --width 640 --height 640

# 768×768 (Default, Balanced)
python3 generate_images_from_prompts.py --width 768 --height 768

# 1024×1024 (Slow, High Quality)
python3 generate_images_from_prompts.py --width 1024 --height 1024
```

### Inference Steps Options

```bash
# 20 steps (Very Fast, Fair Quality)
python3 generate_images_from_prompts.py --steps 20

# 30 steps (Default, Good Quality)
python3 generate_images_from_prompts.py --steps 30

# 40 steps (Slower, Excellent Quality)
python3 generate_images_from_prompts.py --steps 40

# 50 steps (Very Slow, Outstanding Quality)
python3 generate_images_from_prompts.py --steps 50
```

### Device Selection

```bash
# Auto-detect (uses GPU if available)
python3 generate_images_from_prompts.py --device auto

# Force CUDA (GPU)
python3 generate_images_from_prompts.py --device cuda

# Force CPU
python3 generate_images_from_prompts.py --device cpu
```

### Custom Paths

```bash
# Custom prompts file
python3 generate_images_from_prompts.py --prompts-file my_prompts/prompts.json

# Custom output directory
python3 generate_images_from_prompts.py --output-dir ../my_images
```

---

## 🔧 Using Shell Script (Alternative)

The `run_batch_generation.sh` wrapper is available:

```bash
# Generate all prompts
./run_batch_generation.sh

# Generate first 20 samples
./run_batch_generation.sh dataset/label_data_with_16kHz_audio.npy generated_prompts 20

# With mel-spectrogram
./run_batch_generation.sh dataset/label_data_with_16kHz_audio.npy generated_prompts "" 0 true
```

---

## 📈 Analysis Commands

### View Prompt Generation Summary

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

### View Creativity Scores

```bash
python3 << 'EOF'
import json

with open('creativity_scores/creativity_dataset_stats.json') as f:
    stats = json.load(f)

print(f"Total prompts scored: {stats['total_prompts']}")
print(f"Average originality: {stats['originality_mean']:.3f}")
print(f"Average elaboration: {stats['elaboration_mean']:.3f}")
print(f"Average alignment: {stats['alignment_mean']:.3f}")
print(f"Average coherence: {stats['coherence_mean']:.3f}")
EOF
```

### Compare Convergent vs Divergent

```bash
python3 << 'EOF'
import json

with open('creativity_scores/creativity_comparison_report.json') as f:
    report = json.load(f)

conv = report['convergent_metrics']
div = report['divergent_metrics']

print("CONVERGENT vs DIVERGENT")
print(f"Count: {conv['count']} vs {div['count']}")
print(f"Originality: {conv['originality_avg']:.3f} vs {div['originality_avg']:.3f}")
print(f"Elaboration: {conv['elaboration_avg']:.3f} vs {div['elaboration_avg']:.3f}")
print(f"Alignment: {conv['alignment_avg']:.3f} vs {div['alignment_avg']:.3f}")
print(f"Coherence: {conv['coherence_avg']:.3f} vs {div['coherence_avg']:.3f}")
EOF
```

### View Image Generation Summary

```bash
python3 << 'EOF'
import json

with open('images/image_generation_summary.json') as f:
    summary = json.load(f)

print(f"Total images: {summary['total_images_generated']}")
print(f"Success rate: {summary['success_rate']:.1f}%")
print(f"Resolution: {summary['image_dimensions']}")
print(f"Inference steps: {summary['inference_steps']}")
print(f"Device: {summary['device']}")
EOF
```

### Count Generated Files

```bash
# Count total PNG files
find images -name "*.png" | wc -l

# List first sample
ls -lh images/sample_000/

# Check total size
du -sh images/
```

---

## 🔍 File Inspection Commands

### Check Prompt Structure

```bash
python3 << 'EOF'
import json

with open('generated_prompts/visual_prompts_complete.json') as f:
    data = json.load(f)

# Show first sample's structure
sample = data['samples'][0]
print(f"Sample 0 has {len(sample['prompts'])} prompts")
print(f"Features: {list(sample['musical_features'].keys())}")
print(f"First prompt: {sample['prompts'][0]['visual_prompt'][:100]}...")
EOF
```

### Extract Convergent Prompts Only

```bash
python3 << 'EOF'
import json

with open('generated_prompts/visual_prompts_complete.json') as f:
    data = json.load(f)

convergent = []
for sample in data['samples']:
    for prompt in sample['prompts']:
        if prompt['mode'] == 'convergent':
            convergent.append(prompt['visual_prompt'])

print(f"Found {len(convergent)} convergent prompts")
for i, p in enumerate(convergent[:3]):
    print(f"\n{i+1}. {p[:100]}...")
EOF
```

---

## 🚨 Troubleshooting Commands

### Check Installation

```bash
# Test Python imports
python3 -c "import torch; print(f'PyTorch: {torch.__version__}')"
python3 -c "import transformers; print(f'Transformers: {transformers.__version__}')"

# Check CUDA availability
python3 << 'EOF'
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
EOF
```

### Test LLM Connection

```bash
# Test Claude API
python3 << 'EOF'
from llm_client import get_recommended_client
client = get_recommended_client()
print(f"LLM Provider: {type(client).__name__}")
EOF

# Test Ollama
curl http://localhost:11434/api/tags
```

### Free GPU Memory

```bash
python3 << 'EOF'
import torch
torch.cuda.empty_cache()
print("GPU cache cleared")
EOF
```

### Check Output File Integrity

```bash
# Verify JSON files are valid
python3 << 'EOF'
import json

files = [
    'generated_prompts/visual_prompts_complete.json',
    'creativity_scores/creativity_prompt_scores.json',
    'images/image_generation_log.json'
]

for f in files:
    try:
        with open(f) as file:
            json.load(file)
        print(f"✓ {f}")
    except Exception as e:
        print(f"✗ {f}: {e}")
EOF
```

---

## 📋 Complete Examples

### Example 1: Minimal Test

```bash
# Generate 1 sample (5 prompts)
python3 generate_visual_prompts_batch.py --samples 1

# Score them
python3 calculate_batch_creativity_scores.py

# Generate images (quick)
python3 generate_images_from_prompts.py --limit 5 --width 512 --height 512
```

### Example 2: Production Quality

```bash
# Generate all prompts
python3 generate_visual_prompts_batch.py

# Score all
python3 calculate_batch_creativity_scores.py

# High quality images
python3 generate_images_from_prompts.py --refiner --steps 40 --width 768 --height 768
```

### Example 3: Fast Turnaround

```bash
# Quick prompts (first 20 samples)
python3 generate_visual_prompts_batch.py --samples 20

# Score them
python3 calculate_batch_creativity_scores.py

# Fast images (512×512, 20 steps)
python3 generate_images_from_prompts.py --limit 100 --width 512 --height 512 --steps 20
```

### Example 4: CPU-Only Mode

```bash
# No GPU needed (everything works on CPU)
python3 generate_visual_prompts_batch.py --samples 10

python3 calculate_batch_creativity_scores.py

python3 generate_images_from_prompts.py --device cpu --width 512 --height 512 --steps 20
```

---

## ⏱️ Time Estimates

| Step | Full (100 samples) | Quick (10 samples) | Fast (GPU) | CPU |
|------|-------|-------|-------|-------|
| Prompts | 50-70 min | 5-7 min | 50-70 min | N/A |
| Scoring | 2-5 min | <1 min | 2-5 min | 2-5 min |
| Images (512×512) | 45 min | 5 min | 45 min | 3-4 hours |
| Images (768×768, 30) | 2-3 hours | 15 min | 2-3 hours | 6-8 hours |
| **Total** | **~3-4 hours** | **~20 min** | **~3-4 hours** | **~9-12 hours** |

---

## 🎯 Recommended Commands by Use Case

**Just verify it works?**
```bash
python3 generate_visual_prompts_batch.py --samples 1
python3 calculate_batch_creativity_scores.py
python3 generate_images_from_prompts.py --limit 5 --width 512 --height 512
```

**Production quality?**
```bash
python3 generate_visual_prompts_batch.py
python3 calculate_batch_creativity_scores.py
python3 generate_images_from_prompts.py --refiner --steps 40
```

**No GPU?**
```bash
python3 generate_visual_prompts_batch.py --samples 10
python3 calculate_batch_creativity_scores.py
python3 generate_images_from_prompts.py --device cpu --width 512 --height 512
```

**Analysis only?**
```bash
python3 calculate_batch_creativity_scores.py
# Then use Python scripts above to analyze results
```

---

**Last Updated**: November 6, 2025
