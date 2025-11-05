# Music-to-Image Paper Implementation Architecture

**Framework**: Yang et al. (2407.05584v1) - Real-Time Music-to-Image Systems
**Status**: ✅ Production Ready
**Date**: November 5, 2025

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT: Audio (16kHz)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           PHASE 1: MUSIC FEATURE EXTRACTION                 │
│                  (music_analyzer.py)                        │
├─────────────────────────────────────────────────────────────┤
│ Extracts 8 musical features using librosa DSP:             │
│  ✓ Key signature (chroma analysis)                         │
│  ✓ Tonality (major/minor)                                  │
│  ✓ Tempo (onset detection → BPM)                           │
│  ✓ Time signature (tempogram analysis)                     │
│  ✓ Melody contour (pitch estimation)                       │
│  ✓ Harmonic progression (spectral analysis)                │
│  ✓ Dynamic intensity (energy analysis)                     │
│  ✓ Overall mood (derived from features)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         PHASE 2: ABC NOTATION GENERATION                    │
│              (MusicalFeatures.to_abc_notation)              │
├─────────────────────────────────────────────────────────────┤
│ Converts features to text-based music representation:       │
│ X:1                                                         │
│ T:Generated Song                                            │
│ M:4/4          (Time signature)                             │
│ L:1/8          (Note length)                                │
│ Q:120          (Tempo in BPM)                               │
│ K:Cmaj         (Key signature)                              │
│ C2 D2 E2 F2    (Melody contour)                             │
│                                                             │
│ Purpose: Text representation for LLM processing             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
         ┌─────────────┴────────────────┐
         │                              │
         ▼                              ▼
┌──────────────────────┐      ┌──────────────────────┐
│  Optional: Mel-      │      │  No Mel-Spectrogram  │
│  Spectrogram         │      │  (Paper default)     │
│  Analysis            │      │                      │
│  (mel_spectrogram... │      │  use_mel_spectrogram │
│   _converter.py)     │      │  = False             │
│                      │      │                      │
│ Adds spectral info:  │      └──────────┬───────────┘
│ - Energy per band    │                 │
│ - Spectral centroid  │                 │
│ - Temporal dynamics  │                 │
│ - ASCII visualizations         │
└──────────────┬────────┘        │
               └────────┬────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│       PHASE 3: LLM PROMPT CONSTRUCTION                      │
│             (PromptBuilderPaper.build_gpt_prompt)           │
├─────────────────────────────────────────────────────────────┤
│ Builds prompt containing:                                   │
│  1. ABC notation (music structure)                          │
│  2. Extracted musical features                              │
│  3. Paper's explicit music-to-visual mappings:              │
│     - Tempo → visual motion/pacing                          │
│     - Key/Tonality → color palette                          │
│     - Melody Contour → compositional flow                   │
│     - Harmony → visual complexity                           │
│     - Dynamics → contrast/saturation                        │
│  4. Instructions to LLM: map music to visual concepts       │
│                                                             │
│ OUTPUT: Complete prompt ready for LLM processing            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│      PHASE 4: LLM ANALYSIS (Visual Prompt Generation)       │
│              (llm_client.py + LLM Backend)                  │
├─────────────────────────────────────────────────────────────┤
│ Sends prompt to LLM (Claude/Ollama) with:                   │
│  Temperature control for generation mode:                   │
│    - Convergent: T=0.4 (consistent, reproducible)           │
│    - Divergent: T=0.8 (creative, exploratory)               │
│                                                             │
│ LLM Response: Detailed visual description ready for SDXL    │
│ Example output:                                             │
│  "A bright, energetic abstract composition with             │
│   swirling warm colors (golds, oranges) in rapid motion.    │
│   The mood is uplifting and dynamic, with sharp contrast    │
│   between light and shadow areas..."                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
       ┌───────────────┴───────────────┐
       │                               │
       ▼                               ▼
┌─────────────────────┐      ┌────────────────────┐
│  Paper Replication  │      │  Extended Use Case │
│  (Stop Here)        │      │  (Image Generation)│
│                     │      │                    │
│  Use visual prompt  │      │  Generate SDXL     │
│  directly for:      │      │  images using      │
│  - Analysis         │      │  image_generator.py│
│  - Benchmarking     │      │                    │
│  - User feedback    │      │  Config:           │
│  - Manual imagery   │      │  - Guidance scale  │
│                     │      │  - Inference steps │
│                     │      │  - Image size      │
└─────────────────────┘      │  - Optional refiner│
                             └────────┬───────────┘
                                      │
                                      ▼
                           ┌──────────────────────┐
                           │   Generated Image    │
                           │   (PNG, high quality)│
                           └──────────────────────┘
```

---

## 2. Core Components

### 2.1 Music Feature Extraction (`music_analyzer.py`)

```python
class MusicAnalyzer:
    def analyze_audio(audio: np.ndarray) -> MusicalFeatures:
        # Input: 1D waveform (16kHz)
        # Output: 8 musical features
        # Process:
        # 1. Chroma analysis → key_signature
        # 2. Tempogram → tempo
        # 3. Autocorrelation → time_signature
        # 4. Pitch tracking → melody_contour
        # 5. Spectral analysis → harmonic_progression
        # 6. Energy analysis → dynamic_intensity
        # 7. Feature combination → overall_mood

class MusicalFeatures:
    key_signature: str           # C, D, E, F, G, A, B
    tonality: str                # major or minor
    tempo: float                 # BPM
    time_signature: str          # 4/4, 3/4, 6/8, etc.
    melody_contour: str          # ascending, descending, stable, mixed
    harmonic_progression: str    # simple, moderate, complex
    dynamic_intensity: str       # soft, moderate, intense, very_intense
    overall_mood: str            # happy, sad, energetic, calm, etc.

    def to_abc_notation() -> str:
        # Converts features to ABC format for LLM
```

### 2.2 Prompt Builder - Paper Version (`prompt_builder_paper.py`)

```python
class PromptBuilderPaper:
    def __init__(self, generation_mode: str = "convergent"):
        # Modes:
        # - "convergent" (T=0.4): Consistent results
        # - "divergent" (T=0.8): Creative variation

    def build_gpt_prompt(
        features: MusicalFeatures,
        abc_notation: str,
        mel_spectrogram_text: Optional[str] = None,
        use_mel_spectrogram: bool = False
    ) -> str:
        # Builds prompt with:
        # 1. ABC notation input
        # 2. Extracted features
        # 3. Paper's music-to-visual mapping rules
        # 4. Instructions for visual prompt generation
        # Output: Complete LLM prompt
```

**Key Mapping Rules (from paper)**:
```
Tempo → Visual Motion
  Fast (>120 BPM) → Dynamic, energetic, rapid
  Moderate (80-120) → Balanced, moderate pacing
  Slow (<80) → Calm, serene, flowing

Key/Tonality → Color Palette
  Major → Warm, bright, positive
  Minor → Cool, dark, introspective

Melody Contour → Compositional Flow
  Ascending → Upward movement, growth, elevation
  Descending → Downward, grounding, settling
  Stable → Stillness, balance, centeredness

Harmonic Progression → Visual Complexity
  Simple → Clean, minimal
  Complex → Layered, intricate, rich details

Dynamic Intensity → Contrast & Saturation
  Intense → High contrast, saturated
  Soft → Subtle, muted, low contrast
```

### 2.3 Main Pipeline (`music_to_image_paper_pipeline.py`)

```python
class MusicToImagePaperPipeline:
    async def process_audio(
        audio_data: np.ndarray,
        metadata: Dict[str, Any],
        llm_client: LLMClient
    ) -> Dict[str, Any]:
        # Step 1: Extract musical features
        features = self.music_analyzer.analyze_audio(audio_data)

        # Step 2: Generate ABC notation
        abc_notation = features.to_abc_notation()

        # Step 3: Optional mel-spectrogram analysis
        if use_mel_spectrogram:
            mel_spec = self.mel_converter.audio_to_mel_spectrogram(audio)
            mel_text = self.mel_converter.mel_spectrogram_to_text(mel_spec)

        # Step 4: Build LLM prompt
        gpt_prompt = self.prompt_builder.build_gpt_prompt(
            features, abc_notation, mel_spectrogram_text
        )

        # Step 5: Send to LLM
        visual_prompt = await llm_client.analyze(gpt_prompt)

        # Return results with all intermediate data
        return {
            "features": {...},
            "abc_notation": abc_notation,
            "gpt_prompt": gpt_prompt,
            "visual_prompt": visual_prompt,
            "temperature": 0.4 or 0.8,
            "generation_mode": "convergent" or "divergent"
        }

class AudioLoaderFromNPY:
    @staticmethod
    def load_sample(npy_path: str, sample_idx: int = 0):
        # Load single audio sample from .npy file
        # Returns: (audio, metadata)

    @staticmethod
    def load_batch(npy_path: str, indices: List[int]):
        # Load multiple samples
        # Returns: List[(audio, metadata)]
```

### 2.4 LLM Client Abstraction (`llm_client.py`)

```python
class LLMClient(ABC):
    async def analyze(self, prompt: str) -> str:
        # Send prompt to LLM, return visual description

class ClaudeClient(LLMClient):
    # Uses Anthropic Claude API
    # Primary choice (recommended)

class OllamaClient(LLMClient):
    # Uses local Ollama models
    # Secondary choice (free, local)

class MockLLMClient(LLMClient):
    # Mock client for testing
    # Fallback mode (no API needed)

def get_recommended_client() -> LLMClient:
    # Auto-detects available LLM:
    # 1. Check Claude API key
    # 2. Check Ollama availability
    # 3. Fall back to Mock
```

### 2.5 Image Generator (`image_generator.py`)

```python
class StableDiffusionXLGenerator:
    def __init__(self, config: ImageGenerationConfig):
        # Loads:
        # - Base model: stabilityai/stable-diffusion-xl-base-1.0
        # - Optional refiner: stabilityai/stable-diffusion-xl-refiner-1.0

    def generate(
        prompt: str,
        negative_prompt: Optional[str] = None,
        num_images: int = 1,
        guidance_scale: float = 7.5,
        num_steps: int = 30,
        seed: Optional[int] = None,
        height: int = 1024,
        width: int = 1024
    ) -> Tuple[List[PIL.Image], Dict]:
        # Generates images from text prompt
        # Returns: (images, metadata)

def create_image_generator(
    device: str = "auto",      # GPU detection
    use_refiner: bool = True,  # Quality refinement
    height: int = 1024,
    width: int = 1024,
    num_steps: int = 30
) -> StableDiffusionXLGenerator:
    # Factory function
```

---

## 3. Data Flow Example

### Input: Audio Sample
```python
audio, metadata = loader.load_sample("dataset.npy", sample_idx=0)
# audio shape: (16000 * duration,)
# metadata: {"track_name": "...", "artist": "...", ...}
```

### Feature Extraction
```python
features = analyzer.analyze_audio(audio)
# MusicalFeatures(
#     key_signature="G",
#     tonality="major",
#     tempo=120.5,
#     time_signature="4/4",
#     melody_contour="ascending",
#     harmonic_progression="moderate",
#     dynamic_intensity="intense",
#     overall_mood="happy"
# )
```

### ABC Notation
```
X:1
T:Generated Song
M:4/4
L:1/8
Q:121
K:Gmaj
G2 A2 B2 c2 d2 | e2 d2 c2 B2 A2 |
G2 A2 B2 c2 d2 | e2 d2 c2 B2 A2 |
```

### LLM Prompt (Simplified)
```
You are an expert music-to-visual translator...

ABC NOTATION ANALYSIS:
[Full ABC notation from above]

EXTRACTED MUSICAL FEATURES:
- Key Signature: G major
- Tempo: 121 BPM
- Time Signature: 4/4
- Melody Contour: ascending
- Harmonic Progression: moderate
- Dynamic Intensity: intense
- Overall Mood: happy

MAPPING MUSIC TO VISUAL ELEMENTS:
[Paper's music-to-visual mapping rules]

YOUR TASK:
Generate a detailed visual prompt for SDXL image generation.
Output ONLY the visual prompt.
```

### LLM Response (Visual Prompt)
```
A vibrant, uplifting abstract composition with golden yellow and
bright orange tones creating a sense of joy and movement. The scene
features ascending flowing shapes and dynamic energy, with layered
elements creating visual complexity. The overall impression is warm,
energetic, and deeply optimistic, conveying the ascending melodic
journey of the music.
```

### SDXL Output (Optional)
```
[Generated 1024x1024 PNG image matching the visual prompt]
```

---

## 4. Generation Modes

### Convergent Mode (Temperature 0.4)
**Use Case**: Reproducible research, benchmarking
```python
pipeline = MusicToImagePaperPipeline(generation_mode="convergent")

# Characteristics:
# - Lower temperature (0.4) → more deterministic
# - LLM produces consistent visual descriptions
# - Same audio → similar visual prompts
# - Seed control in SDXL → reproducible images
```

### Divergent Mode (Temperature 0.8)
**Use Case**: Creative exploration, variation
```python
pipeline = MusicToImagePaperPipeline(generation_mode="divergent")

# Characteristics:
# - Higher temperature (0.8) → more creative
# - LLM produces varied visual descriptions
# - Same audio → different visual prompts
# - Useful for exploring multiple visual interpretations
```

---

## 5. Optional Enhancements

### Mel-Spectrogram Analysis
```python
pipeline = MusicToImagePaperPipeline(use_mel_spectrogram=True)

# Adds to LLM context:
# - Spectral energy distribution
# - Frequency band analysis (4 ranges)
# - Spectral centroid
# - Temporal dynamics
# - ASCII art visualizations

# Benefits:
# - Better frequency information
# - Complements melodic features
# - Enriches LLM understanding
```

### SDXL Image Generation
```python
visual_prompt = results["visual_prompt"]

generator = create_image_generator(
    device="auto",
    use_refiner=True,
    num_steps=30
)

images, metadata = generator.generate(
    prompt=visual_prompt,
    seed=42,
    num_images=1
)

images[0].save("output.png")
```

---

## 6. Configuration Parameters

### Music Analysis (`config.yaml`)
```yaml
audio:
  sample_rate: 16000        # Hz
  n_fft: 2048              # FFT window size
  hop_length: 512          # Frame shift

generation:
  convergent_temperature: 0.4
  divergent_temperature: 0.8

mel_spectrogram:
  enabled: false            # Optional
  n_mels: 128              # Mel bands
  n_fft: 2048
  hop_length: 512
```

### Image Generation
```python
create_image_generator(
    device="auto",                    # "cuda", "cpu", or "auto"
    use_refiner=True,                 # SDXL refiner
    height=1024,                      # 512-1024
    width=1024,                       # 512-1024
    num_steps=30                      # More = better quality
)

generator.generate(
    prompt=visual_prompt,
    guidance_scale=7.5,               # 1.0-20.0
    num_images=1,
    seed=42                           # For reproducibility
)
```

---

## 7. File Sizes and Dependencies

| File | Size | Dependencies |
|------|------|--------------|
| music_analyzer.py | 8 KB | librosa, numpy |
| prompt_builder_paper.py | 4 KB | pydantic |
| music_to_image_paper_pipeline.py | 10 KB | numpy, asyncio |
| image_generator.py | 15 KB | torch, diffusers, PIL |
| llm_client.py | 12 KB | anthropic/requests |
| mel_spectrogram_converter.py | 20 KB | librosa, numpy |
| **Total Core** | **~70 KB** | **Minimal footprint** |

---

## 8. Performance Characteristics

| Operation | Time (GPU) | Time (CPU) |
|-----------|-----------|-----------|
| Feature Extraction | ~100ms | ~100ms |
| ABC Notation | <1ms | <1ms |
| Mel-Spectrogram | ~100ms | ~200ms |
| LLM Analysis (Claude) | 3-5s | 3-5s |
| SDXL Generation (30 steps) | 30-60s | 5-10min |
| **Total Per Sample** | **~40-70s** | **~5-10min** |

---

## 9. Differences from Original Paper

| Aspect | Paper | This Implementation |
|--------|-------|-------------------|
| **Audio Input** | MIDI keyboard | 16kHz PCM audio |
| **Feature Extraction** | Symbolic MIDI | librosa DSP analysis |
| **LLM** | GPT-4 (OpenAI) | Claude/Ollama (no cost/local) |
| **Image Gen** | SDXL Turbo | SDXL (higher quality) |
| **Mel-Spectrogram** | Not used | Optional enhancement |

**Why Changes**:
- Audio instead of MIDI: Practical for music datasets
- Claude instead of GPT-4: No OpenAI subscription required
- SDXL instead of Turbo: Better image quality (slightly slower)
- Mel-spectrogram optional: Improves understanding without overhead

---

## 10. Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up LLM
export ANTHROPIC_API_KEY="your-api-key"

# 3. Run paper implementation
python3 example_paper_implementation.py

# Expected output:
# ✓ EXAMPLE 1: Basic paper implementation
# ✓ EXAMPLE 2: Generation modes comparison
# ✓ EXAMPLE 3: Batch processing
# ✓ EXAMPLE 4: Mel-spectrogram enhancement
# ✓ EXAMPLE 5: End-to-end with SDXL
```

---

## 11. Reference Implementation

See corresponding Python files:
- **Feature Extraction**: `music_analyzer.py` → `MusicAnalyzer.analyze_audio()`
- **Prompt Building**: `prompt_builder_paper.py` → `PromptBuilderPaper.build_gpt_prompt()`
- **Pipeline**: `music_to_image_paper_pipeline.py` → `MusicToImagePaperPipeline.process_audio()`
- **Examples**: `example_paper_implementation.py` → 5 complete examples

---

## 12. Citation

```bibtex
@article{yang2024exploring,
  title={Exploring Real-Time Music-to-Image Systems for Creative Inspiration in Music Creation},
  author={Yang, Meng and Llano, Maria Teresa and McCormack, Jon},
  journal={arXiv preprint arXiv:2407.05584},
  year={2024}
}
```

---

**Ready to replicate the paper! 🚀**
