# Music-to-Image Paper Implementation - Quick Start Guide

**Status**: ✅ Ready to Test
**Last Updated**: November 5, 2025

This guide helps you verify and run the paper-faithful music-to-image system implementation.

---

## 1. Prerequisites Check

### Dataset ✅
```bash
ls -lh ./FA_project/dataset/label_data_with_16kHz_audio.npy
# Expected: 422M file with 16kHz audio samples
```

### Python Environment
```bash
python3 --version
# Expected: Python 3.8+
```

---

## 2. Installation

### Step 1: Install Dependencies

```bash
cd ./FA_project/project

# Install all requirements
pip install -r requirements.txt

# Verify installations
python3 -c "import librosa; import numpy; import anthropic; print('✓ Dependencies installed')"
```

### Step 2: Set Up LLM (Choose One)

**Option A: Anthropic Claude API (Recommended)**
```bash
# Set API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Verify
python3 -c "from llm_client import get_recommended_client; print(get_recommended_client().get_model_name())"
```

**Option B: Local Ollama**
```bash
# Install Ollama from https://ollama.ai
ollama pull mistral
ollama serve

# In another terminal, verify
python3 -c "from llm_client import get_recommended_client; print(get_recommended_client().get_model_name())"
```

**Option C: Mock (No Setup - Testing Only)**
```bash
# No setup needed, system will auto-detect mock mode if no API available
```

---

## 3. Run the Paper Implementation

### Test 1: Basic Paper Implementation (Audio → Visual Prompt)

```bash
cd ./FA_project/project

python3 -c "
import asyncio
from music_to_image_paper_pipeline import MusicToImagePaperPipeline, AudioLoaderFromNPY
from llm_client import get_recommended_client

async def test():
    # Load sample audio
    loader = AudioLoaderFromNPY()
    audio, metadata = loader.load_sample(
        '../dataset/label_data_with_16kHz_audio.npy',
        sample_idx=0
    )

    # Create pipeline
    pipeline = MusicToImagePaperPipeline(
        sample_rate=16000,
        generation_mode='convergent'
    )

    # Get LLM client
    llm_client = get_recommended_client()

    # Process
    results = await pipeline.process_audio(audio, metadata, llm_client)

    # Display results
    print('\\n✓ MUSIC ANALYSIS COMPLETE')
    print(f'Key: {results[\"features\"][\"key\"]} {results[\"features\"][\"tonality\"]}')
    print(f'Tempo: {results[\"features\"][\"tempo\"]:.0f} BPM')
    print(f'Mood: {results[\"features\"][\"overall_mood\"]}')
    print(f'\\n✓ VISUAL PROMPT GENERATED')
    print(results['visual_prompt'][:300] + '...')

asyncio.run(test())
"
```

**Expected Output**:
```
✓ MUSIC ANALYSIS COMPLETE
Key: C Major
Tempo: 120 BPM
Mood: energetic

✓ VISUAL PROMPT GENERATED
A energetic visual scene in warm and bright colors...
```

### Test 2: Compare Generation Modes

```bash
python3 example_paper_implementation.py
```

This runs all 5 examples:
1. ✅ Basic paper implementation
2. ✅ Convergent vs Divergent modes comparison
3. ✅ Batch processing multiple samples
4. ✅ Mel-spectrogram enhancement
5. ✅ End-to-end with SDXL image generation

---

## 4. Key Files for Paper Replication

| File | Purpose | Key Class |
|------|---------|-----------|
| `music_analyzer.py` | Extract 8 musical features | `MusicAnalyzer`, `MusicalFeatures` |
| `prompt_builder_paper.py` | Build LLM prompt (paper-only) | `PromptBuilderPaper` |
| `music_to_image_paper_pipeline.py` | Main orchestrator | `MusicToImagePaperPipeline` |
| `image_generator.py` | SDXL image generation | `StableDiffusionXLGenerator` |
| `llm_client.py` | LLM abstraction | `ClaudeClient`, `OllamaClient` |

---

## 5. Paper Implementation Flow

```
Audio Input (16kHz)
    ↓
Feature Extraction (8 features)
    ├─ Key signature
    ├─ Tempo
    ├─ Time signature
    ├─ Melody contour
    ├─ Harmonic progression
    ├─ Dynamic intensity
    └─ Overall mood
    ↓
ABC Notation Generation
    (Text-based music representation)
    ↓
LLM Prompt Construction
    (Music features + ABC notation)
    ↓
LLM Analysis (Claude/Ollama)
    (Maps music to visual concepts)
    ↓
Visual Prompt Generation
    (Ready for image generation)
    ↓
SDXL Image Generation (Optional)
    (Hugging Face integration)
    ↓
Generated Image
```

---

## 6. Configuration

### Generation Modes

**Convergent (Temperature 0.4)**
- Consistent, reproducible results
- Use for: Reproducible research, benchmarking
```python
pipeline = MusicToImagePaperPipeline(generation_mode="convergent")
```

**Divergent (Temperature 0.8)**
- Creative variations
- Use for: Exploring alternatives, creative results
```python
pipeline = MusicToImagePaperPipeline(generation_mode="divergent")
```

### Optional Enhancements

**Mel-Spectrogram Analysis**
```python
pipeline = MusicToImagePaperPipeline(
    generation_mode="convergent",
    use_mel_spectrogram=True  # Adds spectral analysis
)
```

**SDXL Image Generation**
```python
from image_generator import create_image_generator

generator = create_image_generator(
    device="auto",       # GPU if available, CPU fallback
    use_refiner=True,    # Quality refinement
    num_steps=30,        # Inference steps (higher = better quality)
    guidance_scale=7.5   # How much to follow prompt
)

images, metadata = generator.generate(
    prompt=visual_prompt,
    seed=42,             # For reproducibility
    num_images=1
)
```

---

## 7. Troubleshooting

### Issue: "Librosa not found"
```bash
pip install librosa
```

### Issue: "LLM client not initialized"
```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Or use Ollama/mock
export OLLAMA_HOST=http://localhost:11434
```

### Issue: "Dataset not found"
```bash
# Verify path
ls -lh ./FA_project/dataset/label_data_with_16kHz_audio.npy

# Adjust path in code if needed
loader = AudioLoaderFromNPY()
audio, metadata = loader.load_sample(
    "../dataset/label_data_with_16kHz_audio.npy",  # Adjust path
    sample_idx=0
)
```

### Issue: "SDXL image generation too slow"
```python
# Use fewer inference steps
generator = create_image_generator(num_steps=15)  # Faster, lower quality

# Or use CPU (slower but no VRAM limit)
generator = create_image_generator(device="cpu")
```

---

## 8. Next Steps

1. **Run Basic Test**
   ```bash
   python3 example_paper_implementation.py
   ```

2. **Process Your Own Audio**
   ```python
   audio_loader = AudioLoaderFromNPY()
   audio, metadata = audio_loader.load_sample(
       "../dataset/label_data_with_16kHz_audio.npy",
       sample_idx=0  # Change this for different samples
   )
   ```

3. **Fine-Tune Parameters**
   - Adjust generation_mode (convergent/divergent)
   - Experiment with use_mel_spectrogram
   - Modify SDXL guidance_scale (lower=creative, higher=prompt-follow)

4. **Batch Process**
   ```python
   loader = AudioLoaderFromNPY()
   samples = loader.load_batch(
       "../dataset/label_data_with_16kHz_audio.npy",
       indices=[0, 1, 2, 3, 4]  # Process 5 samples
   )
   ```

5. **Compare with Original Paper**
   - Use convergent mode for reproducibility
   - Use fixed seeds for consistent results
   - Compare visual similarity metrics

---

## 9. File Organization

```
FA_project/
├── project/
│   ├── CORE PAPER IMPLEMENTATION:
│   │   ├── music_analyzer.py              # Feature extraction
│   │   ├── prompt_builder_paper.py        # Paper-faithful prompts
│   │   ├── music_to_image_paper_pipeline.py  # Main orchestrator
│   │   └── example_paper_implementation.py   # 5 examples
│   │
│   ├── IMAGE GENERATION:
│   │   └── image_generator.py             # SDXL integration
│   │
│   ├── INFRASTRUCTURE:
│   │   ├── llm_client.py                  # LLM abstraction
│   │   ├── config.yaml                    # Configuration
│   │   ├── requirements.txt                # Dependencies
│   │   └── README.md                      # Full documentation
│   │
│   └── EXTENSIONS (Optional):
│       ├── prompt_builder.py              # Multi-agent version
│       ├── music_to_image_pipeline.py     # Multi-agent version
│       └── example_usage.py               # Multi-agent examples
│
├── dataset/
│   └── label_data_with_16kHz_audio.npy   # Your audio data
│
└── papers/
    └── 2407.05584v1.pdf                  # Yang et al. paper
```

---

## 10. Performance Notes

**Feature Extraction**: ~100ms per sample
**LLM Analysis** (Claude): ~3-5 seconds per sample
**SDXL Image Generation**:
- With GPU (CUDA): ~30-60s for 30 steps
- With CPU: ~5-10 minutes

**Total Pipeline Time**:
- GPU: ~40-70 seconds per sample
- CPU: ~5-10 minutes per sample

---

## 11. Verification Checklist

- [ ] Dataset exists at `./FA_project/dataset/label_data_with_16kHz_audio.npy`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] LLM configured (Claude API, Ollama, or Mock)
- [ ] Run basic test: `python3 example_paper_implementation.py`
- [ ] Paper features extracted correctly
- [ ] Visual prompts generated
- [ ] (Optional) SDXL images generated

---

## 12. Support Resources

- **Full Documentation**: See `README.md` for complete module reference
- **Paper Summary**: See `PAPER_IMPLEMENTATION_SUMMARY.md` for framework details
- **Original Paper**: See `../papers/2407.05584v1.pdf`

---

## Citation

If you use this implementation, please cite the original paper:

```bibtex
@article{yang2024exploring,
  title={Exploring Real-Time Music-to-Image Systems for Creative Inspiration in Music Creation},
  author={Yang, Meng and Llano, Maria Teresa and McCormack, Jon},
  journal={arXiv preprint arXiv:2407.05584},
  year={2024}
}
```

---

**Ready to replicate the paper!** 🚀
Start with: `python3 example_paper_implementation.py`
