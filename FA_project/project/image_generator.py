"""
Image Generator - Generates images from visual prompts using Stable Diffusion XL

Based on text-to-image generation with Hugging Face Diffusers library.
Supports both CPU and GPU processing with configurable parameters.
"""

import logging
import torch
import numpy as np
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline

logger = logging.getLogger(__name__)


@dataclass
class ImageGenerationConfig:
    """Configuration for image generation"""
    model_id: str = "stabilityai/stable-diffusion-xl-base-1.0"  # Base model
    refiner_model_id: str = "stabilityai/stable-diffusion-xl-refiner-1.0"  # Refiner model
    height: int = 1024  # Image height (must be multiple of 8)
    width: int = 1024  # Image width (must be multiple of 8)
    num_inference_steps: int = 30  # Number of denoising steps
    guidance_scale: float = 7.5  # Classifier-free guidance scale
    num_images_per_prompt: int = 1  # Number of images to generate
    use_refiner: bool = True  # Whether to use refiner model for refinement
    negative_prompt: Optional[str] = None  # Negative guidance prompt
    seed: Optional[int] = None  # Random seed for reproducibility
    device: str = "auto"  # "cuda", "cpu", or "auto" (auto-detect)
    torch_dtype: torch.dtype = torch.float16  # Precision (float16 for memory efficiency)
    use_safetensors: bool = True  # Use safetensors format for safety

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "model_id": self.model_id,
            "refiner_model_id": self.refiner_model_id,
            "height": self.height,
            "width": self.width,
            "num_inference_steps": self.num_inference_steps,
            "guidance_scale": self.guidance_scale,
            "num_images_per_prompt": self.num_images_per_prompt,
            "use_refiner": self.use_refiner,
            "negative_prompt": self.negative_prompt,
            "seed": self.seed,
            "device": self.device,
            "torch_dtype": self.torch_dtype,
            "use_safetensors": self.use_safetensors
        }


class StableDiffusionXLGenerator:
    """
    Image generator using Stable Diffusion XL from Hugging Face

    Provides:
    - High-quality image generation from text prompts
    - Optional refiner model for enhanced quality
    - Flexible configuration for different hardware
    - Batch processing support
    - Reproducible generation with seed control
    """

    def __init__(self, config: Optional[ImageGenerationConfig] = None):
        """
        Initialize the image generator

        Args:
            config: ImageGenerationConfig instance (uses defaults if None)
        """
        self.config = config or ImageGenerationConfig()
        self.logger = logging.getLogger(__name__)

        # Detect device if auto-selected
        if self.config.device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.logger.info(f"Auto-detected device: {self.device}")
        else:
            self.device = self.config.device

        # Initialize models
        self.pipeline = None
        self.refiner_pipeline = None
        self._initialize_pipelines()

    def _initialize_pipelines(self):
        """Initialize base and refiner pipelines"""
        self.logger.info("Initializing Stable Diffusion XL pipelines...")
        self.logger.info(f"  Device: {self.device}")
        self.logger.info(f"  Precision: {self.config.torch_dtype}")

        try:
            # Initialize base pipeline
            self.logger.info(f"Loading base model: {self.config.model_id}")
            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                self.config.model_id,
                torch_dtype=self.config.torch_dtype,
                use_safetensors=self.config.use_safetensors,
                variant="fp16" if self.config.torch_dtype == torch.float16 else None
            )
            self.pipeline.to(self.device)
            self.logger.info("✓ Base model loaded successfully")

            # Initialize refiner pipeline if enabled
            if self.config.use_refiner:
                self.logger.info(f"Loading refiner model: {self.config.refiner_model_id}")
                self.refiner_pipeline = StableDiffusionXLPipeline.from_pretrained(
                    self.config.refiner_model_id,
                    torch_dtype=self.config.torch_dtype,
                    use_safetensors=self.config.use_safetensors,
                    variant="fp16" if self.config.torch_dtype == torch.float16 else None
                )
                self.refiner_pipeline.to(self.device)
                self.logger.info("✓ Refiner model loaded successfully")

            # Enable memory optimization
            if self.device == "cuda":
                self.pipeline.enable_attention_slicing()
                if self.refiner_pipeline:
                    self.refiner_pipeline.enable_attention_slicing()
                self.logger.info("✓ Memory optimization enabled")

        except Exception as e:
            self.logger.error(f"Failed to initialize pipelines: {e}")
            raise

    def generate(self,
                 prompt: str,
                 negative_prompt: Optional[str] = None,
                 num_images: Optional[int] = None,
                 guidance_scale: Optional[float] = None,
                 num_steps: Optional[int] = None,
                 seed: Optional[int] = None,
                 height: Optional[int] = None,
                 width: Optional[int] = None) -> Tuple[list, Dict[str, Any]]:
        """
        Generate images from a text prompt

        Args:
            prompt: Text prompt for image generation
            negative_prompt: Negative prompt to guide generation away from certain concepts
            num_images: Number of images to generate (overrides config)
            guidance_scale: Guidance scale (overrides config)
            num_steps: Number of inference steps (overrides config)
            seed: Random seed for reproducibility
            height: Image height (overrides config)
            width: Image width (overrides config)

        Returns:
            Tuple of (images list, metadata dict)
        """
        self.logger.info("=" * 60)
        self.logger.info("🎨 Starting Image Generation")
        self.logger.info("=" * 60)

        # Use config defaults if not specified
        num_images = num_images or self.config.num_images_per_prompt
        guidance_scale = guidance_scale or self.config.guidance_scale
        num_steps = num_steps or self.config.num_inference_steps
        seed = seed or self.config.seed
        height = height or self.config.height
        width = width or self.config.width
        negative_prompt = negative_prompt or self.config.negative_prompt

        # Validate dimensions
        if height % 8 != 0 or width % 8 != 0:
            self.logger.warning(f"Height and width should be multiples of 8")
            height = (height // 8) * 8
            width = (width // 8) * 8
            self.logger.info(f"Adjusted to: {width}x{height}")

        # Set seed for reproducibility
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device)
            generator.manual_seed(seed)
            self.logger.info(f"Using seed: {seed}")

        self.logger.info(f"\n📝 Prompt: {prompt[:100]}...")
        if negative_prompt:
            self.logger.info(f"❌ Negative prompt: {negative_prompt[:100]}...")

        self.logger.info(f"\n⚙️  Generation parameters:")
        self.logger.info(f"   Images: {num_images}")
        self.logger.info(f"   Guidance scale: {guidance_scale}")
        self.logger.info(f"   Steps: {num_steps}")
        self.logger.info(f"   Resolution: {width}x{height}")

        try:
            # Generate images with base model
            self.logger.info("\n🔄 Running base model inference...")
            images = self.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                height=height,
                width=width,
                num_inference_steps=num_steps,
                guidance_scale=guidance_scale,
                num_images_per_prompt=num_images,
                generator=generator,
                output_type="latent" if self.config.use_refiner else "pil"
            ).images

            self.logger.info(f"✓ Base model inference complete ({len(images)} images)")

            # Refine images if refiner is enabled
            if self.config.use_refiner and self.refiner_pipeline:
                self.logger.info("\n✨ Refining with refiner model...")
                images = self.refiner_pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=images,
                    num_inference_steps=num_steps // 2,  # Use fewer steps for refinement
                    guidance_scale=guidance_scale,
                    generator=generator
                ).images
                self.logger.info(f"✓ Refiner inference complete")

            self.logger.info("\n✅ Image generation successful!")
            self.logger.info("=" * 60)

            # Prepare metadata
            metadata = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "guidance_scale": guidance_scale,
                "num_inference_steps": num_steps,
                "height": height,
                "width": width,
                "num_images": num_images,
                "seed": seed,
                "used_refiner": self.config.use_refiner,
                "model_id": self.config.model_id,
                "refiner_model_id": self.config.refiner_model_id if self.config.use_refiner else None
            }

            return images, metadata

        except Exception as e:
            self.logger.error(f"Image generation failed: {e}")
            raise

    def generate_batch(self,
                      prompts: list,
                      num_images: int = 1,
                      save_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate images for multiple prompts

        Args:
            prompts: List of text prompts
            num_images: Images per prompt
            save_dir: Directory to save images (if provided)

        Returns:
            Dictionary with all results
        """
        self.logger.info(f"\n📦 Batch Generation: {len(prompts)} prompts")
        self.logger.info("=" * 60)

        results = {
            "prompts": prompts,
            "generated_images": [],
            "metadata": []
        }

        for idx, prompt in enumerate(prompts):
            self.logger.info(f"\n[{idx + 1}/{len(prompts)}] Processing prompt...")
            try:
                images, metadata = self.generate(
                    prompt=prompt,
                    num_images=num_images
                )
                results["generated_images"].append(images)
                results["metadata"].append(metadata)

                # Save if directory provided
                if save_dir:
                    self._save_images(images, prompt, save_dir, idx)

            except Exception as e:
                self.logger.error(f"Failed to generate for prompt {idx}: {e}")
                results["generated_images"].append([])
                results["metadata"].append({"error": str(e)})

        self.logger.info("\n" + "=" * 60)
        self.logger.info(f"✅ Batch generation complete: {len(results['generated_images'])} prompts processed")

        return results

    def _save_images(self,
                    images: list,
                    prompt: str,
                    save_dir: str,
                    batch_idx: int):
        """Save generated images to disk"""
        try:
            save_path = Path(save_dir)
            save_path.mkdir(parents=True, exist_ok=True)

            # Create safe filename from prompt
            safe_prompt = prompt[:50].replace(" ", "_").replace("/", "_")
            filename_base = f"batch{batch_idx:03d}_{safe_prompt}"

            for img_idx, image in enumerate(images):
                filename = f"{filename_base}_img{img_idx:02d}.png"
                filepath = save_path / filename
                image.save(filepath)
                self.logger.info(f"  ✓ Saved: {filename}")

        except Exception as e:
            self.logger.error(f"Failed to save images: {e}")

    def free_memory(self):
        """Free GPU memory"""
        if self.pipeline:
            self.pipeline.to("cpu")
        if self.refiner_pipeline:
            self.refiner_pipeline.to("cpu")

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        self.logger.info("Memory freed")


def create_image_generator(
    device: str = "auto",
    use_refiner: bool = True,
    height: int = 1024,
    width: int = 1024,
    num_steps: int = 30) -> StableDiffusionXLGenerator:
    """
    Factory function to create an image generator

    Args:
        device: "cuda", "cpu", or "auto"
        use_refiner: Whether to use refiner model
        height: Image height
        width: Image width
        num_steps: Number of inference steps

    Returns:
        Configured StableDiffusionXLGenerator instance
    """
    config = ImageGenerationConfig(
        device=device,
        use_refiner=use_refiner,
        height=height,
        width=width,
        num_inference_steps=num_steps,
        torch_dtype=torch.float16 if device != "cpu" else torch.float32
    )
    return StableDiffusionXLGenerator(config)


# Example usage and testing
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Create generator
    generator = create_image_generator(
        device="auto",
        use_refiner=True,
        height=1024,
        width=1024,
        num_steps=30
    )

    # Test single image generation
    prompt = "A vibrant sunset over a mountain landscape, oil painting style, warm colors"
    images, metadata = generator.generate(
        prompt=prompt,
        seed=42,
        num_images=1
    )

    print(f"\nGenerated {len(images)} image(s)")
    print(f"Metadata: {metadata}")

    # Save test image
    if images:
        images[0].save("test_output.png")
        print("✓ Test image saved to test_output.png")

    # Clean up
    generator.free_memory()
