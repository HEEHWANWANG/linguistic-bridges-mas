# Creativity Scoring - Quick Start

## TL;DR: Run This

```bash
python3 calculate_batch_creativity_scores.py
```

**What happens**: Scores all 500 prompts, saves results, prints summary

**Time**: 2-5 minutes

---

## 3 Output Files Created

1. **creativity_prompt_scores.json** (2-5 MB)
   - Individual scores for all 500 prompts
   - Use: Find best/worst prompts, detailed analysis

2. **creativity_sample_summaries.json** (0.5-2 MB)
   - Aggregated scores for each of 100 samples
   - Use: Per-sample analysis, feature correlation

3. **creativity_dataset_stats.json** (~50 KB)
   - Overall statistics for entire dataset
   - Use: Paper results, publication data

4. **creativity_comparison_report.json** (~2 KB)
   - Convergent vs divergent comparison
   - Use: Mode analysis, strategy recommendations

---

## What Gets Scored

**For each prompt (1-5 scale)**:
- **Originality**: How novel/unique?
- **Elaboration**: How detailed/rich?
- **Alignment**: How well matched to music?
- **Coherence**: Do elements work together?
- **Overall**: Weighted average

---

## Quick Commands

```bash
# Run scoring
python3 calculate_batch_creativity_scores.py

# Run examples
python3 example_creativity_scoring.py 1  # Simple scoring
python3 example_creativity_scoring.py 2  # Detailed analysis
python3 example_creativity_scoring.py 3  # Inspect scores
python3 example_creativity_scoring.py 4  # Comparison
python3 example_creativity_scoring.py 5  # Custom workflow
python3 example_creativity_scoring.py all  # All examples

# View results
head -50 creativity_scores/creativity_dataset_stats.json
```

---

## Load Results (Python)

```python
import json

# Load prompt scores
with open('creativity_scores/creativity_prompt_scores.json') as f:
    scores = json.load(f)

# Load dataset stats
with open('creativity_scores/creativity_dataset_stats.json') as f:
    stats = json.load(f)

# Find best prompt
best = max(scores, key=lambda x: x['overall'])
print(f"Best creativity: {best['overall']:.2f}")

# Find worst prompt
worst = min(scores, key=lambda x: x['overall'])
print(f"Worst creativity: {worst['overall']:.2f}")

# Dataset average
print(f"Average: {stats['mean_overall']:.2f}")

# Convergent vs divergent
print(f"Convergent: {stats['convergent_mean']:.2f}")
print(f"Divergent:  {stats['divergent_mean']:.2f}")
```

---

## Score Interpretation

| Score | Meaning |
|-------|---------|
| 1.0-2.0 | Very low creativity |
| 2.0-3.0 | Below average |
| 3.0-3.5 | Average |
| 3.5-4.0 | Good |
| 4.0-5.0 | Excellent |

---

## Use Results

### For Research Paper
- Report mean, std, min, max from `creativity_dataset_stats.json`
- Compare convergent vs divergent
- Discuss feature correlations

### For Image Generation
- Use highest-scoring prompts first
- Filter by creativity threshold
- Prioritize creative prompts

### For Analysis
- Find patterns in features
- Correlate with music tempo/mood
- Identify improvements needed

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| File not found | Run batch generation first |
| No module error | Run from project/ directory |
| Takes too long | Normal - 2-5 min is expected |
| Results look odd | Check batch generation completed successfully |

---

## Next Steps

1. Run: `python3 calculate_batch_creativity_scores.py`
2. Check: `ls -lh creativity_scores/`
3. Inspect: `head -50 creativity_scores/creativity_dataset_stats.json`
4. Analyze: Load JSON files and run custom analysis
5. Publish: Use scores in research paper/report

---

## Files

- **calculate_batch_creativity_scores.py** - Main script
- **example_creativity_scoring.py** - 5 examples
- **CREATIVITY_SCORING_GUIDE.md** - Full documentation
- **CREATIVITY_SCORING_QUICK_START.md** - This file

---

**Ready?** → Run: `python3 calculate_batch_creativity_scores.py`
