"""
Example: Batch Visual Prompt Generation

Demonstrates how to:
1. Generate 5 prompts for all 100 audio samples
2. Use different generation modes (convergent/divergent)
3. Save results for downstream processing
4. Access generated prompts for image generation
"""

import asyncio
import json
from pathlib import Path
from generate_visual_prompts_batch import BatchPromptGenerator


async def example_full_batch():
    """Example 1: Generate prompts for all 100 samples."""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Full Batch Generation (All 100 Samples)")
    print("=" * 60)

    generator = BatchPromptGenerator(
        dataset_path="dataset/label_data_with_16kHz_audio.npy",
        output_dir="generated_prompts",
        use_mel_spectrogram=False,
        batch_size=5  # 3 convergent + 2 divergent
    )

    print("Starting batch generation...")
    print("  - 100 audio samples")
    print("  - 5 prompts per sample = 500 total prompts")
    print("  - 3 convergent (T=0.4) + 2 divergent (T=0.8)")
    print("")

    # Generate all prompts
    results = await generator.generate_all_prompts()

    # Save all outputs
    generator.save_results()
    generator.save_summary_stats()
    generator.export_for_image_generation()
    generator.print_summary()

    return results


async def example_partial_batch():
    """Example 2: Generate prompts for subset of samples."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Partial Batch (First 10 Samples)")
    print("=" * 60)

    generator = BatchPromptGenerator(
        dataset_path="dataset/label_data_with_16kHz_audio.npy",
        output_dir="generated_prompts_sample",
        use_mel_spectrogram=False,
        batch_size=5
    )

    print("Generating prompts for first 10 samples only...")
    print("  - 10 audio samples")
    print("  - 5 prompts per sample = 50 total prompts")
    print("")

    # Generate only first 10 samples
    sample_indices = list(range(10))
    results = await generator.generate_all_prompts(sample_indices)

    generator.save_results()
    generator.print_summary()

    return results


async def example_with_mel_spectrogram():
    """Example 3: Generate prompts with mel-spectrogram enhancement."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Batch with Mel-Spectrogram Enhancement")
    print("=" * 60)

    generator = BatchPromptGenerator(
        dataset_path="dataset/label_data_with_16kHz_audio.npy",
        output_dir="generated_prompts_mel",
        use_mel_spectrogram=True,  # Enable enhancement
        batch_size=5
    )

    print("Generating prompts WITH mel-spectrogram enhancement...")
    print("  - Provides additional spectral context to LLM")
    print("  - May generate richer visual prompts")
    print("")

    sample_indices = list(range(20))  # First 20 samples
    results = await generator.generate_all_prompts(sample_indices)

    generator.save_results()
    generator.print_summary()

    return results


def example_load_and_inspect():
    """Example 4: Load and inspect generated prompts."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Loading and Inspecting Generated Prompts")
    print("=" * 60)

    prompts_file = Path("generated_prompts/visual_prompts_complete.json")

    if not prompts_file.exists():
        print(f"File not found: {prompts_file}")
        print("Run one of the generation examples first!")
        return

    print(f"Loading {prompts_file}...")
    with open(prompts_file, 'r') as f:
        data = json.load(f)

    # Print metadata
    print("\nMetadata:")
    for key, value in data["metadata"].items():
        print(f"  {key}: {value}")

    # Print sample statistics
    print(f"\nSample Statistics:")
    print(f"  Total samples: {len(data['samples'])}")

    if len(data["samples"]) > 0:
        first_sample = data["samples"][0]
        print(f"\nFirst Sample (index {first_sample['sample_idx']}):")
        print(f"  Musical Features:")
        for feat, val in first_sample.get("musical_features", {}).items():
            print(f"    {feat}: {val}")
        print(f"\n  Generated Prompts ({len(first_sample['prompts'])} total):")
        for i, prompt_data in enumerate(first_sample["prompts"]):
            print(f"\n    Prompt {i + 1}:")
            print(f"      Mode: {prompt_data['mode']}")
            print(f"      Temperature: {prompt_data['temperature']}")
            print(f"      Text: {prompt_data['visual_prompt'][:100]}...")


def example_access_image_generation_format():
    """Example 5: Access prompts in image generation format."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Accessing Prompts for Image Generation")
    print("=" * 60)

    image_gen_file = Path("generated_prompts/prompts_for_image_generation.json")

    if not image_gen_file.exists():
        print(f"File not found: {image_gen_file}")
        print("Run one of the generation examples first!")
        return

    print(f"Loading {image_gen_file}...")
    with open(image_gen_file, 'r') as f:
        prompts = json.load(f)

    print(f"Total prompts ready for image generation: {len(prompts)}")
    print("\nFormat for image generation pipeline:")
    if len(prompts) > 0:
        example = prompts[0]
        print(f"  - sample_idx: {example['sample_idx']}")
        print(f"  - prompt_id: {example['prompt_id']}")
        print(f"  - mode: {example['mode']}")
        print(f"  - temperature: {example['temperature']}")
        print(f"  - visual_prompt: {example['visual_prompt'][:80]}...")
        print(f"  - features: {list(example['features'].keys())}")
        print(f"  - abc_notation: {example['abc_notation'][:50]}...")

    print("\nUsage in image generation pipeline:")
    print("""
    from image_generator import create_image_generator
    import json

    # Load prompts
    with open('generated_prompts/prompts_for_image_generation.json') as f:
        prompts = json.load(f)

    # Generate images
    generator = create_image_generator(device='cuda')
    for prompt_data in prompts:
        images = generator.generate(
            prompt=prompt_data['visual_prompt'],
            num_images=1
        )
    """)


async def main():
    """Run all examples."""
    import sys

    if len(sys.argv) > 1:
        example = sys.argv[1]
    else:
        example = "all"

    if example == "1" or example == "all":
        await example_full_batch()

    if example == "2" or example == "all":
        await example_partial_batch()

    if example == "3" or example == "all":
        await example_with_mel_spectrogram()

    if example == "4" or example == "all":
        example_load_and_inspect()

    if example == "5" or example == "all":
        example_access_image_generation_format()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
