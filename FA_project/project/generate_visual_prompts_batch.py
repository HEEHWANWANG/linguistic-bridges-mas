"""
Batch Visual Prompt Generation from Audio Dataset

Generates 5 visual prompts for each audio sample using:
- Convergent mode (T=0.4): 3 consistent prompts
- Divergent mode (T=0.8): 2 creative prompts

Saves results to JSON for downstream image generation pipeline.
"""

import asyncio
import json
import logging
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys

from music_to_image_paper_pipeline import MusicToImagePaperPipeline
from llm_client import get_recommended_client


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('generate_prompts.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BatchPromptGenerator:
    """Generate visual prompts for all audio samples in batch."""

    def __init__(
        self,
        dataset_path: str,
        output_dir: str = "generated_prompts",
        use_mel_spectrogram: bool = False,
        batch_size: int = 5
    ):
        """
        Initialize batch generator.

        Args:
            dataset_path: Path to label_data_with_16kHz_audio.npy
            output_dir: Directory to save results
            use_mel_spectrogram: Whether to use mel-spectrogram enhancement
            batch_size: Number of prompts per audio sample
        """
        self.dataset_path = dataset_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.use_mel_spectrogram = use_mel_spectrogram
        self.batch_size = batch_size

        # Load dataset
        logger.info(f"Loading dataset from {dataset_path}")
        self.data = np.load(dataset_path, allow_pickle=True)
        logger.info(f"Loaded {len(self.data)} audio samples")

        # Initialize pipelines (convergent and divergent)
        self.pipeline_convergent = MusicToImagePaperPipeline(
            generation_mode="convergent",
            use_mel_spectrogram=use_mel_spectrogram
        )
        self.pipeline_divergent = MusicToImagePaperPipeline(
            generation_mode="divergent",
            use_mel_spectrogram=use_mel_spectrogram
        )

        # Get LLM client
        self.llm_client = get_recommended_client()
        logger.info(f"Using LLM: {type(self.llm_client).__name__}")

        # Results storage
        self.results = {
            "metadata": {
                "dataset_path": str(dataset_path),
                "generation_timestamp": datetime.now().isoformat(),
                "total_samples": len(self.data),
                "prompts_per_sample": batch_size,
                "mel_spectrogram": use_mel_spectrogram,
                "llm_provider": type(self.llm_client).__name__,
                "sample_rate": 16000
            },
            "samples": []
        }

    async def generate_prompts_for_sample(
        self,
        sample_idx: int,
        audio: np.ndarray,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate 5 visual prompts for a single audio sample.

        Args:
            sample_idx: Index of the sample
            audio: Audio waveform (16kHz)
            metadata: Sample metadata

        Returns:
            Dictionary with features and 5 prompts (3 convergent, 2 divergent)
        """
        try:
            logger.info(f"Processing sample {sample_idx + 1}/{len(self.data)}")

            # Extract features once (same for all prompts)
            features_result = await self.pipeline_convergent.process_audio(
                audio, metadata, self.llm_client
            )

            sample_data = {
                "sample_idx": sample_idx,
                "metadata": metadata,
                "musical_features": {
                    "key": features_result["features"]["key"],
                    "tonality": features_result["features"]["tonality"],
                    "tempo": float(features_result["features"]["tempo"]),
                    "time_signature": features_result["features"]["time_signature"],
                    "mood": features_result["features"]["overall_mood"],
                    "melody_contour": features_result["features"]["melody_contour"],
                    "harmonic_progression": features_result["features"]["harmonic_progression"],
                    "dynamic_intensity": features_result["features"]["dynamic_intensity"]
                },
                "abc_notation": features_result["abc_notation"],
                "prompts": []
            }

            # Generate 3 convergent prompts (consistent, reproducible)
            logger.info(f"  Generating 3 convergent prompts...")
            for i in range(3):
                result = await self.pipeline_convergent.process_audio(
                    audio, metadata, self.llm_client
                )
                sample_data["prompts"].append({
                    "prompt_id": len(sample_data["prompts"]),
                    "mode": "convergent",
                    "temperature": 0.4,
                    "visual_prompt": result["visual_prompt"]
                })

            # Generate 2 divergent prompts (creative, exploratory)
            logger.info(f"  Generating 2 divergent prompts...")
            for i in range(2):
                result = await self.pipeline_divergent.process_audio(
                    audio, metadata, self.llm_client
                )
                sample_data["prompts"].append({
                    "prompt_id": len(sample_data["prompts"]),
                    "mode": "divergent",
                    "temperature": 0.8,
                    "visual_prompt": result["visual_prompt"]
                })

            logger.info(f"  ✓ Sample {sample_idx} complete: 5 prompts generated")
            return sample_data

        except Exception as e:
            logger.error(f"Error processing sample {sample_idx}: {e}")
            return {
                "sample_idx": sample_idx,
                "error": str(e),
                "prompts": []
            }

    async def generate_all_prompts(
        self,
        sample_indices: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Generate prompts for all (or specified) samples.

        Args:
            sample_indices: List of sample indices to process (None = all)

        Returns:
            Results dictionary with all prompts
        """
        if sample_indices is None:
            sample_indices = list(range(len(self.data)))

        logger.info(f"Starting batch generation for {len(sample_indices)} samples")
        logger.info(f"Each sample will generate {self.batch_size} prompts")

        for idx in sample_indices:
            try:
                audio = self.data[idx]["audio"]
                metadata = self.data[idx].get("audio_meta", {})

                sample_result = await self.generate_prompts_for_sample(
                    idx, audio, metadata
                )
                self.results["samples"].append(sample_result)

                # Save checkpoint every 10 samples
                if (len(self.results["samples"]) % 10) == 0:
                    self._save_results(checkpoint=True)
                    logger.info(f"Checkpoint: {len(self.results['samples'])} samples saved")

            except KeyboardInterrupt:
                logger.warning("Generation interrupted by user")
                self._save_results(checkpoint=True)
                raise
            except Exception as e:
                logger.error(f"Critical error at sample {idx}: {e}")
                continue

        return self.results

    def _save_results(self, checkpoint: bool = False) -> Path:
        """
        Save results to JSON file.

        Args:
            checkpoint: If True, save as checkpoint file

        Returns:
            Path to saved file
        """
        if checkpoint:
            filename = f"prompts_checkpoint_{len(self.results['samples']):03d}.json"
        else:
            filename = f"visual_prompts_complete.json"

        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)

        logger.info(f"Saved {len(self.results['samples'])} samples to {filepath}")
        return filepath

    def save_results(self) -> Path:
        """Save final results."""
        return self._save_results(checkpoint=False)

    def save_summary_stats(self) -> Path:
        """
        Save summary statistics about generated prompts.

        Returns:
            Path to summary file
        """
        summary = {
            "total_samples": len(self.results["samples"]),
            "total_prompts": len(self.results["samples"]) * self.batch_size,
            "convergent_prompts": len(self.results["samples"]) * 3,
            "divergent_prompts": len(self.results["samples"]) * 2,
            "generation_timestamp": self.results["metadata"]["generation_timestamp"],
            "samples_with_errors": sum(
                1 for s in self.results["samples"] if "error" in s
            ),
            "sample_summary": []
        }

        for sample in self.results["samples"]:
            if "prompts" in sample and len(sample["prompts"]) > 0:
                summary["sample_summary"].append({
                    "sample_idx": sample["sample_idx"],
                    "features": sample.get("musical_features", {}),
                    "prompt_count": len(sample["prompts"]),
                    "modes": list(set(p["mode"] for p in sample["prompts"]))
                })

        filepath = self.output_dir / "generation_summary.json"
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Saved summary stats to {filepath}")
        return filepath

    def export_for_image_generation(self) -> Path:
        """
        Export prompts in format ready for image generation pipeline.

        Returns:
            Path to export file
        """
        export_data = []

        for sample in self.results["samples"]:
            if "prompts" not in sample or len(sample["prompts"]) == 0:
                continue

            for prompt_data in sample["prompts"]:
                export_data.append({
                    "sample_idx": sample["sample_idx"],
                    "prompt_id": prompt_data["prompt_id"],
                    "mode": prompt_data["mode"],
                    "temperature": prompt_data["temperature"],
                    "visual_prompt": prompt_data["visual_prompt"],
                    "features": sample.get("musical_features", {}),
                    "abc_notation": sample.get("abc_notation", "")
                })

        filepath = self.output_dir / "prompts_for_image_generation.json"
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

        logger.info(f"Exported {len(export_data)} prompts to {filepath}")
        return filepath

    def print_summary(self):
        """Print summary of generation results."""
        total_samples = len(self.results["samples"])
        successful_samples = sum(
            1 for s in self.results["samples"]
            if "prompts" in s and len(s["prompts"]) > 0
        )
        total_prompts = successful_samples * self.batch_size

        print("\n" + "=" * 60)
        print("BATCH PROMPT GENERATION SUMMARY")
        print("=" * 60)
        print(f"Total samples processed: {total_samples}")
        print(f"Successful samples: {successful_samples}")
        print(f"Failed samples: {total_samples - successful_samples}")
        print(f"Total prompts generated: {total_prompts}")
        print(f"  - Convergent (T=0.4): {successful_samples * 3}")
        print(f"  - Divergent (T=0.8): {successful_samples * 2}")
        print(f"\nOutput directory: {self.output_dir.absolute()}")
        print(f"Files created:")
        print(f"  - visual_prompts_complete.json (all data)")
        print(f"  - prompts_for_image_generation.json (image pipeline format)")
        print(f"  - generation_summary.json (statistics)")
        print("=" * 60 + "\n")


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Batch generate visual prompts from audio dataset"
    )
    parser.add_argument(
        "--dataset",
        default="dataset/label_data_with_16kHz_audio.npy",
        help="Path to dataset NPY file"
    )
    parser.add_argument(
        "--output-dir",
        default="generated_prompts",
        help="Output directory for results"
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=None,
        help="Number of samples to process (default: all)"
    )
    parser.add_argument(
        "--start-idx",
        type=int,
        default=0,
        help="Starting sample index"
    )
    parser.add_argument(
        "--mel-spectrogram",
        action="store_true",
        help="Use mel-spectrogram enhancement"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of prompts per sample"
    )

    args = parser.parse_args()

    # Determine sample indices
    all_samples = np.load(args.dataset, allow_pickle=True)
    total_samples = len(all_samples)

    if args.samples is None:
        sample_indices = list(range(args.start_idx, total_samples))
    else:
        sample_indices = list(
            range(args.start_idx, min(args.start_idx + args.samples, total_samples))
        )

    logger.info(f"Processing {len(sample_indices)} samples out of {total_samples}")

    # Create generator and run
    generator = BatchPromptGenerator(
        dataset_path=args.dataset,
        output_dir=args.output_dir,
        use_mel_spectrogram=args.mel_spectrogram,
        batch_size=args.batch_size
    )

    try:
        await generator.generate_all_prompts(sample_indices)
        generator.save_results()
        generator.save_summary_stats()
        generator.export_for_image_generation()
        generator.print_summary()

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
