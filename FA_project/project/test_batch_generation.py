"""
Test script to verify batch generation setup.

Run this to check if all components are properly installed and working.
"""

import asyncio
import json
import sys
from pathlib import Path


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import numpy as np
        print("  ✓ numpy")
        import librosa
        print("  ✓ librosa")
        from music_to_image_paper_pipeline import MusicToImagePaperPipeline
        print("  ✓ MusicToImagePaperPipeline")
        from llm_client import get_recommended_client
        print("  ✓ llm_client")
        from generate_visual_prompts_batch import BatchPromptGenerator
        print("  ✓ BatchPromptGenerator")
        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False


def test_dataset():
    """Test that dataset can be loaded."""
    print("\nTesting dataset...")
    try:
        import numpy as np
        dataset_path = "dataset/label_data_with_16kHz_audio.npy"
        data = np.load(dataset_path, allow_pickle=True)
        print(f"  ✓ Dataset loaded: {len(data)} samples")

        # Check first sample
        sample = data[0]
        if "audio" in sample and "audio_meta" in sample:
            print(f"  ✓ Sample structure valid")
            print(f"    - Audio shape: {sample['audio'].shape}")
            print(f"    - Sample rate: 16000 Hz (expected)")
            return True
        else:
            print(f"  ✗ Invalid sample structure")
            return False
    except Exception as e:
        print(f"  ✗ Dataset error: {e}")
        return False


async def test_feature_extraction():
    """Test feature extraction."""
    print("\nTesting feature extraction...")
    try:
        import numpy as np
        from music_analyzer import MusicAnalyzer

        # Load sample
        data = np.load("dataset/label_data_with_16kHz_audio.npy", allow_pickle=True)
        audio = data[0]["audio"][:16000]  # First second

        # Extract features
        analyzer = MusicAnalyzer(sr=16000)
        features = analyzer.analyze_audio(audio)

        print(f"  ✓ Features extracted:")
        print(f"    - Key: {features.key_signature}")
        print(f"    - Tempo: {features.tempo:.1f} BPM")
        print(f"    - Tonality: {features.tonality}")
        print(f"    - Mood: {features.overall_mood}")

        return True
    except Exception as e:
        print(f"  ✗ Feature extraction error: {e}")
        return False


async def test_llm_connection():
    """Test LLM connection."""
    print("\nTesting LLM connection...")
    try:
        from llm_client import get_recommended_client

        client = get_recommended_client()
        print(f"  ✓ LLM client: {type(client).__name__}")

        # Test simple prompt
        result = await client.analyze("Say 'Hello' in one word")
        if result:
            print(f"  ✓ LLM response: {result[:50]}...")
            return True
        else:
            print(f"  ✗ No response from LLM")
            return False
    except Exception as e:
        print(f"  ✗ LLM error: {e}")
        return False


async def test_batch_generator():
    """Test batch generator initialization."""
    print("\nTesting batch generator...")
    try:
        from generate_visual_prompts_batch import BatchPromptGenerator

        generator = BatchPromptGenerator(
            dataset_path="dataset/label_data_with_16kHz_audio.npy",
            output_dir="test_output"
        )

        print(f"  ✓ Generator initialized")
        print(f"    - Dataset: {len(generator.data)} samples")
        print(f"    - Output dir: {generator.output_dir}")
        print(f"    - LLM provider: {type(generator.llm_client).__name__}")

        return True
    except Exception as e:
        print(f"  ✗ Generator error: {e}")
        return False


async def test_single_sample():
    """Test generation on single sample."""
    print("\nTesting single sample generation...")
    try:
        from generate_visual_prompts_batch import BatchPromptGenerator

        generator = BatchPromptGenerator(
            dataset_path="dataset/label_data_with_16kHz_audio.npy",
            output_dir="test_output",
            batch_size=2  # Only 2 prompts for testing
        )

        # Get first sample
        audio = generator.data[0]["audio"]
        metadata = generator.data[0].get("audio_meta", {})

        # Generate prompts for one sample
        result = await generator.generate_prompts_for_sample(0, audio, metadata)

        if "prompts" in result and len(result["prompts"]) > 0:
            print(f"  ✓ Generated {len(result['prompts'])} prompts")
            print(f"    - Features extracted: {len(result.get('musical_features', {}))} features")
            print(f"    - Sample prompt: {result['prompts'][0]['visual_prompt'][:60]}...")
            return True
        else:
            print(f"  ✗ No prompts generated")
            return False
    except Exception as e:
        print(f"  ✗ Single sample error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_files():
    """Check that all batch generation files exist."""
    print("\nChecking batch generation files...")

    files = [
        "generate_visual_prompts_batch.py",
        "example_batch_generation.py",
        "run_batch_generation.sh",
        "BATCH_GENERATION_GUIDE.md",
        "BATCH_QUICK_REFERENCE.md"
    ]

    all_exist = True
    for fname in files:
        fpath = Path(fname)
        if fpath.exists():
            size = fpath.stat().st_size
            print(f"  ✓ {fname} ({size:,} bytes)")
        else:
            print(f"  ✗ {fname} NOT FOUND")
            all_exist = False

    return all_exist


async def main():
    """Run all tests."""
    print("=" * 60)
    print("BATCH GENERATION TEST SUITE")
    print("=" * 60)

    results = []

    # Static tests
    results.append(("Imports", test_imports()))
    results.append(("Dataset", test_dataset()))
    results.append(("Files", check_files()))

    # Async tests
    results.append(("Feature Extraction", await test_feature_extraction()))
    results.append(("LLM Connection", await test_llm_connection()))
    results.append(("Batch Generator", await test_batch_generator()))
    results.append(("Single Sample", await test_single_sample()))

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:.<40} {status}")

    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n✓ ALL TESTS PASSED! Ready to run batch generation.")
        print("\nNext steps:")
        print("1. python3 generate_visual_prompts_batch.py")
        print("   or")
        print("2. ./run_batch_generation.sh")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. Check errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
