"""
Generate Images from Visual Prompts

Generates SDXL images from visual prompts saved in generated_prompts/visual_prompts_complete.json

Input:
  - visual_prompts_complete.json (500 prompts from 100 audio samples)

Output:
  - images/ directory with organized image files
  - image_generation_log.json with metadata for all generated images
  - image_generation_summary.json with statistics

Features:
  - Batch processing with checkpointing
  - Supports both GPU and CPU
  - Configurable image dimensions and quality
  - Progress tracking and error recovery
  - Optional refiner model for enhanced quality
"""

import asyncio
import json
import logging
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import sys

from image_generator import StableDiffusionXLGenerator, ImageGenerationConfig, create_image_generator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('generate_images.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BatchImageGenerator:
    """Generate images for all visual prompts in batch mode."""

    def __init__(
        self,
        prompts_file: str = "./generated_prompts/visual_prompts_complete.json",
        output_dir: str = "./images",
        image_height: int = 768,
        image_width: int = 768,
        num_inference_steps: int = 30,
        use_refiner: bool = False,
        device: str = "auto",
        save_images: bool = True
    ):
        """
        Initialize batch image generator.

        Args:
            prompts_file: Path to visual_prompts_complete.json
            output_dir: Directory to save generated images
            image_height: Height of generated images (multiple of 8)
            image_width: Width of generated images (multiple of 8)
            num_inference_steps: Number of diffusion steps (higher = better quality, slower)
            use_refiner: Whether to use refiner model (slower, better quality)
            device: "cuda", "cpu", or "auto"
            save_images: Whether to save images to disk
        """
        self.prompts_file = Path(prompts_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.image_height = image_height
        self.image_width = image_width
        self.num_inference_steps = num_inference_steps
        self.use_refiner = use_refiner
        self.device = device
        self.save_images = save_images

        # Load prompts
        logger.info(f"Loading prompts from {self.prompts_file}")
        self.prompts_data = self._load_prompts()

        # Initialize image generator
        logger.info("Initializing image generator...")
        self.generator = create_image_generator(
            device=device,
            use_refiner=use_refiner,
            height=image_height,
            width=image_width,
            num_steps=num_inference_steps
        )

        # Results storage
        self.results = {
            "metadata": {
                "prompts_file": str(self.prompts_file),
                "generation_timestamp": datetime.now().isoformat(),
                "total_prompts": 0,
                "image_height": image_height,
                "image_width": image_width,
                "num_inference_steps": num_inference_steps,
                "use_refiner": use_refiner,
                "device": device,
                "save_images": save_images
            },
            "generated_images": []
        }

    def _load_prompts(self) -> Dict[str, Any]:
        """Load prompts from JSON file."""
        try:
            with open(self.prompts_file, 'r') as f:
                data = json.load(f)

            logger.info(f"✓ Loaded prompts:")
            logger.info(f"  - Total samples: {len(data['samples'])}")
            total_prompts = sum(len(s.get('prompts', [])) for s in data['samples'])
            logger.info(f"  - Total prompts: {total_prompts}")

            return data

        except FileNotFoundError:
            logger.error(f"Prompts file not found: {self.prompts_file}")
            logger.error("Please run: python3 generate_visual_prompts_batch.py first")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in prompts file: {e}")
            raise

    async def generate_image_for_prompt(
        self,
        sample_idx: int,
        prompt_id: int,
        visual_prompt: str,
        mode: str,
        temperature: float
    ) -> Tuple[Optional[List], Optional[Dict[str, Any]]]:
        """
        Generate image(s) for a single visual prompt.

        Args:
            sample_idx: Index of audio sample
            prompt_id: ID of prompt within sample
            visual_prompt: Visual prompt text
            mode: "convergent" or "divergent"
            temperature: Temperature used for generation

        Returns:
            Tuple of (images, metadata) or (None, error_dict)
        """
        try:
            logger.info(f"  Generating image for sample {sample_idx}, prompt {prompt_id}...")

            # Generate image
            images, metadata = self.generator.generate(
                prompt=visual_prompt,
                num_images=1,
                height=self.image_height,
                width=self.image_width,
                num_steps=self.num_inference_steps
            )

            # Save image if requested
            image_path = None
            if self.save_images and images:
                image_path = self._save_image(sample_idx, prompt_id, images[0])

            return images, {
                "sample_idx": sample_idx,
                "prompt_id": prompt_id,
                "mode": mode,
                "temperature": temperature,
                "visual_prompt": visual_prompt,
                "image_path": str(image_path) if image_path else None,
                "status": "success",
                "generation_metadata": metadata
            }

        except Exception as e:
            logger.error(f"  ✗ Error generating image: {e}")
            return None, {
                "sample_idx": sample_idx,
                "prompt_id": prompt_id,
                "mode": mode,
                "temperature": temperature,
                "visual_prompt": visual_prompt,
                "status": "error",
                "error": str(e)
            }

    def _save_image(self, sample_idx: int, prompt_id: int, image) -> Optional[Path]:
        """Save generated image to disk."""
        try:
            # Create directory structure: images/sample_XXX/
            sample_dir = self.output_dir / f"sample_{sample_idx:03d}"
            sample_dir.mkdir(parents=True, exist_ok=True)

            # Create filename
            filename = f"sample_{sample_idx:03d}_prompt_{prompt_id:02d}.png"
            filepath = sample_dir / filename

            # Save image
            image.save(filepath)

            return filepath

        except Exception as e:
            logger.error(f"Failed to save image: {e}")
            return None

    async def generate_all_images(
        self,
        sample_indices: Optional[List[int]] = None,
        prompt_limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate images for all (or specified) prompts.

        Args:
            sample_indices: List of sample indices to process (None = all)
            prompt_limit: Maximum number of prompts to process (None = all)

        Returns:
            Results dictionary with all generated images
        """
        if sample_indices is None:
            sample_indices = list(range(len(self.prompts_data['samples'])))

        logger.info("=" * 80)
        logger.info("🎨 BATCH IMAGE GENERATION")
        logger.info("=" * 80)
        logger.info(f"Samples to process: {len(sample_indices)}")
        logger.info(f"Image dimensions: {self.image_width}x{self.image_height}")
        logger.info(f"Inference steps: {self.num_inference_steps}")
        logger.info(f"Use refiner: {self.use_refiner}")
        logger.info(f"Device: {self.generator.device}")
        logger.info("=" * 80 + "\n")

        prompt_count = 0
        successful = 0
        failed = 0

        for sample_idx in sample_indices:
            if sample_idx >= len(self.prompts_data['samples']):
                logger.warning(f"Sample {sample_idx} out of range")
                continue

            sample = self.prompts_data['samples'][sample_idx]
            prompts = sample.get('prompts', [])

            logger.info(f"\n📌 Sample {sample_idx}: {len(prompts)} prompts")

            for prompt_data in prompts:
                # Check prompt limit
                if prompt_limit and prompt_count >= prompt_limit:
                    logger.info(f"Reached prompt limit ({prompt_limit})")
                    break

                prompt_id = prompt_data['prompt_id']
                visual_prompt = prompt_data['visual_prompt']
                mode = prompt_data['mode']
                temperature = prompt_data['temperature']

                # Generate image
                images, metadata = await self.generate_image_for_prompt(
                    sample_idx, prompt_id, visual_prompt, mode, temperature
                )

                # Store result
                self.results["generated_images"].append(metadata)

                if metadata['status'] == 'success':
                    successful += 1
                else:
                    failed += 1

                prompt_count += 1

                # Checkpoint every 50 images
                if (successful + failed) % 50 == 0:
                    self._save_results(checkpoint=True)
                    logger.info(f"Checkpoint: {successful + failed} images processed")

            if prompt_limit and prompt_count >= prompt_limit:
                break

        # Update metadata
        self.results["metadata"]["total_prompts"] = prompt_count
        self.results["metadata"]["successful"] = successful
        self.results["metadata"]["failed"] = failed

        logger.info("\n" + "=" * 80)
        logger.info("✅ IMAGE GENERATION COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total prompts processed: {prompt_count}")
        logger.info(f"Successfully generated: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Output directory: {self.output_dir.absolute()}")
        logger.info("=" * 80 + "\n")

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
            filename = f"image_generation_checkpoint_{len(self.results['generated_images']):04d}.json"
        else:
            filename = "image_generation_log.json"

        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)

        logger.info(f"Saved results to {filepath}")
        return filepath

    def save_results(self) -> Path:
        """Save final results."""
        return self._save_results(checkpoint=False)

    def save_summary_stats(self) -> Path:
        """Save summary statistics about generated images."""
        successful = sum(1 for img in self.results["generated_images"] if img['status'] == 'success')
        failed = sum(1 for img in self.results["generated_images"] if img['status'] == 'error')

        # Group by mode
        convergent = sum(1 for img in self.results["generated_images"] if img['mode'] == 'convergent' and img['status'] == 'success')
        divergent = sum(1 for img in self.results["generated_images"] if img['mode'] == 'divergent' and img['status'] == 'success')

        # Group by sample
        samples_with_images = {}
        for img in self.results["generated_images"]:
            sample_idx = img['sample_idx']
            if sample_idx not in samples_with_images:
                samples_with_images[sample_idx] = {'convergent': 0, 'divergent': 0, 'failed': 0}

            if img['status'] == 'success':
                if img['mode'] == 'convergent':
                    samples_with_images[sample_idx]['convergent'] += 1
                else:
                    samples_with_images[sample_idx]['divergent'] += 1
            else:
                samples_with_images[sample_idx]['failed'] += 1

        summary = {
            "generation_timestamp": self.results["metadata"]["generation_timestamp"],
            "total_images_generated": successful,
            "total_images_failed": failed,
            "success_rate": (successful / (successful + failed) * 100) if (successful + failed) > 0 else 0,
            "by_mode": {
                "convergent": convergent,
                "divergent": divergent
            },
            "by_sample": samples_with_images,
            "image_dimensions": f"{self.image_width}x{self.image_height}",
            "inference_steps": self.num_inference_steps,
            "used_refiner": self.use_refiner,
            "device": self.generator.device,
            "output_directory": str(self.output_dir.absolute())
        }

        filepath = self.output_dir / "image_generation_summary.json"
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Saved summary stats to {filepath}")
        return filepath

    def print_summary(self):
        """Print summary of image generation results."""
        successful = sum(1 for img in self.results["generated_images"] if img['status'] == 'success')
        failed = sum(1 for img in self.results["generated_images"] if img['status'] == 'error')

        convergent = sum(1 for img in self.results["generated_images"]
                        if img['mode'] == 'convergent' and img['status'] == 'success')
        divergent = sum(1 for img in self.results["generated_images"]
                       if img['mode'] == 'divergent' and img['status'] == 'success')

        print("\n" + "=" * 80)
        print("BATCH IMAGE GENERATION SUMMARY")
        print("=" * 80)
        print(f"Total prompts processed: {successful + failed}")
        print(f"Successfully generated: {successful}")
        print(f"Failed: {failed}")
        print(f"Success rate: {(successful / (successful + failed) * 100) if (successful + failed) > 0 else 0:.1f}%")
        print(f"\nBy mode:")
        print(f"  Convergent (T=0.4): {convergent}")
        print(f"  Divergent (T=0.8): {divergent}")
        print(f"\nImage settings:")
        print(f"  Dimensions: {self.image_width}x{self.image_height}")
        print(f"  Inference steps: {self.num_inference_steps}")
        print(f"  Refiner model: {'Yes' if self.use_refiner else 'No'}")
        print(f"  Device: {self.generator.device}")
        print(f"\nOutput directory: {self.output_dir.absolute()}")
        print(f"Files created:")
        print(f"  - image_generation_log.json (all metadata)")
        print(f"  - image_generation_summary.json (statistics)")
        print(f"  - Images organized in sample_XXX/ directories")
        print("=" * 80 + "\n")


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate SDXL images from visual prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all images (GPU, high quality)
  python3 generate_images_from_prompts.py

  # Generate with lower resolution (faster)
  python3 generate_images_from_prompts.py --width 512 --height 512

  # Generate first 10 prompts only (testing)
  python3 generate_images_from_prompts.py --limit 10

  # Generate without saving images to disk (metadata only)
  python3 generate_images_from_prompts.py --no-save

  # Use CPU instead of GPU
  python3 generate_images_from_prompts.py --device cpu
        """
    )

    parser.add_argument(
        "--prompts-file",
        default="./generated_prompts/visual_prompts_complete.json",
        help="Path to visual_prompts_complete.json"
    )
    parser.add_argument(
        "--output-dir",
        default="./images",
        help="Directory to save generated images"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=768,
        help="Image width (default: 768, must be multiple of 8)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=768,
        help="Image height (default: 768, must be multiple of 8)"
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=30,
        help="Number of inference steps (default: 30, more = better quality)"
    )
    parser.add_argument(
        "--refiner",
        action="store_true",
        help="Use refiner model for enhanced quality (slower)"
    )
    parser.add_argument(
        "--device",
        choices=["cuda", "cpu", "auto"],
        default="auto",
        help="Device to use (default: auto-detect)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of prompts to process (for testing)"
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=None,
        help="Number of samples to process (default: all)"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save images to disk (metadata only)"
    )

    args = parser.parse_args()

    # Validate dimensions
    if args.width % 8 != 0 or args.height % 8 != 0:
        print(f"❌ Error: Image dimensions must be multiples of 8")
        print(f"   Width: {args.width}, Height: {args.height}")
        return 1

    try:
        # Create generator
        generator = BatchImageGenerator(
            prompts_file=args.prompts_file,
            output_dir=args.output_dir,
            image_height=args.height,
            image_width=args.width,
            num_inference_steps=args.steps,
            use_refiner=args.refiner,
            device=args.device,
            save_images=not args.no_save
        )

        # Determine samples to process
        sample_indices = None
        if args.samples:
            sample_indices = list(range(min(args.samples, len(generator.prompts_data['samples']))))

        # Generate images
        results = await generator.generate_all_images(
            sample_indices=sample_indices,
            prompt_limit=args.limit
        )

        # Save results
        generator.save_results()
        generator.save_summary_stats()
        generator.print_summary()

        return 0

    except KeyboardInterrupt:
        logger.warning("Generation interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
