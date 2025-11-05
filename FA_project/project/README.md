# Music-to-Image System: Paper Replication

**Status**: ✅ Production Ready | **Date**: November 6, 2025 | **Clean Release**

Generate high-quality SDXL images from audio samples using the music-to-image paper replication system.

---

## 🚀 Quick Start (3 Commands)

```bash
# Step 1: Generate 500 visual prompts from 100 audio samples (50-70 min)
python3 generate_visual_prompts_batch.py

# Step 2: Score prompts on 4 creativity dimensions (2-5 min)
python3 calculate_batch_creativity_scores.py

# Step 3: Generate SDXL images from prompts (2-6 hours)
python3 generate_images_from_prompts.py
```

**Total time**: ~3-4 hours (GPU) | **Output**: 500 high-quality PNG images + metadata

---

## 📖 Documentation

### Start Here
- **[SYSTEM_GUIDE.md](SYSTEM_GUIDE.md)** ⭐ - Complete system overview, architecture, configuration
- **[RUNNING_COMMANDS.md](RUNNING_COMMANDS.md)** ⭐ - All executable commands with examples

### Detailed Guides
- **[BATCH_GENERATION_GUIDE.md](BATCH_GENERATION_GUIDE.md)** - Phase 1: Generate visual prompts
- **[CREATIVITY_SCORING_GUIDE.md](CREATIVITY_SCORING_GUIDE.md)** - Phase 2: Evaluate creativity
- **[IMAGE_GENERATION_GUIDE.md](IMAGE_GENERATION_GUIDE.md)** - Phase 3: Generate SDXL images

### Reference
- **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - What was cleaned up and why

---

## 📊 System Overview

```
Audio (100 samples, 16 kHz)
         ↓
    [PHASE 1] generate_visual_prompts_batch.py
    Generate 5 prompts per sample (500 total)
         ↓
    500 visual prompts + features
         ↓
    [PHASE 2] calculate_batch_creativity_scores.py
    Score each prompt (originality, elaboration, alignment, coherence)
         ↓
    Creativity scores + statistics
         ↓
    [PHASE 3] generate_images_from_prompts.py
    Generate SDXL images (768×768 by default)
         ↓
    500 high-quality PNG images + metadata
```

---

## 🎯 Use Cases

### Quick Test (5 minutes)
```bash
# Test with 1 sample (5 prompts, 5 images)
python3 generate_visual_prompts_batch.py --samples 1
python3 calculate_batch_creativity_scores.py
python3 generate_images_from_prompts.py --limit 5 --width 512 --height 512
```

### Production Run (3-4 hours)
```bash
python3 generate_visual_prompts_batch.py
python3 calculate_batch_creativity_scores.py
python3 generate_images_from_prompts.py
```

### High-Quality Images (4-6 hours)
```bash
python3 generate_visual_prompts_batch.py
python3 calculate_batch_creativity_scores.py
python3 generate_images_from_prompts.py --refiner --steps 40
```

See [RUNNING_COMMANDS.md](RUNNING_COMMANDS.md) for more examples.

---

## 🛠️ Requirements

- Python 3.8+
- 16GB+ RAM
- GPU with 6GB+ VRAM (recommended) or CPU mode
- 20GB+ free disk space
- Dataset: `dataset/label_data_with_16kHz_audio.npy`

**Install dependencies**:
```bash
pip install -r requirements.txt
```

**Configure LLM**:
```bash
# Claude API (recommended)
export ANTHROPIC_API_KEY="sk-ant-..."

# OR: Ollama (free, local)
ollama serve  # In another terminal
export LLM_PROVIDER=ollama
```

---

## 📁 Project Structure

```
FA_project/project/
├─ 📖 SYSTEM_GUIDE.md                 ⭐ Start here
├─ 📖 RUNNING_COMMANDS.md             ⭐ Quick reference
├─ 📖 BATCH_GENERATION_GUIDE.md       (Phase 1 details)
├─ 📖 CREATIVITY_SCORING_GUIDE.md     (Phase 2 details)
├─ 📖 IMAGE_GENERATION_GUIDE.md       (Phase 3 details)
├─ 📖 CLEANUP_SUMMARY.md              (Project cleanup info)
│
├─ 🎯 Core Scripts (3 files)
│  ├─ generate_visual_prompts_batch.py
│  ├─ calculate_batch_creativity_scores.py
│  └─ generate_images_from_prompts.py
│
├─ 🔧 Support Libraries (7 files)
│  ├─ music_to_image_paper_pipeline.py
│  ├─ music_analyzer.py
│  ├─ creativity_evaluator.py
│  ├─ llm_client.py
│  ├─ image_generator.py
│  ├─ prompt_builder.py
│  └─ mel_spectrogram_converter.py
│
├─ ⚙️ Configuration
│  ├─ config.yaml
│  ├─ requirements.txt
│  └─ run_batch_generation.sh
│
└─ 📊 Data (created during execution)
   ├─ dataset/                      (Input audio)
   ├─ generated_prompts/            (Phase 1 output)
   ├─ creativity_scores/            (Phase 2 output)
   └─ images/                       (Phase 3 output)
```

---

## 💡 Key Features

✅ **Complete Paper Replication**
- Exact implementation of the music-to-image pipeline
- Feature extraction, prompt generation, image synthesis

✅ **Production Ready**
- Error handling and fault recovery
- Checkpointing every 10-50 items
- Comprehensive logging
- JSON output with detailed metadata

✅ **Flexible Configuration**
- Resolution: 512×512 to 1024×1024
- Inference steps: 20-50 (quality/speed trade-off)
- Optional refiner model
- GPU/CPU selection
- Test mode with limited samples

✅ **Well Documented**
- 2000+ lines of documentation
- Complete guides for each phase
- Command examples for all use cases
- Troubleshooting sections
- Time estimates

---

## 🚀 Common Commands

### Generate Prompts
```bash
# All 100 samples (default)
python3 generate_visual_prompts_batch.py

# First 10 samples
python3 generate_visual_prompts_batch.py --samples 10

# With Ollama
export LLM_PROVIDER=ollama
python3 generate_visual_prompts_batch.py
```

### Score Prompts
```bash
# All 500 prompts (default)
python3 calculate_batch_creativity_scores.py

# First 100 prompts (test)
python3 calculate_batch_creativity_scores.py --limit 100
```

### Generate Images
```bash
# Default: 768×768, 30 steps, 2-3 hours
python3 generate_images_from_prompts.py

# Fast: 512×512, 20 steps, 45 minutes
python3 generate_images_from_prompts.py --width 512 --height 512 --steps 20

# High quality: 768×768, 40 steps + refiner, 4-6 hours
python3 generate_images_from_prompts.py --refiner --steps 40

# Test: Just 10 images
python3 generate_images_from_prompts.py --limit 10 --width 512 --height 512
```

See [RUNNING_COMMANDS.md](RUNNING_COMMANDS.md) for complete command reference.

---

## 📊 Output Examples

**Phase 1 Output** (`generated_prompts/`)
```json
{
  "samples": [
    {
      "sample_idx": 0,
      "musical_features": {
        "key": "C major",
        "tempo": 120,
        "mood": "happy"
      },
      "prompts": [
        {
          "prompt_id": 0,
          "mode": "convergent",
          "temperature": 0.4,
          "visual_prompt": "A vibrant concert stage..."
        }
      ]
    }
  ]
}
```

**Phase 2 Output** (`creativity_scores/`)
```
- creativity_prompt_scores.json (500 individual scores)
- creativity_sample_summaries.json (100 sample aggregations)
- creativity_dataset_stats.json (overall statistics)
- creativity_comparison_report.json (convergent vs divergent)
```

**Phase 3 Output** (`images/`)
```
images/
├── sample_000/
│   ├── sample_000_prompt_00.png
│   ├── sample_000_prompt_01.png
│   ... (5 images per sample)
├── sample_001/
... (100 samples total, 500 images)
├── image_generation_log.json
└── image_generation_summary.json
```

---

## 🔍 Verify Installation

```bash
# Check Python version
python3 --version

# Check dependencies
pip list | grep -E "torch|transformers|diffusers"

# Check GPU availability
python3 << 'EOF'
import torch
print(f"GPU available: {torch.cuda.is_available()}")
EOF

# Check dataset
ls -lh dataset/label_data_with_16kHz_audio.npy
```

---

## ⚡ Performance

### Time Estimates
| Phase | Task | Time |
|-------|------|------|
| 1 | Generate 500 prompts | 50-70 min |
| 2 | Score 500 prompts | 2-5 min |
| 3 | Generate 500 images (512px) | 45 min |
| 3 | Generate 500 images (768px) | 2-3 hours |
| 3 | Generate 500 images (768px + refiner) | 4-6 hours |
| **Total** | **All phases** | **~3-4 hours** |

### Memory Requirements
- **System RAM**: 16GB+
- **GPU VRAM**: 6GB+ (for 512×512), 10GB+ (for 768×768)
- **Disk Space**: 20GB+ (for models + outputs)

---

## 🆘 Troubleshooting

### "CUDA out of memory"
```bash
# Reduce resolution
python3 generate_images_from_prompts.py --width 512 --height 512

# Reduce steps
python3 generate_images_from_prompts.py --steps 20

# Use CPU
python3 generate_images_from_prompts.py --device cpu
```

### "Prompts file not found"
```bash
# Generate prompts first
python3 generate_visual_prompts_batch.py
```

### "LLM connection failed"
```bash
# Check API key
echo $ANTHROPIC_API_KEY

# Or use Ollama
export LLM_PROVIDER=ollama
ollama serve  # In another terminal
```

See [SYSTEM_GUIDE.md](SYSTEM_GUIDE.md) for comprehensive troubleshooting.

---

## 📚 Further Reading

- [SYSTEM_GUIDE.md](SYSTEM_GUIDE.md) - Complete overview of the system
- [RUNNING_COMMANDS.md](RUNNING_COMMANDS.md) - All commands reference
- [BATCH_GENERATION_GUIDE.md](BATCH_GENERATION_GUIDE.md) - Prompt generation details
- [CREATIVITY_SCORING_GUIDE.md](CREATIVITY_SCORING_GUIDE.md) - Creativity metrics
- [IMAGE_GENERATION_GUIDE.md](IMAGE_GENERATION_GUIDE.md) - Image generation details

---

## 📝 License

Paper replication implementation, November 2025

---

**Ready to start?** → Read [SYSTEM_GUIDE.md](SYSTEM_GUIDE.md) or run the [Quick Start](#-quick-start-3-commands) commands above.
