# Image Generation from Visual Prompts - Complete Guide

**Date**: November 5, 2025
**Status**: ✅ Production Ready
**Purpose**: Generate SDXL images from visual prompts created by audio analysis

---

## Overview

This guide shows how to generate high-quality images from the visual prompts created by the music-to-image system.

### What You're Doing

1. **Input**: Visual prompts saved in `generated_prompts/visual_prompts_complete.json`
   - 500 prompts (5 per audio sample × 100 samples)
   - Each prompt is a detailed text description

2. **Process**: Convert each prompt to an image using SDXL (Stable Diffusion XL)
   - Uses SDXL base model (2GB) + optional refiner (2GB)
   - Configurable quality and speed settings

3. **Output**:
   - PNG images organized in `images/sample_XXX/` directories
   - Metadata saved in JSON files
   - Statistics and generation log

---

## Quick Start

### Prerequisites

```bash
# Ensure you have generated prompts first
ls generated_prompts/visual_prompts_complete.json

# If file doesn't exist, generate prompts:
python3 generate_visual_prompts_batch.py
```

### Basic Usage (GPU, Fast)

```bash
# Generate all 500 images
python3 generate_images_from_prompts.py

# Time: ~2-4 hours (depending on GPU)
# Output: 500 PNG images in images/ directory
```

### Common Configurations

#### 1. **Test Mode** (Quick test before full run)

```bash
# Generate first 10 images only
python3 generate_images_from_prompts.py --limit 10

# Time: ~10-20 minutes
# Use: Verify everything works before full generation
```

#### 2. **Fast Mode** (Lower resolution)

```bash
# Generate 512x512 images (faster)
python3 generate_images_from_prompts.py --width 512 --height 512

# Time: ~1-2 hours
# Use: Quick results, smaller file sizes (~0.5MB per image)
```

#### 3. **High Quality Mode** (Better results, slower)

```bash
# Use refiner model for enhanced quality
python3 generate_images_from_prompts.py --refiner --steps 40

# Time: ~4-6 hours
# Use: Best quality results
```

#### 4. **CPU Only** (No GPU required)

```bash
# Generate on CPU (much slower)
python3 generate_images_from_prompts.py --device cpu

# Time: ~12-24 hours
# Use: If GPU not available
```

#### 5. **Metadata Only** (No image files)

```bash
# Don't save images to disk
python3 generate_images_from_prompts.py --no-save

# Time: ~2-4 hours
# Use: If you only need metadata/statistics
```

---

## Command-Line Options

```bash
python3 generate_images_from_prompts.py [OPTIONS]
```

### Available Options

| Option | Default | Description |
|--------|---------|-------------|
| `--width` | 768 | Image width (must be multiple of 8) |
| `--height` | 768 | Image height (must be multiple of 8) |
| `--steps` | 30 | Inference steps (higher = better quality, slower) |
| `--refiner` | False | Use refiner model for enhancement |
| `--device` | auto | cuda, cpu, or auto-detect |
| `--limit` | None | Max prompts to process (for testing) |
| `--samples` | None | Number of samples to process |
| `--no-save` | False | Don't save images, metadata only |
| `--prompts-file` | (auto) | Path to prompts JSON |
| `--output-dir` | ../images | Where to save images |

### Example Commands

```bash
# Generate first 20 prompts at high quality
python3 generate_images_from_prompts.py --limit 20 --steps 40

# Generate samples 0-10 only (50 prompts)
python3 generate_images_from_prompts.py --samples 10

# Generate 512x512 images using refiner
python3 generate_images_from_prompts.py --width 512 --height 512 --refiner

# Generate on CPU with lower resolution (faster)
python3 generate_images_from_prompts.py --device cpu --width 512 --height 512

# Just get statistics, don't save images
python3 generate_images_from_prompts.py --no-save --steps 20
```

---

## Understanding the Output

### Directory Structure

```
images/
├── sample_000/
│   ├── sample_000_prompt_00.png     (convergent)
│   ├── sample_000_prompt_01.png     (convergent)
│   ├── sample_000_prompt_02.png     (convergent)
│   ├── sample_000_prompt_03.png     (divergent)
│   └── sample_000_prompt_04.png     (divergent)
├── sample_001/
│   ├── sample_001_prompt_00.png
│   ├── ... (5 images per sample)
│   └── sample_001_prompt_04.png
├── ... (sample_002 through sample_099)
│
├── image_generation_log.json        (detailed metadata)
└── image_generation_summary.json    (statistics)
```

**Total**:
- 500 PNG files (one per prompt)
- ~500 MB total (1MB per image at 768x768)
- ~250 MB total (0.5MB per image at 512x512)

### Output Files

#### 1. `image_generation_log.json` (Detailed)

Contains metadata for every generated image:

```json
{
  "metadata": {
    "prompts_file": "...",
    "generation_timestamp": "2025-11-05T...",
    "total_prompts": 500,
    "image_height": 768,
    "image_width": 768,
    "num_inference_steps": 30,
    "use_refiner": false,
    "device": "cuda",
    "successful": 500,
    "failed": 0
  },
  "generated_images": [
    {
      "sample_idx": 0,
      "prompt_id": 0,
      "mode": "convergent",
      "temperature": 0.4,
      "visual_prompt": "A vibrant concert stage...",
      "image_path": "sample_000/sample_000_prompt_00.png",
      "status": "success"
    },
    // ... 499 more entries
  ]
}
```

#### 2. `image_generation_summary.json` (Statistics)

High-level statistics:

```json
{
  "generation_timestamp": "2025-11-05T...",
  "total_images_generated": 500,
  "total_images_failed": 0,
  "success_rate": 100.0,
  "by_mode": {
    "convergent": 300,
    "divergent": 200
  },
  "by_sample": {
    "0": {
      "convergent": 3,
      "divergent": 2,
      "failed": 0
    },
    // ... sample 1-99
  },
  "image_dimensions": "768x768",
  "inference_steps": 30,
  "used_refiner": false,
  "device": "cuda",
  "output_directory": "..."
}
```

---

## Performance & Quality Settings

### Inference Steps

| Steps | Quality | Speed | Use Case |
|-------|---------|-------|----------|
| 20 | Fair | Very Fast | Testing/preview |
| 30 | Good | Fast | Default (balanced) |
| 40 | Excellent | Slower | High quality |
| 50 | Outstanding | Very Slow | Publication quality |

### Image Dimensions

| Dimensions | Quality | File Size | Speed | Memory |
|-----------|---------|-----------|-------|--------|
| 512×512 | Good | ~0.5MB | Very Fast | 6GB |
| 640×640 | Better | ~0.7MB | Fast | 8GB |
| 768×768 | Excellent | ~1.0MB | Normal | 10GB |
| 1024×1024 | Outstanding | ~1.8MB | Slow | 12GB+ |

### Refiner Model

**Without Refiner** (faster):
```bash
python3 generate_images_from_prompts.py --steps 30
# Time: ~2-3 hours (500 images)
# Quality: Good
# Memory: 10GB
```

**With Refiner** (better quality):
```bash
python3 generate_images_from_prompts.py --refiner --steps 30
# Time: ~4-5 hours (500 images)
# Quality: Excellent
# Memory: 12GB+
```

---

## System Requirements

### Minimum Requirements
- **GPU**: NVIDIA GPU with 6GB VRAM (for 512×512 images)
- **Python**: 3.8+
- **Storage**:
  - 2GB for model downloads
  - 500MB-2GB for 500 generated images

### Recommended
- **GPU**: NVIDIA GPU with 10GB+ VRAM (for 768×768+ images)
- **RAM**: 16GB system RAM
- **Storage**: 20GB free (for models + images)

### CPU Only
- Works but very slow (~2 hours per image)
- Use only for testing

---

## Workflow Examples

### Example 1: Quick Test

```bash
# Test setup with 5 images
python3 generate_images_from_prompts.py --limit 5 --width 512 --height 512

# Check results
ls -lh images/
cat images/image_generation_summary.json

# Takes: ~5-10 minutes
```

### Example 2: Complete High-Quality Generation

```bash
# Generate all 500 at high quality
python3 generate_images_from_prompts.py --refiner --steps 40 --width 768 --height 768

# This will take 4-6 hours
# Result: 500 high-quality images (~500MB)
```

### Example 3: Convergent vs Divergent Comparison

```bash
# Generate all images
python3 generate_images_from_prompts.py

# Analyze results
python3 << 'EOF'
import json

with open('images/image_generation_log.json') as f:
    data = json.load(f)

convergent = [img for img in data['generated_images'] if img['mode'] == 'convergent']
divergent = [img for img in data['generated_images'] if img['mode'] == 'divergent']

print(f"Convergent images: {len(convergent)}")
print(f"Divergent images: {len(divergent)}")

# Find convergent images
for img in convergent[:3]:
    print(f"\n{img['image_path']}")
    print(f"  Prompt: {img['visual_prompt'][:80]}...")
EOF
```

---

## Troubleshooting

### Problem: "CUDA out of memory"

**Solution 1**: Reduce image resolution
```bash
python3 generate_images_from_prompts.py --width 512 --height 512
```

**Solution 2**: Reduce inference steps
```bash
python3 generate_images_from_prompts.py --steps 20
```

**Solution 3**: Disable refiner
```bash
python3 generate_images_from_prompts.py  # (default, no refiner)
```

### Problem: "Prompts file not found"

**Solution**: Generate prompts first
```bash
python3 generate_visual_prompts_batch.py
python3 generate_images_from_prompts.py
```

### Problem: Generation is very slow

**Cause 1**: Using CPU
```bash
# Check device in logs
grep "device:" generate_images.log

# Use GPU instead (if available)
python3 generate_images_from_prompts.py --device cuda
```

**Cause 2**: Too many inference steps
```bash
# Use fewer steps
python3 generate_images_from_prompts.py --steps 20
```

**Cause 3**: Image resolution too high
```bash
# Use lower resolution
python3 generate_images_from_prompts.py --width 512 --height 512
```

### Problem: "Out of disk space"

```bash
# Check disk usage
du -sh images/

# Solution: Delete old images or use lower resolution
python3 generate_images_from_prompts.py --width 512 --height 512
```

---

## Analysis & Next Steps

### View Generated Images

```bash
# List all generated images
ls -lh images/sample_000/

# Count total images
find images -name "*.png" | wc -l

# Check file sizes
du -sh images/
```

### Statistical Analysis

```python
import json
from pathlib import Path

# Load metadata
with open('images/image_generation_log.json') as f:
    log = json.load(f)

with open('images/image_generation_summary.json') as f:
    summary = json.load(f)

# Print statistics
print(f"Success rate: {summary['success_rate']:.1f}%")
print(f"Total images: {summary['total_images_generated']}")
print(f"Convergent: {summary['by_mode']['convergent']}")
print(f"Divergent: {summary['by_mode']['divergent']}")

# Group by sample
for sample_idx in range(5):  # First 5 samples
    sample_images = [img for img in log['generated_images']
                    if img['sample_idx'] == sample_idx]
    print(f"\nSample {sample_idx}: {len(sample_images)} images")
```

### Create Comparison Grid (Optional)

```python
from PIL import Image
import json

# Load log
with open('images/image_generation_log.json') as f:
    log = json.load(f)

# Get first sample's 5 images
sample_0_images = [img for img in log['generated_images']
                   if img['sample_idx'] == 0]

# Create 5-image grid
images = [Image.open(img['image_path']).resize((256, 256))
          for img in sample_0_images]

# Save grid (requires PIL)
# grid = Image.new('RGB', (5*256, 256))
# for i, img in enumerate(images):
#     grid.paste(img, (i*256, 0))
# grid.save('sample_0_comparison.png')
```

---

## Advanced Usage

### Using with Different Prompts

If you have prompts from another source:

```python
from generate_images_from_prompts import BatchImageGenerator

# Create custom prompts
custom_prompts = {
    'samples': [
        {
            'sample_idx': 0,
            'prompts': [
                {'prompt_id': 0, 'visual_prompt': 'Your custom prompt...',
                 'mode': 'convergent', 'temperature': 0.4}
            ]
        }
    ]
}

# Save to JSON
import json
with open('custom_prompts.json', 'w') as f:
    json.dump(custom_prompts, f)

# Generate images
generator = BatchImageGenerator(
    prompts_file='custom_prompts.json',
    output_dir='custom_images'
)
```

### Batch Processing Multiple Sets

```bash
# Generate set 1 (samples 0-20)
python3 generate_images_from_prompts.py --samples 20 --output-dir images_batch1

# Generate set 2 (samples 21-40)
python3 generate_images_from_prompts.py --samples 20 --output-dir images_batch2

# Generate set 3 (samples 41-60)
python3 generate_images_from_prompts.py --samples 20 --output-dir images_batch3
```

---

## Summary

### Quick Reference Commands

```bash
# Test (5 images, fast)
python3 generate_images_from_prompts.py --limit 5 --width 512 --height 512

# Fast (500 images, 768p)
python3 generate_images_from_prompts.py --width 768 --height 768 --steps 30

# High Quality (500 images, with refiner)
python3 generate_images_from_prompts.py --refiner --steps 40

# Metadata only (no image files)
python3 generate_images_from_prompts.py --no-save

# Check results
ls -lh images/
cat images/image_generation_summary.json
```

### Time Estimates

| Configuration | Time | Quality | Storage |
|---------------|------|---------|---------|
| 512px, 20 steps | 45 min | Fair | 250 MB |
| 768px, 30 steps | 2-3 hours | Good | 500 MB |
| 768px, 40 steps + refiner | 4-6 hours | Excellent | 500 MB |
| 1024px, 50 steps + refiner | 8+ hours | Outstanding | 1+ GB |

---

**Status**: ✅ Production Ready
**Ready to Generate**: Yes, run `python3 generate_images_from_prompts.py`
