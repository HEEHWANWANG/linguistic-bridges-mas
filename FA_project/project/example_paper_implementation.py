"""
Example Usage - Paper Implementation

Demonstrates the exact framework from "Exploring Real-Time Music-to-Image Systems"
(Yang et al., 2407.05584v1) without multi-agent extensions.

Simple pipeline: Audio → Features → ABC Notation → LLM → Visual Prompt → SDXL
"""

import asyncio
import logging
import os
from pathlib import Path

from music_to_image_paper_pipeline import MusicToImagePaperPipeline, AudioLoaderFromNPY
from llm_client import get_recommended_client, create_llm_client
from image_generator import create_image_generator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def example_paper_basic():
    """Example 1: Basic paper implementation - Audio to visual prompt"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 1: Paper Implementation - Audio to Visual Prompt")
    logger.info("=" * 70)

    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"

    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found at {dataset_path}")
        return

    # Load audio
    logger.info("\nLoading audio sample...")
    audio_loader = AudioLoaderFromNPY()
    audio, metadata = audio_loader.load_sample(dataset_path, sample_idx=0)

    logger.info(f"✓ Loaded audio:")
    logger.info(f"   Duration: {len(audio) / 16000:.2f} seconds")
    logger.info(f"   Track: {metadata.get('track_name', 'Unknown')}")

    # Create pipeline
    logger.info("\nInitializing pipeline...")
    pipeline = MusicToImagePaperPipeline(
        sample_rate=16000,
        generation_mode="convergent",  # Paper uses convergent (0.4 temp)
        use_mel_spectrogram=False
    )

    # Get LLM client
    logger.info("\nInitializing LLM client...")
    try:
        llm_client = get_recommended_client()
        logger.info(f"✓ Using: {llm_client.get_model_name()}")
    except Exception as e:
        logger.warning(f"LLM initialization failed: {e}")
        logger.info("Using mock client for demonstration...")
        llm_client = create_llm_client("mock")

    # Process
    logger.info("\nProcessing audio through pipeline...")
    results = await pipeline.process_audio(
        audio_data=audio,
        metadata=metadata,
        llm_client=llm_client
    )

    # Display results
    logger.info("\n" + "=" * 70)
    logger.info("📊 ANALYSIS RESULTS")
    logger.info("=" * 70)

    logger.info("\n🎵 Musical Features:")
    for key, value in results["features"].items():
        logger.info(f"   {key.title()}: {value}")

    logger.info(f"\n🎼 ABC Notation (first 200 chars):")
    abc = results["abc_notation"]
    logger.info(abc[:200] + "..." if len(abc) > 200 else abc)

    logger.info(f"\n🎨 Visual Prompt for Image Generation:")
    logger.info("=" * 70)
    logger.info(results["visual_prompt"])
    logger.info("=" * 70)

    logger.info(f"\n📋 Parameters:")
    logger.info(f"   Temperature: {results['temperature']}")
    logger.info(f"   Mode: {results['generation_mode']}")

    return results


async def example_generation_modes():
    """Example 2: Compare convergent vs divergent modes (paper's two modes)"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 2: Compare Generation Modes")
    logger.info("=" * 70)

    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"

    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found at {dataset_path}")
        return

    # Load audio
    audio_loader = AudioLoaderFromNPY()
    audio, metadata = audio_loader.load_sample(dataset_path, sample_idx=0)

    # Get LLM client
    try:
        llm_client = get_recommended_client()
    except:
        llm_client = create_llm_client("mock")

    modes = [
        ("convergent", 0.4),
        ("divergent", 0.8)
    ]

    results_by_mode = {}

    for mode, expected_temp in modes:
        logger.info(f"\n--- Mode: {mode.upper()} (Temperature {expected_temp}) ---")

        pipeline = MusicToImagePaperPipeline(
            sample_rate=16000,
            generation_mode=mode,
            use_mel_spectrogram=False
        )

        results = await pipeline.process_audio(
            audio_data=audio,
            metadata=metadata,
            llm_client=llm_client
        )

        results_by_mode[mode] = results

        logger.info(f"✓ Generated visual prompt ({len(results['visual_prompt'])} chars)")
        logger.info(f"  Prompt preview: {results['visual_prompt'][:100]}...")

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("MODE COMPARISON SUMMARY")
    logger.info("=" * 70)

    convergent = results_by_mode["convergent"]
    divergent = results_by_mode["divergent"]

    logger.info("\nCONVERGENT (T=0.4):")
    logger.info("  Use case: Consistent, reproducible visual generation")
    logger.info(f"  Prompt length: {len(convergent['visual_prompt'])} chars")

    logger.info("\nDIVERGENT (T=0.8):")
    logger.info("  Use case: Creative variation, exploring alternatives")
    logger.info(f"  Prompt length: {len(divergent['visual_prompt'])} chars")

    return results_by_mode


async def example_batch_processing():
    """Example 3: Batch process multiple samples"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 3: Batch Processing")
    logger.info("=" * 70)

    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"

    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found")
        return

    # Load multiple samples
    logger.info("\nLoading audio samples...")
    audio_loader = AudioLoaderFromNPY()
    samples = audio_loader.load_batch(dataset_path, indices=[0, 1, 2])
    logger.info(f"✓ Loaded {len(samples)} samples")

    # Create pipeline
    pipeline = MusicToImagePaperPipeline(
        sample_rate=16000,
        generation_mode="convergent",
        use_mel_spectrogram=False
    )

    # Get LLM client
    try:
        llm_client = get_recommended_client()
    except:
        llm_client = create_llm_client("mock")

    # Process all
    logger.info("\nProcessing samples...")
    all_results = []

    for idx, (audio, metadata) in enumerate(samples):
        logger.info(f"\n[{idx + 1}/{len(samples)}] Processing...")

        try:
            results = await pipeline.process_audio(
                audio_data=audio,
                metadata=metadata,
                llm_client=llm_client
            )
            all_results.append(results)

            logger.info(f"  ✓ Mood: {results['features']['overall_mood']}")

        except Exception as e:
            logger.error(f"  ✗ Failed: {e}")

    logger.info("\n" + "=" * 70)
    logger.info(f"✓ Processed {len(all_results)} samples successfully")
    logger.info("=" * 70)

    return all_results


async def example_with_mel_spectrogram():
    """Example 4: Using mel-spectrogram enhancement"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 4: Mel-Spectrogram Enhancement")
    logger.info("=" * 70)

    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"

    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found")
        return

    # Load audio
    audio_loader = AudioLoaderFromNPY()
    audio, metadata = audio_loader.load_sample(dataset_path, sample_idx=0)

    # Get LLM client
    try:
        llm_client = get_recommended_client()
    except:
        llm_client = create_llm_client("mock")

    # Without mel-spectrogram
    logger.info("\n--- Without Mel-Spectrogram ---")
    pipeline_basic = MusicToImagePaperPipeline(
        sample_rate=16000,
        generation_mode="convergent",
        use_mel_spectrogram=False
    )

    results_basic = await pipeline_basic.process_audio(
        audio_data=audio,
        metadata=metadata,
        llm_client=llm_client
    )

    logger.info(f"Prompt length: {len(results_basic['visual_prompt'])} chars")

    # With mel-spectrogram
    logger.info("\n--- With Mel-Spectrogram ---")
    pipeline_mel = MusicToImagePaperPipeline(
        sample_rate=16000,
        generation_mode="convergent",
        use_mel_spectrogram=True
    )

    results_mel = await pipeline_mel.process_audio(
        audio_data=audio,
        metadata=metadata,
        llm_client=llm_client
    )

    logger.info(f"Prompt length: {len(results_mel['visual_prompt'])} chars")

    logger.info("\n✓ Mel-spectrogram provides additional spectral analysis for LLM")

    return results_basic, results_mel


async def example_image_generation():
    """Example 5: End-to-end with SDXL image generation"""
    logger.info("\n" + "=" * 70)
    logger.info("EXAMPLE 5: Complete End-to-End with Image Generation")
    logger.info("=" * 70)

    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"

    if not os.path.exists(dataset_path):
        logger.error(f"Dataset not found")
        return

    # Load audio
    logger.info("\nLoading audio...")
    audio_loader = AudioLoaderFromNPY()
    audio, metadata = audio_loader.load_sample(dataset_path, sample_idx=0)

    # Create pipeline
    logger.info("Creating music-to-image pipeline...")
    pipeline = MusicToImagePaperPipeline(
        sample_rate=16000,
        generation_mode="convergent",
        use_mel_spectrogram=False
    )

    # Get LLM client
    try:
        llm_client = get_recommended_client()
    except:
        llm_client = create_llm_client("mock")

    # Generate visual prompt
    logger.info("Generating visual prompt...")
    prompt_results = await pipeline.process_audio(
        audio_data=audio,
        metadata=metadata,
        llm_client=llm_client
    )

    visual_prompt = prompt_results["visual_prompt"]
    logger.info(f"✓ Visual prompt ready ({len(visual_prompt)} chars)")

    # Generate image
    logger.info("\nInitializing image generator...")
    try:
        image_generator = create_image_generator(
            device="auto",
            use_refiner=True,
            height=1024,
            width=1024,
            num_steps=30
        )

        logger.info("Generating image from prompt...")
        images, gen_metadata = image_generator.generate(
            prompt=visual_prompt,
            num_images=1,
            seed=42
        )

        # Save image
        if images:
            output_path = Path("./generated_images_paper")
            output_path.mkdir(exist_ok=True)

            mood = prompt_results["features"]["overall_mood"]
            filename = f"music_to_image_{mood}_paper.png"
            filepath = output_path / filename

            images[0].save(filepath)
            logger.info(f"\n✓ Image saved to {filepath}")

        # Cleanup
        image_generator.free_memory()

    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        logger.info("Note: Ensure you have CUDA/GPU available for image generation")
        logger.info("Or install CPU-friendly versions of diffusers")

    return prompt_results


async def main():
    """Run all examples"""
    logger.info("\n")
    logger.info("╔" + "=" * 68 + "╗")
    logger.info("║" + " " * 12 + "Music-to-Image Paper Implementation" + " " * 22 + "║")
    logger.info("║" + " " * 10 + "Framework from Yang et al. (2407.05584v1)" + " " * 16 + "║")
    logger.info("╚" + "=" * 68 + "╝")

    # Check dependencies
    logger.info("\nChecking dependencies...")
    try:
        import librosa
        import numpy as np
        logger.info("✓ librosa and numpy installed")
    except ImportError as e:
        logger.error(f"Missing dependencies: {e}")
        return

    try:
        # Run examples
        await example_paper_basic()
        await example_generation_modes()
        await example_batch_processing()
        await example_with_mel_spectrogram()
        await example_image_generation()

        logger.info("\n" + "=" * 70)
        logger.info("✅ All examples completed!")
        logger.info("=" * 70)
        logger.info("\nNext steps:")
        logger.info("1. Fine-tune temperature and guidance scales for your use case")
        logger.info("2. Adjust image generation parameters (steps, guidance_scale)")
        logger.info("3. Batch process your full dataset")
        logger.info("4. Compare results with original paper")

    except KeyboardInterrupt:
        logger.info("\n⚠ Interrupted by user")
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
