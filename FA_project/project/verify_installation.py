#!/usr/bin/env python3
"""
Verify Installation and Dependencies

Checks that all required components are properly installed and configured
for the music-to-image paper implementation.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Verify Python version"""
    print("\n" + "=" * 60)
    print("🐍 PYTHON VERSION")
    print("=" * 60)

    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (requires 3.8+)")
        return False

def check_dependencies():
    """Check required Python packages"""
    print("\n" + "=" * 60)
    print("📦 REQUIRED DEPENDENCIES")
    print("=" * 60)

    required = {
        'numpy': 'Array operations',
        'librosa': 'Audio processing',
        'scipy': 'Scientific computing',
        'pyyaml': 'Configuration files',
        'pydantic': 'Data validation',
        'python-dotenv': 'Environment variables',
    }

    optional = {
        'anthropic': 'Claude API support',
        'requests': 'HTTP requests (Ollama)',
        'diffusers': 'Stable Diffusion XL',
        'torch': 'PyTorch (image generation)',
        'transformers': 'HuggingFace transformers',
        'safetensors': 'Safe tensor loading',
        'pillow': 'Image processing',
    }

    all_good = True

    print("\n📋 CORE DEPENDENCIES:")
    for package, description in required.items():
        try:
            __import__(package)
            print(f"  ✓ {package:<20} - {description}")
        except ImportError:
            print(f"  ✗ {package:<20} - {description} [MISSING]")
            all_good = False

    print("\n🔧 OPTIONAL DEPENDENCIES:")
    for package, description in optional.items():
        try:
            __import__(package)
            print(f"  ✓ {package:<20} - {description}")
        except ImportError:
            print(f"  ○ {package:<20} - {description} [not installed]")

    return all_good

def check_dataset():
    """Verify dataset file exists"""
    print("\n" + "=" * 60)
    print("📊 DATASET")
    print("=" * 60)

    dataset_path = Path("../dataset/label_data_with_16kHz_audio.npy")

    if dataset_path.exists():
        size_mb = dataset_path.stat().st_size / (1024 * 1024)
        print(f"✓ Found: {dataset_path.resolve()}")
        print(f"  Size: {size_mb:.1f} MB")
        return True
    else:
        print(f"✗ Not found: {dataset_path.resolve()}")
        print(f"  Expected path: ./FA_project/dataset/label_data_with_16kHz_audio.npy")
        return False

def check_llm_config():
    """Check LLM configuration"""
    print("\n" + "=" * 60)
    print("🤖 LLM CONFIGURATION")
    print("=" * 60)

    # Check for Claude API
    claude_key = os.environ.get('ANTHROPIC_API_KEY')
    if claude_key:
        print(f"✓ Claude API configured")
        print(f"  Key: {claude_key[:20]}...***")
    else:
        print(f"○ Claude API not configured")
        print(f"  Set: export ANTHROPIC_API_KEY=your-api-key")

    # Check for Ollama
    ollama_host = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
    print(f"○ Ollama host: {ollama_host}")
    print(f"  (Uses mock mode if neither Claude nor Ollama available)")

    return claude_key is not None

def check_core_files():
    """Verify core implementation files exist"""
    print("\n" + "=" * 60)
    print("📄 CORE IMPLEMENTATION FILES")
    print("=" * 60)

    core_files = {
        'music_analyzer.py': 'Feature extraction',
        'prompt_builder_paper.py': 'Paper-faithful prompts',
        'music_to_image_paper_pipeline.py': 'Main pipeline',
        'llm_client.py': 'LLM abstraction',
        'image_generator.py': 'SDXL integration',
        'config.yaml': 'Configuration',
    }

    all_exist = True
    for filename, description in core_files.items():
        filepath = Path(filename)
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            print(f"✓ {filename:<35} ({size_kb:.1f} KB) - {description}")
        else:
            print(f"✗ {filename:<35} [MISSING]")
            all_exist = False

    return all_exist

def check_example_files():
    """Verify example files exist"""
    print("\n" + "=" * 60)
    print("📚 EXAMPLE FILES")
    print("=" * 60)

    examples = {
        'example_paper_implementation.py': 'Paper-faithful examples',
        'example_usage.py': 'Multi-agent examples (optional)',
    }

    for filename, description in examples.items():
        filepath = Path(filename)
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            print(f"✓ {filename:<35} ({size_kb:.1f} KB) - {description}")
        else:
            print(f"○ {filename:<35} [optional]")

def print_summary(checks):
    """Print verification summary"""
    print("\n" + "=" * 60)
    print("✅ VERIFICATION SUMMARY")
    print("=" * 60)

    results = {
        'Python Version': checks['python'],
        'Dependencies': checks['deps'],
        'Dataset': checks['dataset'],
        'Core Files': checks['files'],
    }

    all_required_good = all(results.values())

    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:<8} - {check_name}")

    print("\n" + "=" * 60)

    if all_required_good:
        print("🎉 All checks passed! Ready to run paper implementation.")
        print("\nQuick start:")
        print("  python3 example_paper_implementation.py")
        return 0
    else:
        print("⚠️  Some checks failed. See above for details.")
        print("\nTo fix:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Verify dataset path: ./FA_project/dataset/label_data_with_16kHz_audio.npy")
        print("  3. Configure LLM: export ANTHROPIC_API_KEY=your-key")
        return 1

def main():
    """Run all verification checks"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Music-to-Image Paper Implementation" + " " * 13 + "║")
    print("║" + " " * 15 + "Installation Verification" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")

    checks = {
        'python': check_python_version(),
        'deps': check_dependencies(),
        'dataset': check_dataset(),
        'llm': check_llm_config(),
        'files': check_core_files(),
    }

    check_example_files()

    return print_summary(checks)

if __name__ == "__main__":
    sys.exit(main())
