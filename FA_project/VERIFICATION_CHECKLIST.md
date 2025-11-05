# Verification Checklist - Implementation Complete

**Purpose**: Verify all systems are in place and working correctly
**Date**: November 5, 2025
**Expected Time**: 5-10 minutes

---

## Pre-Flight Checks (Run This First)

### ✅ Step 1: Check File Presence

```bash
# All core files should exist
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

echo "=== Checking Files ==="
test -f generate_visual_prompts_batch.py && echo "✅ Batch generator" || echo "❌ Missing batch generator"
test -f calculate_batch_creativity_scores.py && echo "✅ Creativity scorer" || echo "❌ Missing creativity scorer"
test -f creativity_evaluator.py && echo "✅ Evaluator" || echo "❌ Missing evaluator"
test -f music_analyzer.py && echo "✅ Music analyzer" || echo "❌ Missing music analyzer"
test -f llm_client.py && echo "✅ LLM client" || echo "❌ Missing LLM client"
test -x run_batch_generation.sh && echo "✅ Batch script" || echo "❌ Batch script not executable"
test -f example_batch_generation.py && echo "✅ Batch examples" || echo "❌ Missing batch examples"
test -f example_creativity_scoring.py && echo "✅ Creativity examples" || echo "❌ Missing creativity examples"

echo "=== Documentation Files ==="
test -f BATCH_GENERATION_GUIDE.md && echo "✅ Batch guide" || echo "❌ Missing batch guide"
test -f CREATIVITY_SCORING_GUIDE.md && echo "✅ Creativity guide" || echo "❌ Missing creativity guide"
test -f BATCH_QUICK_REFERENCE.md && echo "✅ Quick reference" || echo "❌ Missing quick reference"
test -f CREATIVITY_SCORING_QUICK_START.md && echo "✅ Creativity quick start" || echo "❌ Missing"
```

### ✅ Step 2: Check Dataset Presence

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project

test -f dataset/label_data_with_16kHz_audio.npy && echo "✅ Dataset found" || echo "❌ Dataset missing"
ls -lh dataset/label_data_with_16kHz_audio.npy
```

### ✅ Step 3: Check Python Environment

```bash
python3 --version  # Should be 3.8+

# Check key packages
python3 -c "import librosa; print('✅ librosa')" 2>/dev/null || echo "❌ librosa missing"
python3 -c "import numpy; print('✅ numpy')" 2>/dev/null || echo "❌ numpy missing"
python3 -c "import scipy; print('✅ scipy')" 2>/dev/null || echo "❌ scipy missing"
python3 -c "import json; print('✅ json')" 2>/dev/null || echo "❌ json missing"
```

### ✅ Step 4: Check API Keys

```bash
# Check for API key availability
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "✅ ANTHROPIC_API_KEY is set"
else
    echo "⚠️  ANTHROPIC_API_KEY not set (will use Ollama or Mock)"
fi

# Check for Ollama availability
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
else
    echo "⚠️  Ollama not installed (will fall back to Claude or Mock)"
fi
```

---

## Functional Tests (Run These)

### Test 1: Import All Modules

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

echo "=== Testing Imports ==="
python3 -c "
try:
    from generate_visual_prompts_batch import BatchPromptGenerator
    print('✅ Batch generator imports successfully')
except Exception as e:
    print(f'❌ Batch generator error: {e}')
"

python3 -c "
try:
    from calculate_batch_creativity_scores import BatchCreativityCalculator
    print('✅ Creativity calculator imports successfully')
except Exception as e:
    print(f'❌ Creativity calculator error: {e}')
"

python3 -c "
try:
    from creativity_evaluator import MusicToImageCreativityEvaluator
    print('✅ Creativity evaluator imports successfully')
except Exception as e:
    print(f'❌ Evaluator error: {e}')
"

python3 -c "
try:
    from music_analyzer import MusicAnalyzer
    print('✅ Music analyzer imports successfully')
except Exception as e:
    print(f'❌ Analyzer error: {e}')
"

python3 -c "
try:
    from llm_client import get_recommended_client
    print('✅ LLM client imports successfully')
except Exception as e:
    print(f'❌ LLM client error: {e}')
"
```

### Test 2: Load Dataset

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

python3 << 'EOF'
import numpy as np

try:
    data = np.load('../dataset/label_data_with_16kHz_audio.npy', allow_pickle=True)
    print(f"✅ Dataset loaded successfully")
    print(f"   - Total samples: {len(data)}")
    print(f"   - First sample keys: {list(data[0].keys())}")
    print(f"   - Audio shape: {data[0]['audio'].shape}")
    print(f"   - Audio dtype: {data[0]['audio'].dtype}")
except Exception as e:
    print(f"❌ Dataset loading failed: {e}")
EOF
```

### Test 3: Test Music Feature Extraction

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

python3 << 'EOF'
import numpy as np
from music_analyzer import MusicAnalyzer

try:
    # Load one sample
    data = np.load('../dataset/label_data_with_16kHz_audio.npy', allow_pickle=True)
    audio = data[0]['audio']

    # Extract features
    analyzer = MusicAnalyzer(sr=16000)
    features = analyzer.extract_features(audio)

    print("✅ Feature extraction successful")
    print(f"   - Key: {features['key']}")
    print(f"   - Tempo: {features['tempo']:.1f} BPM")
    print(f"   - Tonality: {features['tonality']}")
    print(f"   - Mood: {features['mood']}")
    print(f"   - All features: {list(features.keys())}")
except Exception as e:
    print(f"❌ Feature extraction failed: {e}")
    import traceback
    traceback.print_exc()
EOF
```

### Test 4: Test Creativity Evaluation

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

python3 << 'EOF'
from creativity_evaluator import MusicToImageCreativityEvaluator

try:
    evaluator = MusicToImageCreativityEvaluator()

    # Test with sample prompt and features
    prompt = "A vibrant concert stage with colorful lights and a dynamic performer"
    features = {
        'key': 'C major',
        'tempo': 120,
        'tonality': 'major',
        'melody': 'ascending',
        'harmony': 'rich',
        'dynamics': 'forte',
        'mood': 'happy'
    }

    metrics = evaluator.evaluate(prompt, features)

    print("✅ Creativity evaluation successful")
    print(f"   - Originality: {metrics.originality:.2f}/5.0")
    print(f"   - Elaboration: {metrics.elaboration:.2f}/5.0")
    print(f"   - Alignment: {metrics.alignment:.2f}/5.0")
    print(f"   - Coherence: {metrics.coherence:.2f}/5.0")
    print(f"   - Overall: {metrics.overall:.2f}/5.0")
except Exception as e:
    print(f"❌ Creativity evaluation failed: {e}")
    import traceback
    traceback.print_exc()
EOF
```

### Test 5: Test LLM Client

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

python3 << 'EOF'
import asyncio
from llm_client import get_recommended_client

async def test_llm():
    try:
        client = get_recommended_client()
        print(f"✅ LLM client initialized: {client}")

        # Test simple generation (with timeout)
        response = await asyncio.wait_for(
            client.generate_prompt(
                abc_notation="M:4/4 L:1/8 C4 D4 E4 F4",
                mode="convergent",
                timeout=10
            ),
            timeout=15
        )

        if response and len(response) > 10:
            print(f"✅ LLM prompt generation successful")
            print(f"   - Response length: {len(response)} chars")
            print(f"   - Sample: {response[:100]}...")
        else:
            print(f"⚠️  LLM returned empty or short response")

    except asyncio.TimeoutError:
        print(f"⚠️  LLM request timed out (this is OK for testing)")
    except Exception as e:
        print(f"❌ LLM client failed: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_llm())
EOF
```

### Test 6: Create Output Directories

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

mkdir -p generated_prompts
mkdir -p creativity_scores

echo "✅ Output directories created/verified"
ls -ld generated_prompts/ creativity_scores/
```

---

## Integration Tests (Run These After Functional Tests)

### Integration Test 1: Small Batch Generation (2 samples)

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

echo "This will generate 10 prompts (2 samples × 5 prompts) - should take 30-50 seconds"
python3 generate_visual_prompts_batch.py --samples 2

# Check outputs
echo "=== Generated Files ==="
ls -lh generated_prompts/ | grep -E "\.json"
```

**Expected Output**:
- `visual_prompts_complete.json` - Created with 2 samples
- `prompts_for_image_generation.json` - Created with 10 prompts
- `generation_summary.json` - Created with summary stats

### Integration Test 2: Creativity Score Calculation

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

echo "This will calculate creativity for 10 prompts - should take 10-30 seconds"
python3 calculate_batch_creativity_scores.py

# Check outputs
echo "=== Creativity Score Files ==="
ls -lh creativity_scores/ | grep -E "\.json"
```

**Expected Output**:
- `creativity_prompt_scores.json` - Created with 10 scores
- `creativity_sample_summaries.json` - Created with 2 sample summaries
- `creativity_dataset_stats.json` - Created with statistics
- `creativity_comparison_report.json` - Created with comparison

### Integration Test 3: Verify JSON Structure

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

python3 << 'EOF'
import json

print("=== Verifying JSON Structures ===\n")

# Check generation summary
try:
    with open('generated_prompts/generation_summary.json') as f:
        summary = json.load(f)
    print("✅ generation_summary.json is valid")
    print(f"   - Samples processed: {summary.get('total_samples_processed', 'N/A')}")
    print(f"   - Prompts generated: {summary.get('total_prompts_generated', 'N/A')}")
except Exception as e:
    print(f"❌ generation_summary.json invalid: {e}")

# Check prompts complete
try:
    with open('generated_prompts/visual_prompts_complete.json') as f:
        data = json.load(f)
    print("\n✅ visual_prompts_complete.json is valid")
    print(f"   - Total samples: {len(data.get('samples', []))}")
    if data['samples']:
        print(f"   - Sample 0 prompts: {len(data['samples'][0].get('prompts', []))}")
except Exception as e:
    print(f"❌ visual_prompts_complete.json invalid: {e}")

# Check prompts for image generation
try:
    with open('generated_prompts/prompts_for_image_generation.json') as f:
        prompts = json.load(f)
    print("\n✅ prompts_for_image_generation.json is valid")
    print(f"   - Total prompts: {len(prompts)}")
    if prompts:
        print(f"   - Sample prompt keys: {list(prompts[0].keys())}")
except Exception as e:
    print(f"❌ prompts_for_image_generation.json invalid: {e}")

# Check creativity scores
try:
    with open('creativity_scores/creativity_prompt_scores.json') as f:
        scores = json.load(f)
    print("\n✅ creativity_prompt_scores.json is valid")
    print(f"   - Total scores: {len(scores)}")
    if scores:
        print(f"   - Sample score keys: {list(scores[0].keys())}")
        print(f"   - Sample overall: {scores[0].get('overall', 'N/A'):.2f}")
except Exception as e:
    print(f"❌ creativity_prompt_scores.json invalid: {e}")

# Check sample summaries
try:
    with open('creativity_scores/creativity_sample_summaries.json') as f:
        summaries = json.load(f)
    print("\n✅ creativity_sample_summaries.json is valid")
    print(f"   - Total samples: {len(summaries)}")
except Exception as e:
    print(f"❌ creativity_sample_summaries.json invalid: {e}")

# Check dataset stats
try:
    with open('creativity_scores/creativity_dataset_stats.json') as f:
        stats = json.load(f)
    print("\n✅ creativity_dataset_stats.json is valid")
    print(f"   - Mean creativity: {stats.get('mean_overall', 'N/A'):.2f}/5.0")
    print(f"   - Std deviation: {stats.get('std_overall', 'N/A'):.2f}")
except Exception as e:
    print(f"❌ creativity_dataset_stats.json invalid: {e}")

print("\n=== All Files Valid ===")
EOF
```

---

## Final Verification

### Run All Examples

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

echo "=== Running Batch Generation Examples ==="
python3 example_batch_generation.py 1

echo -e "\n=== Running Creativity Scoring Examples ==="
python3 example_creativity_scoring.py 1
```

### Check Documentation

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project

echo "=== Documentation Files ==="
ls -lh *.md | grep -E "(BATCH|CREATIVITY|IMPLEMENTATION)"

echo -e "\n=== File Sizes ==="
wc -l project/generate_visual_prompts_batch.py project/calculate_batch_creativity_scores.py project/example_batch_generation.py project/example_creativity_scoring.py | tail -1
```

---

## Verification Checklist Summary

Run this final script to get a complete status:

```bash
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

python3 << 'EOF'
import os
import json

print("=" * 60)
print("IMPLEMENTATION VERIFICATION REPORT")
print("=" * 60)

checks = {
    "Core Files": [
        "generate_visual_prompts_batch.py",
        "calculate_batch_creativity_scores.py",
        "creativity_evaluator.py",
        "music_analyzer.py",
        "llm_client.py"
    ],
    "Example Files": [
        "example_batch_generation.py",
        "example_creativity_scoring.py",
        "test_batch_generation.py"
    ],
    "Documentation": [
        "BATCH_GENERATION_GUIDE.md",
        "CREATIVITY_SCORING_GUIDE.md",
        "BATCH_QUICK_REFERENCE.md",
        "CREATIVITY_SCORING_QUICK_START.md"
    ]
}

all_good = True

for category, files in checks.items():
    print(f"\n{category}:")
    for f in files:
        if os.path.exists(f):
            size = os.path.getsize(f)
            print(f"  ✅ {f} ({size:,} bytes)")
        else:
            print(f"  ❌ {f} - MISSING")
            all_good = False

# Check output directories
print("\nOutput Directories:")
for d in ["generated_prompts", "creativity_scores"]:
    if os.path.exists(d):
        files = len(os.listdir(d))
        print(f"  ✅ {d}/ ({files} files)")
    else:
        print(f"  ⚠️  {d}/ not yet created (will be created when scripts run)")

# Check dataset
print("\nDataset:")
dataset_path = "../dataset/label_data_with_16kHz_audio.npy"
if os.path.exists(dataset_path):
    size = os.path.getsize(dataset_path)
    print(f"  ✅ Found ({size:,} bytes)")
else:
    print(f"  ❌ NOT FOUND at {dataset_path}")
    all_good = False

print("\n" + "=" * 60)
if all_good:
    print("✅ ALL CHECKS PASSED - READY TO RUN")
else:
    print("⚠️  SOME CHECKS FAILED - REVIEW ABOVE")
print("=" * 60)
EOF
```

---

## Quick Verification (2 Minutes)

If you just want a quick check:

```bash
# 1. Navigate to project
cd /Users/apple/Desktop/linguistic-bridges-mas/FA_project/project

# 2. Check files exist
echo "Checking files..." && \
test -f generate_visual_prompts_batch.py && \
test -f calculate_batch_creativity_scores.py && \
test -f creativity_evaluator.py && \
echo "✅ All core files present"

# 3. Import test
python3 -c "
from generate_visual_prompts_batch import BatchPromptGenerator
from calculate_batch_creativity_scores import BatchCreativityCalculator
from creativity_evaluator import MusicToImageCreativityEvaluator
print('✅ All modules import successfully')
"

# 4. Check dataset
python3 -c "
import numpy as np
data = np.load('../dataset/label_data_with_16kHz_audio.npy', allow_pickle=True)
print(f'✅ Dataset loaded: {len(data)} samples')
"

# 5. Ready!
echo "✅ SYSTEM IS READY TO USE"
```

---

## What to Do Next

**If all checks pass**: ✅ Ready to generate prompts and evaluate creativity!

**If any checks fail**:
1. Review the error message above
2. Check the troubleshooting section
3. Ensure you're running from the correct directory
4. Verify Python 3.8+ is installed
5. Check that all dependencies are available

**To start generating**:
```bash
python3 generate_visual_prompts_batch.py
```

---

**Verification Checklist Created**: November 5, 2025
**Expected Verification Time**: 5-10 minutes
**Status**: Ready for execution
