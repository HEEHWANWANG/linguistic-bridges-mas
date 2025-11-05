# Batch Prompt Generation - Quick Reference

## TL;DR: Run This

```bash
# Generate all 100 samples with 5 prompts each (500 total)
python3 generate_visual_prompts_batch.py
```

**Result**: 3 files in `generated_prompts/` directory ready to use.

---

## 3 Ways to Run

### 1️⃣ Simplest (All Samples)
```bash
python3 generate_visual_prompts_batch.py
```

### 2️⃣ Partial (First 20 Samples)
```bash
python3 generate_visual_prompts_batch.py --samples 20
```

### 3️⃣ Shell Script
```bash
./run_batch_generation.sh
```

---

## Output Files

| File | Size | Use For |
|------|------|---------|
| `visual_prompts_complete.json` | 2-5 MB | Complete data, research, analysis |
| `prompts_for_image_generation.json` | 2-5 MB | SDXL image generation |
| `generation_summary.json` | ~100 KB | Quick statistics |

---

## What Gets Generated

**Per Audio Sample**: 5 prompts
- 3x Convergent (T=0.4) - Consistent, reproducible
- 2x Divergent (T=0.8) - Creative, exploratory

**Total**: 100 samples × 5 prompts = **500 visual prompts**

---

## Time Estimate

| Provider | Per Sample | 100 Samples |
|----------|-----------|-------------|
| Claude API | 15-25s | 40-67 min |
| Ollama | 25-75s | 67-200 min |
| Mock | <1s | <2 min |

---

## Data Structure

```python
# Load for analysis
import json
with open('generated_prompts/visual_prompts_complete.json') as f:
    data = json.load(f)

# Access
data['metadata']  # Generation info
data['samples'][0]['musical_features']  # Extracted features
data['samples'][0]['prompts'][0]  # Individual prompt
```

---

## Command Options

```bash
python3 generate_visual_prompts_batch.py \
  --dataset <path>         # Dataset file (default: dataset/...)
  --output-dir <dir>       # Output directory (default: generated_prompts)
  --samples <n>            # How many to process (default: all)
  --start-idx <n>          # Start from sample N (default: 0)
  --mel-spectrogram        # Enable mel-spectrogram (flag)
  --batch-size <n>         # Prompts per sample (default: 5)
```

---

## Use Cases

### Image Generation
```python
import json
from image_generator import create_image_generator

with open('generated_prompts/prompts_for_image_generation.json') as f:
    prompts = json.load(f)

generator = create_image_generator()
for p in prompts:
    images = generator.generate(prompt=p['visual_prompt'])
```

### Creativity Evaluation
```python
from creativity_evaluator import MusicToImageCreativityEvaluator

evaluator = MusicToImageCreativityEvaluator()
for sample in data['samples']:
    for prompt in sample['prompts']:
        metrics = evaluator.evaluate(prompt['visual_prompt'],
                                   sample['musical_features'])
```

### Research Analysis
```python
# Compare convergent vs divergent
convergent = [p for s in data['samples'] for p in s['prompts']
              if p['mode'] == 'convergent']
divergent = [p for s in data['samples'] for p in s['prompts']
             if p['mode'] == 'divergent']
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Module not found" | Run from `FA_project/project/` directory |
| "Connection refused" | Start Ollama: `ollama serve` |
| Too slow | Use Claude API or process fewer samples |
| Generation interrupted | Restart from checkpoint file |

---

## Files Created

```
project/
├── generate_visual_prompts_batch.py      # Main script
├── example_batch_generation.py           # 5 examples
├── run_batch_generation.sh               # Bash wrapper
├── BATCH_GENERATION_GUIDE.md             # Full guide
└── BATCH_QUICK_REFERENCE.md              # This file

generated_prompts/
├── visual_prompts_complete.json          # Full data
├── prompts_for_image_generation.json     # Image format
├── generation_summary.json               # Stats
└── prompts_checkpoint_*.json             # Auto-saves
```

---

## Next Steps

1. ✅ Run batch generation
2. 📊 Evaluate creativity with `creativity_evaluator.py`
3. 🎨 Generate images with `image_generator.py`
4. 📈 Analyze results

---

**Ready?** → `python3 generate_visual_prompts_batch.py`
