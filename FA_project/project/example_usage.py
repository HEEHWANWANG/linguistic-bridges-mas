"""
Example Usage - Music-to-Image Pipeline

This script demonstrates how to use the complete pipeline with your dataset.

SETUP INSTRUCTIONS:
1. Install dependencies: pip install -r requirements.txt
2. Set up LLM (choose one):

   Option A: Claude API (RECOMMENDED - no OpenAI subscription needed!)
   - Get API key from: https://console.anthropic.com/
   - Set environment: export ANTHROPIC_API_KEY=your_key

   Option B: Local Ollama (Free, runs locally)
   - Install: https://ollama.ai
   - Run: ollama pull mistral && ollama serve
   - Then use OllamaClient in this script

   Option C: Mock client (for testing without API)
   - Just run the script, it will use MockLLMClient

3. Run this script: python example_usage.py
"""

import asyncio
import logging
import os
from pathlib import Path
import numpy as np
import sys

# Add project directory to path
sys.path.insert(0, str(Path(__file__).parent))

from music_to_image_pipeline import MusicToImagePipeline, AudioLoaderFromNPY, print_sample_output
from llm_client import get_recommended_client, create_llm_client
from mel_spectrogram_converter import MelSpectrogramConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def example_single_sample():
    """Example 1: Process a single audio sample"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 1: Process Single Audio Sample")
    logger.info("=" * 70)

    # Path to dataset
    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"

    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found at {dataset_path}")
        logger.info("Please ensure the dataset is at ./FA_project/dataset/label_data_with_16kHz_audio.npy")
        return

    # Load first audio sample
    logger.info("\nLoading audio sample...")
    audio_loader = AudioLoaderFromNPY()
    audio, metadata = audio_loader.load_sample(dataset_path, sample_idx=0)

    logger.info(f"✓ Loaded audio:")
    logger.info(f"   Shape: {audio.shape}")
    logger.info(f"   Duration: {len(audio) / 16000:.2f} seconds")
    logger.info(f"   Artist: {metadata.get('artist_name', 'Unknown')}")
    logger.info(f"   Track: {metadata.get('track_name', 'Unknown')}")

    # Initialize pipeline
    logger.info("\nInitializing pipeline...")
    pipeline = MusicToImagePipeline(
        sample_rate=16000,
        generation_mode="convergent",  # Use convergent for more consistent results
        use_designer_agents=True
    )

    # Get LLM client (auto-detects available option)
    logger.info("\nInitializing LLM client...")
    try:
        llm_client = get_recommended_client()
        logger.info(f"✓ Using LLM: {llm_client.get_model_name()}")
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        logger.info("Proceeding with mock client for demonstration...")
        llm_client = create_llm_client("mock")

    # Process through pipeline
    logger.info("\nProcessing through pipeline...")
    results = await pipeline.process_audio(
        audio_data=audio,
        metadata=metadata,
        llm_client=llm_client
    )

    # Display results
    print_sample_output(results)

    # Save results to file
    save_results_to_file(results, "example_output_single.json")


async def example_batch_processing():
    """Example 2: Process multiple samples in batch"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 2: Batch Process Multiple Samples")
    logger.info("=" * 70)

    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"

    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found at {dataset_path}")
        return

    # Load multiple samples
    logger.info("\nLoading audio samples...")
    audio_loader = AudioLoaderFromNPY()
    samples = audio_loader.load_batch(dataset_path, indices=[0, 1, 2])  # First 3 samples
    logger.info(f"✓ Loaded {len(samples)} samples")

    # Initialize pipeline
    pipeline = MusicToImagePipeline(
        sample_rate=16000,
        generation_mode="divergent",  # Use divergent for more creative variation
        use_designer_agents=True
    )

    # Get LLM client
    try:
        llm_client = get_recommended_client()
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        llm_client = create_llm_client("mock")

    # Process all samples
    all_results = []
    for idx, (audio, metadata) in enumerate(samples):
        logger.info(f"\n--- Processing sample {idx + 1}/{len(samples)} ---")
        results = await pipeline.process_audio(
            audio_data=audio,
            metadata=metadata,
            llm_client=llm_client
        )
        all_results.append(results)

    # Save batch results
    logger.info(f"\n✓ Processed {len(all_results)} samples")
    save_results_to_file(all_results, "example_output_batch.json")

    # Print summary
    logger.info("\n" + "=" * 70)
    logger.info("BATCH PROCESSING SUMMARY")
    logger.info("=" * 70)
    for idx, results in enumerate(all_results):
        logger.info(f"\nSample {idx + 1}:")
        logger.info(f"   Track: {results['metadata'].get('track_name', 'Unknown')[:50]}")
        logger.info(f"   Key: {results['features']['key']} {results['features']['tonality']}")
        logger.info(f"   Tempo: {results['features']['tempo']:.0f} BPM")
        logger.info(f"   Mood: {results['features']['overall_mood']}")


async def example_compare_generation_modes():
    """Example 3: Compare divergent vs convergent generation modes"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 3: Compare Generation Modes")
    logger.info("=" * 70)

    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"

    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found at {dataset_path}")
        return

    # Load single sample
    audio_loader = AudioLoaderFromNPY()
    audio, metadata = audio_loader.load_sample(dataset_path, sample_idx=0)

    # Get LLM client
    try:
        llm_client = get_recommended_client()
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        llm_client = create_llm_client("mock")

    modes = [
        ("convergent", 0.4),  # Lower temperature = more consistent
        ("divergent", 0.8)     # Higher temperature = more creative variation
    ]

    results_by_mode = {}

    for mode, expected_temp in modes:
        logger.info(f"\n--- Processing in {mode.upper()} mode ---")
        pipeline = MusicToImagePipeline(
            sample_rate=16000,
            generation_mode=mode,
            use_designer_agents=True
        )

        results = await pipeline.process_audio(
            audio_data=audio,
            metadata=metadata,
            llm_client=llm_client
        )

        results_by_mode[mode] = results
        actual_temp = results['visual_analysis'].get('temperature', 'N/A')
        logger.info(f"Expected temp: {expected_temp}, Actual: {actual_temp}")

    # Compare results
    logger.info("\n" + "=" * 70)
    logger.info("MODE COMPARISON")
    logger.info("=" * 70)

    convergent = results_by_mode["convergent"]
    divergent = results_by_mode["divergent"]

    logger.info("\nConvergent mode (Temperature 0.4):")
    logger.info(f"  Visual prompt length: {len(convergent.get('final_image_prompt', ''))}")
    logger.info("  Use case: Consistent, focused, refined visuals")

    logger.info("\nDivergent mode (Temperature 0.8):")
    logger.info(f"  Visual prompt length: {len(divergent.get('final_image_prompt', ''))}")
    logger.info("  Use case: Creative exploration, varied alternatives")

    save_results_to_file(results_by_mode, "example_output_mode_comparison.json")


def save_results_to_file(results, filename):
    """Save results to JSON file"""
    import json
    from pathlib import Path

    output_dir = Path("./example_outputs")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename

    try:
        # Convert non-serializable types
        def json_serializer(obj):
            import numpy as np
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.generic):
                return obj.item()
            else:
                return str(obj)

        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=json_serializer)

        logger.info(f"\n✓ Results saved to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save results: {e}")


async def example_with_mel_spectrogram():
    """Example 4: Process with mel-spectrogram enhancement"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 4: Process with Mel-Spectrogram Enhancement")
    logger.info("=" * 70)

    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"

    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found at {dataset_path}")
        return

    # Load audio sample
    logger.info("\nLoading audio sample...")
    audio_loader = AudioLoaderFromNPY()
    audio, metadata = audio_loader.load_sample(dataset_path, sample_idx=0)

    logger.info(f"✓ Loaded audio:")
    logger.info(f"   Shape: {audio.shape}")
    logger.info(f"   Duration: {len(audio) / 16000:.2f} seconds")

    # Get LLM client
    try:
        llm_client = get_recommended_client()
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        llm_client = create_llm_client("mock")

    # Process WITHOUT mel-spectrogram (baseline)
    logger.info("\n--- Processing WITHOUT mel-spectrogram ---")
    pipeline_without_mel = MusicToImagePipeline(
        sample_rate=16000,
        generation_mode="convergent",
        use_designer_agents=True,
        use_mel_spectrogram=False  # Disabled
    )

    results_without_mel = await pipeline_without_mel.process_audio(
        audio_data=audio,
        metadata=metadata,
        llm_client=llm_client
    )
    logger.info(f"✓ Baseline processing complete")
    logger.info(f"   Mel-spectrogram enabled: {results_without_mel['mel_spectrogram_enabled']}")

    # Process WITH mel-spectrogram (enhanced)
    logger.info("\n--- Processing WITH mel-spectrogram ---")

    # Create custom mel-spectrogram configuration
    mel_config = MelSpectrogramConfig(
        n_mels=128,          # Number of mel frequency bands
        n_fft=2048,          # FFT window size
        hop_length=512,      # Samples between successive frames
        sample_rate=16000
    )

    pipeline_with_mel = MusicToImagePipeline(
        sample_rate=16000,
        generation_mode="convergent",
        use_designer_agents=True,
        use_mel_spectrogram=True,  # Enabled
        mel_spectrogram_config=mel_config
    )

    results_with_mel = await pipeline_with_mel.process_audio(
        audio_data=audio,
        metadata=metadata,
        llm_client=llm_client
    )
    logger.info(f"✓ Mel-spectrogram processing complete")
    logger.info(f"   Mel-spectrogram enabled: {results_with_mel['mel_spectrogram_enabled']}")

    # Compare results
    logger.info("\n" + "=" * 70)
    logger.info("MEL-SPECTROGRAM COMPARISON")
    logger.info("=" * 70)

    logger.info("\nBaseline (Audio waveform only):")
    logger.info(f"  GPT prompt size: {len(results_without_mel['gpt_prompt'])} chars")
    logger.info(f"  Final prompt size: {len(results_without_mel.get('final_image_prompt', ''))} chars")

    logger.info("\nEnhanced (With mel-spectrogram analysis):")
    logger.info(f"  Mel-spectrogram text: {len(results_with_mel.get('mel_spectrogram_text', ''))} chars")
    logger.info(f"  GPT prompt size: {len(results_with_mel['gpt_prompt'])} chars")
    logger.info(f"  Final prompt size: {len(results_with_mel.get('final_image_prompt', ''))} chars")

    logger.info("\nBenefits of mel-spectrogram enhancement:")
    logger.info("  • Perceptually-relevant frequency analysis")
    logger.info("  • Enhanced spectral feature representation")
    logger.info("  • Better LLM understanding of audio characteristics")
    logger.info("  • Improved visual prompt accuracy for audio-visual alignment")

    # Save comparison results
    save_results_to_file({
        "without_mel_spectrogram": results_without_mel,
        "with_mel_spectrogram": results_with_mel
    }, "example_output_mel_spectrogram_comparison.json")


async def main():
    """Main entry point"""
    logger.info("\n")
    logger.info("╔" + "=" * 68 + "╗")
    logger.info("║" + " " * 15 + "Music-to-Image Pipeline Examples" + " " * 21 + "║")
    logger.info("╚" + "=" * 68 + "╝")

    # Check dependencies
    logger.info("\nChecking dependencies...")
    try:
        import librosa
        import numpy as np
        logger.info("✓ librosa and numpy are installed")
    except ImportError as e:
        logger.error(f"Missing dependencies: {e}")
        logger.info("Run: pip install -r requirements.txt")
        return

    # Run examples
    try:
        # Example 1: Single sample
        await example_single_sample()

        # Example 2: Batch processing
        await example_batch_processing()

        # Example 3: Mode comparison
        await example_compare_generation_modes()

        # Example 4: Mel-spectrogram enhancement
        await example_with_mel_spectrogram()

        logger.info("\n" + "=" * 70)
        logger.info("✅ All examples completed successfully!")
        logger.info("=" * 70)
        logger.info("\nOutput files saved to ./example_outputs/")
        logger.info("\nNext steps:")
        logger.info("1. Check the generated prompts in the output files")
        logger.info("2. Use the 'final_image_prompt' with your image generation model")
        logger.info("3. Experiment with different generation modes and designer agents")
        logger.info("4. Try mel-spectrogram enhancement for improved audio analysis")

    except KeyboardInterrupt:
        logger.info("\n⚠ Interrupted by user")
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
