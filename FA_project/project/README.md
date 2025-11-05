# Music-to-Image System: Real-Time Visuals for Music

**Based on**: "Exploring Real-Time Music-to-Image Systems for Creative Inspiration" (Yang et al., arXiv:2407.05584v1)

**Framework**: Adapted from the paper's approach with multi-agent design principles

This system analyzes music audio and generates detailed visual prompts that can be used to create accompanying images.

## 🎯 Key Features

- **Music Feature Analysis**: Extracts key signature, tempo, mood, melody contour, and more
- **ABC Notation Generation**: Converts musical features to text-based music notation for LLM processing
- **Mel-Spectrogram Enhancement**: Optional mel-spectrogram analysis for improved spectral understanding
- **Multi-LLM Support**: Works with Claude, local models (Ollama), or mock client for testing
- **Designer Agent Roles**: Five specialized perspectives (Narrative, Mood, Style, Conceptual, Commercial)
- **Stable Diffusion XL Integration**: High-quality image generation with optional refiner model
- **Complete End-to-End Pipeline**: From audio → prompts → images
- **Generation Modes**:
  - **Convergent** (Temperature 0.4): Consistent, focused results
  - **Divergent** (Temperature 0.8): Creative exploration and variation

## 📋 System Architecture

```
┌─────────────────┐
│  Audio Input    │ (16 kHz WAV or array)
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│  1. Music Analyzer       │ ─→ Extract features
│     (librosa)            │    (key, tempo, mood, etc)
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  2. ABC Notation Gen     │ ─→ Create text representation
│     (MusicalFeatures)    │    of music for LLM
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  3. Prompt Builder       │ ─→ Generate GPT analysis prompt
│     (PromptBuilder)      │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  4. LLM Analysis         │ ─→ Claude/Local Model
│     (Claude/Ollama)      │    analyzes music features
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  5. Designer Agents      │ ─→ 5 specialized perspectives
│     (5 roles)            │    on visual direction
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  6. Final Image Prompt   │ ─→ Blended consensus prompt
│     (Consensus Builder)  │    ready for image generation
└──────────────────────────┘
```

## 🎨 Image Generation with Stable Diffusion XL

### Overview

The system integrates **Stable Diffusion XL** from Hugging Face for high-quality image generation:

- **Base Model**: `stabilityai/stable-diffusion-xl-base-1.0`
- **Refiner Model**: `stabilityai/stable-diffusion-xl-refiner-1.0` (optional)
- **Resolution**: 1024×1024 (configurable)
- **Quality Settings**: Adjustable guidance scale and inference steps

### Quick Example

```python
from image_generator import create_image_generator

# Create generator
generator = create_image_generator(
    device="auto",      # Auto-detect GPU/CPU
    use_refiner=True,   # Use refiner for quality
    height=1024,
    width=1024,
    num_steps=30
)

# Generate image
prompt = "A vibrant sunset over mountains, oil painting style"
images, metadata = generator.generate(
    prompt=prompt,
    seed=42,           # Reproducible results
    num_images=1
)

# Save image
if images:
    images[0].save("output.png")
```

### End-to-End Pipeline

For complete audio-to-image generation:

```python
from music_to_image_complete_pipeline import CompleteMusicToImagePipeline
import asyncio

async def main():
    # Create complete pipeline
    pipeline = CompleteMusicToImagePipeline(
        sample_rate=16000,
        generation_mode="convergent",
        use_designer_agents=True,
        use_mel_spectrogram=False,
        image_generation_enabled=True,
        image_output_dir="./generated_images"
    )

    # Load audio
    from music_to_image_pipeline import AudioLoaderFromNPY
    loader = AudioLoaderFromNPY()
    audio, metadata = loader.load_sample(
        "./FA_project/dataset/label_data_with_16kHz_audio.npy",
        sample_idx=0
    )

    # Process audio to images
    results = await pipeline.process_audio_to_images(
        audio_data=audio,
        metadata=metadata,
        save_images=True
    )

    # Cleanup
    pipeline.cleanup()

# Run
asyncio.run(main())
```

### Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `height` | 1024 | Image height (multiple of 8) |
| `width` | 1024 | Image width (multiple of 8) |
| `num_inference_steps` | 30 | Denoising steps (more = quality but slower) |
| `guidance_scale` | 7.5 | How much to follow prompt (higher = more faithful) |
| `use_refiner` | True | Use refiner model for polishing |
| `num_images_per_prompt` | 1 | Number of images to generate |
| `device` | "auto" | "cuda", "cpu", or "auto" |

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to project directory
cd FA_project/project

# Install dependencies
pip install -r requirements.txt

# For GPU support (CUDA), install PyTorch separately:
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. Set Up LLM (Choose One)

#### Option A: Claude API ⭐ RECOMMENDED
You don't need OpenAI subscription - Claude works great for this!

```bash
# Get API key from https://console.anthropic.com/
export ANTHROPIC_API_KEY=sk-ant-...

# Verify it works
python -c "from llm_client import get_recommended_client; print(get_recommended_client().get_model_name())"
```

#### Option B: Local Ollama (Free, runs locally)

```bash
# Install Ollama from https://ollama.ai
# Pull a model
ollama pull mistral  # or: llama2, neural-chat, etc.

# Start Ollama server
ollama serve

# In another terminal, run the example
python example_usage.py
```

#### Option C: Mock Client (Testing only)
```python
# No setup needed - just run example_usage.py
# It will automatically fall back to MockLLMClient
```

### 3. Run the Examples

```bash
python example_usage.py
```

This runs three examples:
1. **Single Sample**: Process one audio track
2. **Batch Processing**: Process multiple tracks
3. **Mode Comparison**: Compare convergent vs divergent modes

## 🎼 Understanding Mel-Spectrograms

### What is a Mel-Spectrogram?

A **mel-spectrogram** is a time-frequency representation of audio that mimics how humans perceive sound:

- **Frequency Domain**: Divides audio into perceptually-relevant frequency bands (mel-scale frequencies)
- **Time Domain**: Captures how these frequencies change over time
- **Human Perception**: Uses logarithmic frequency spacing, matching human auditory system

### Why Use Mel-Spectrograms?

When processing audio with LLMs, mel-spectrograms provide:

1. **Perceptual Relevance**: Frequencies are spaced according to how humans actually hear
2. **Compression**: Reduces high-dimensional audio data to manageable size
3. **Feature Extraction**: Highlights musically-relevant information (pitch, timbre, dynamics)
4. **LLM Understanding**: Text-based representation that LLMs can easily process

### Mel-Spectrogram Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_mels` | 128 | Number of mel frequency bins (higher = more detail) |
| `n_fft` | 2048 | FFT window size (affects frequency resolution) |
| `hop_length` | 512 | Samples between frames (affects time resolution) |
| `window` | "hann" | Window function (reduces spectral leakage) |
| `power` | 2.0 | Power of magnitude spectrum |
| `log_scale` | True | Convert to dB scale for better dynamic range |

### Text Representation

The system converts mel-spectrograms to text for LLM analysis, including:

- **Spectral statistics**: Mean/peak energy, frequency stability
- **Frequency band analysis**: Energy distribution across frequency ranges
- **Temporal characteristics**: How energy changes over time
- **Visual patterns**: ASCII art representations of the spectrogram

Example output:
```
MEL-SPECTROGRAM ANALYSIS:
- Shape: 128 mel bands × 312 time frames
- Duration: 10.00 seconds
- Time Resolution: 0.0320 seconds/frame

SPECTRAL FEATURES:
- Peak Energy: -5.23 dB
- Mean Energy: -25.45 dB
- Frequency Stability: 0.87 (stable)
- Energy Continuity: 0.92 (smooth)

FREQUENCY BAND ANALYSIS:
- Low (0-500 Hz): 15.3%
- Mid-Low (500-2K Hz): 28.4%
- Mid (2K-8K Hz): 42.1%
- High (8K+ Hz): 14.2%
```

## 📖 Usage Guide

### Basic Usage

```python
import asyncio
from music_to_image_pipeline import MusicToImagePipeline, AudioLoaderFromNPY
from llm_client import get_recommended_client

async def main():
    # Load audio from your dataset
    loader = AudioLoaderFromNPY()
    audio, metadata = loader.load_sample("./FA_project/dataset/label_data_with_16kHz_audio.npy", sample_idx=0)

    # Create pipeline
    pipeline = MusicToImagePipeline(
        sample_rate=16000,
        generation_mode="convergent",  # or "divergent"
        use_designer_agents=True
    )

    # Get LLM client
    llm_client = get_recommended_client()

    # Process audio
    results = await pipeline.process_audio(audio, metadata, llm_client)

    # Get final image prompt
    image_prompt = results["final_image_prompt"]
    print(image_prompt)

asyncio.run(main())
```

### Processing Your Own Audio

```python
import numpy as np

# Load your audio file
audio = np.load("your_audio.npy")  # or use librosa.load()

# Process through pipeline
results = await pipeline.process_audio(audio, llm_client=llm_client)
```

### Enabling Mel-Spectrogram Analysis

```python
from mel_spectrogram_converter import MelSpectrogramConfig

# Create pipeline with mel-spectrogram enabled
pipeline = MusicToImagePipeline(
    sample_rate=16000,
    generation_mode="convergent",
    use_mel_spectrogram=True,  # Enable mel-spectrogram
    mel_spectrogram_config=MelSpectrogramConfig(
        n_mels=128,      # Frequency bins
        n_fft=2048,      # Window size
        hop_length=512,  # Frame shift
        sample_rate=16000
    )
)

# Process audio with mel-spectrogram enhancement
results = await pipeline.process_audio(audio, llm_client=llm_client)

# Access mel-spectrogram analysis
if results["mel_spectrogram_enabled"]:
    mel_text = results["mel_spectrogram_text"]
    print("Mel-spectrogram analysis included in LLM prompt")
```

### Accessing Different Outputs

```python
# Musical features extracted
features = results["features"]
print(f"Key: {features['key']}, Tempo: {features['tempo']} BPM")

# ABC notation representation
abc = results["abc_notation"]

# Visual analysis from LLM
visual = results["visual_analysis"]
print(f"Color palette: {visual['color_palette']}")

# Individual designer perspectives
designers = results["designer_variations"]
print(f"Narrative: {designers['narrative']}")
print(f"Mood: {designers['mood']}")
print(f"Style: {designers['style']}")

# Final blended prompt ready for image generation
final_prompt = results["final_image_prompt"]
```

## 🎨 How It Works: Step by Step

### Step 1: Music Analysis
The system uses `librosa` to extract:
- **Key Signature**: Chroma feature analysis
- **Tonality**: Major vs minor (based on spectral features)
- **Tempo**: BPM from onset detection
- **Melody Contour**: Ascending/descending based on spectral centroid
- **Harmonic Progression**: Complexity from MFCC variance
- **Dynamic Intensity**: Loudness and variation from RMS

### Step 2: ABC Notation Generation
Features are converted to ABC notation (text-based music format):
```
X:1
T:Generated Song
M:4/4
L:1/8
Q:120
K:C
C2 D2 E2 F2 G2 |
```

This allows LLMs to understand and analyze the music.

### Step 3: GPT Analysis
A comprehensive prompt is sent to Claude/LLM:
- Includes ABC notation
- Includes extracted features
- Asks for visual mapping (e.g., "fast tempo = dynamic visuals")

### Step 4: Designer Agent Perspectives
Five specialized agents provide different viewpoints:

| Role | Focus | Example Output |
|------|-------|-----------------|
| **Narrative** | Story arc, emotional journey | "A figure ascending toward light" |
| **Mood** | Colors, emotional tone, atmosphere | "Cool blues with warm highlights" |
| **Style** | Artistic direction, visual language | "Impressionistic oil painting style" |
| **Conceptual** | Abstract meaning, symbolism | "Spiral pattern representing growth" |
| **Commercial** | Audience appeal, marketability | "Vibrant, eye-catching composition" |

### Step 5: Consensus Building (70/30 Ratio)
- **70% Consensus**: Blend all agent perspectives into coherent direction
- **30% Creative Alternatives**: Preserve some minority viewpoints for novelty

### Step 6: Final Image Prompt
A unified prompt is created for image generation:
```
A vibrant, energetic scene with flowing abstract forms in warm amber and golden yellow tones,
capturing the ascending melodic contour of the music...
[color palette details]
[compositional guidance]
[mood and atmosphere]
```

## ⚙️ Configuration

### Generation Modes

```python
# Convergent mode: Consistent, focused results
pipeline = MusicToImagePipeline(generation_mode="convergent")
# Temperature: 0.4 (lower = more consistent)

# Divergent mode: Creative exploration
pipeline = MusicToImagePipeline(generation_mode="divergent")
# Temperature: 0.8 (higher = more varied)
```

### Designer Agents On/Off

```python
# With all 5 designer perspectives
pipeline = MusicToImagePipeline(use_designer_agents=True)

# Just use primary LLM analysis
pipeline = MusicToImagePipeline(use_designer_agents=False)
```

### LLM Selection

```python
# Auto-detect available LLM
from llm_client import get_recommended_client
client = get_recommended_client()

# Explicitly use Claude
from llm_client import create_llm_client
client = create_llm_client("claude", model="claude-3-opus-20250219")

# Use local Ollama
client = create_llm_client("ollama", model="mistral")

# Use mock for testing
client = create_llm_client("mock")
```

## 📊 Understanding the Output

The pipeline returns a comprehensive results dictionary:

```python
{
    "metadata": {...},           # Input metadata
    "features": {
        "key": "C",
        "tonality": "major",
        "tempo": 120.0,
        "time_signature": "4/4",
        "melody_contour": "ascending",
        "harmonic_progression": "complex_progression",
        "dynamic_intensity": "intense",
        "overall_mood": "energetic, bright, dramatic"
    },
    "abc_notation": "X:1\nT:...",  # Text music representation
    "gpt_prompt": "...",           # The prompt sent to Claude
    "visual_analysis": {
        "visual_prompt": "A vibrant, energetic scene...",
        "color_palette": ["golden amber", "warm yellow"],
        "composition": "ascending compositional flow",
        "mood": "uplifting, energetic",
        "temperature": 0.4
    },
    "designer_variations": {
        "narrative": "A figure ascending toward light...",
        "mood": "Cool blues with warm highlights...",
        "style": "Impressionistic oil painting...",
        "conceptual": "Spiral pattern representing growth...",
        "commercial": "Vibrant, eye-catching composition..."
    },
    "final_image_prompt": "PRIMARY VISUAL DIRECTION:\nA vibrant, energetic scene...\n[complete blended prompt]"
}
```

## 🔧 Troubleshooting

### Issue: "ANTHROPIC_API_KEY not found"
**Solution**: Set your API key
```bash
export ANTHROPIC_API_KEY=your_key_here
```

### Issue: Ollama connection refused
**Solution**: Make sure Ollama is running
```bash
ollama serve  # In a separate terminal
```

### Issue: "librosa not installed"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Audio file too short/long
**Solution**: The system handles variable-length audio. If you have issues:
```python
# Trim or pad audio
if len(audio) < 16000:  # Less than 1 second
    audio = np.pad(audio, (0, 16000 - len(audio)))
elif len(audio) > 160000:  # More than 10 seconds
    audio = audio[:160000]
```

## 📚 Module Reference

### `music_analyzer.py`
- `MusicAnalyzer`: Extracts musical features using librosa
- `MusicalFeatures`: Data class for holding features
- Methods for extracting: key, tonality, tempo, melody, harmony, dynamics

### `prompt_builder.py`
- `PromptBuilder`: Builds visual prompts from music features
- Supports 5 designer roles: narrative, mood, style, conceptual, commercial
- Handles consensus/dissent blending
- Optional mel-spectrogram inclusion in prompts

### `music_to_image_pipeline.py`
- `MusicToImagePipeline`: Main orchestrator with optional mel-spectrogram support
- `AudioLoaderFromNPY`: Helper for loading from .npy files
- `print_sample_output`: Pretty-printing results
- **Parameters**: `use_mel_spectrogram`, `mel_spectrogram_config`

### `mel_spectrogram_converter.py` *(NEW)*
- `MelSpectrogramConverter`: Converts audio waveforms to mel-spectrograms
- `MelSpectrogramConfig`: Configuration dataclass for parameters
- Key methods:
  - `audio_to_mel_spectrogram()`: Convert waveform to mel-spectrogram
  - `mel_spectrogram_to_text_representation()`: Generate text for LLM
  - `detect_input_type()`: Identify waveform vs mel-spectrogram
  - `ensure_mel_spectrogram()`: Convert if needed
  - `ensure_audio_waveform()`: Validate waveform format

### `llm_client.py`
- `ClaudeClient`: Anthropic Claude API
- `OllamaClient`: Local model via Ollama
- `MockLLMClient`: Testing without API
- `create_llm_client()`: Factory function

### `image_generator.py` *(NEW)*
- `StableDiffusionXLGenerator`: Main image generation class
- `ImageGenerationConfig`: Configuration dataclass
- Key methods:
  - `generate()`: Generate images from text prompt
  - `generate_batch()`: Generate images for multiple prompts
  - `free_memory()`: Clean up GPU memory
- `create_image_generator()`: Factory function for easy initialization

### `music_to_image_complete_pipeline.py` *(NEW)*
- `CompleteMusicToImagePipeline`: End-to-end orchestrator
- Combines music analysis + LLM prompt generation + image creation
- Key methods:
  - `process_audio_to_images()`: Single audio to images
  - `process_batch()`: Multiple audios to images
  - `cleanup()`: Resource cleanup

## 🎬 Paper Comparison

### Original Paper (Yang et al.)
- Input: MIDI keyboard input
- Analysis: GPT-4 emotion inference from ABC notation
- Generation: SDXL Turbo (real-time)
- Modes: Divergent (0.8) vs Convergent (0.4)

### This Implementation
- Input: Audio files (any 16kHz PCM)
- Analysis: Librosa feature extraction + LLM analysis
- Generation: Multi-agent debate with 5 designer roles
- Modes: Same convergent/divergent approach
- **Addition**: 70/30 consensus/dissent for novelty preservation

## 📝 Citation

Original paper:
```
@article{yang2024exploring,
  title={Exploring Real-Time Music-to-Image Systems for Creative Inspiration in Music Creation},
  author={Yang, Meng and Llano, Maria Teresa and McCormack, Jon},
  journal={arXiv preprint arXiv:2407.05584},
  year={2024}
}
```

## 🤝 Contributing

Improvements welcome! Some ideas:
- Add MIDI file support
- Implement actual image generation integration (DALL-E 3, Flux)
- Add more designer agent roles
- Improve feature extraction accuracy
- Add real-time streaming support

## 📄 License

This implementation is provided as research code. Please cite the original paper if you use it.

## 🙋 Support

For questions or issues:
1. Check the Troubleshooting section above
2. Review the example scripts in `example_usage.py`
3. Check that all dependencies are installed: `pip install -r requirements.txt`
4. Verify LLM setup is correct for your chosen provider

---

**Ready to create stunning music-to-image combinations?** 🎨🎵

Start with: `python example_usage.py`
