"""
Complete Music-to-Image Pipeline - End-to-end system from audio to images

Orchestrates:
1. Audio loading and analysis
2. Musical feature extraction
3. Visual prompt generation via LLM
4. Image generation using Stable Diffusion XL

This is the complete pipeline integrating all components.
"""

import asyncio
import logging
import torch
from typing import Dict, Any, Optional, List
from pathlib import Path

from music_to_image_pipeline import MusicToImagePipeline, AudioLoaderFromNPY
from llm_client import get_recommended_client, create_llm_client
from image_generator import StableDiffusionXLGenerator, ImageGenerationConfig
from mel_spectrogram_converter import MelSpectrogramConfig

logger = logging.getLogger(__name__)


class CompleteMusicToImagePipeline:
    """
    Complete end-to-end music-to-image system

    Flow:
    1. Load audio from dataset
    2. Extract musical features
    3. Generate ABC notation
    4. Get LLM analysis and visual prompts
    5. Generate images using Stable Diffusion XL
    """

    def __init__(self,
                 sample_rate: int = 16000,
                 generation_mode: str = "convergent",
                 use_designer_agents: bool = True,
                 use_mel_spectrogram: bool = False,
                 image_generation_enabled: bool = True,
                 image_output_dir: str = "./generated_images"):
        """
        Initialize complete pipeline

        Args:
            sample_rate: Audio sample rate
            generation_mode: "convergent" or "divergent"
            use_designer_agents: Use 5 designer roles
            use_mel_spectrogram: Include mel-spectrogram analysis
            image_generation_enabled: Generate actual images
            image_output_dir: Directory to save generated images
        """
        self.sample_rate = sample_rate
        self.generation_mode = generation_mode
        self.use_designer_agents = use_designer_agents
        self.use_mel_spectrogram = use_mel_spectrogram
        self.image_generation_enabled = image_generation_enabled
        self.image_output_dir = image_output_dir

        self.logger = logging.getLogger(__name__)

        # Initialize music-to-prompt pipeline
        self.logger.info("Initializing music-to-prompt pipeline...")
        self.music_pipeline = MusicToImagePipeline(
            sample_rate=sample_rate,
            generation_mode=generation_mode,
            use_designer_agents=use_designer_agents,
            use_mel_spectrogram=use_mel_spectrogram
        )
        self.logger.info("✓ Music pipeline initialized")

        # Initialize image generator if enabled
        self.image_generator = None
        if self.image_generation_enabled:
            self.logger.info("Initializing image generator...")
            self.image_generator = StableDiffusionXLGenerator(
                ImageGenerationConfig(
                    device="auto",
                    height=1024,
                    width=1024,
                    num_inference_steps=30,
                    use_refiner=True
                )
            )
            self.logger.info("✓ Image generator initialized")

    async def process_audio_to_images(self,
                                      audio_data,
                                      metadata: Dict[str, Any] = None,
                                      llm_client=None,
                                      save_images: bool = True) -> Dict[str, Any]:
        """
        Process audio through complete pipeline to image generation

        Args:
            audio_data: Audio waveform
            metadata: Audio metadata
            llm_client: LLM client for prompt generation
            save_images: Whether to save generated images

        Returns:
            Complete results dictionary
        """
        self.logger.info("\n" + "=" * 70)
        self.logger.info("🎵➜🎨 COMPLETE MUSIC-TO-IMAGE PIPELINE")
        self.logger.info("=" * 70)

        results = {
            "audio_analysis": None,
            "visual_prompts": None,
            "generated_images": None,
            "metadata": metadata or {}
        }

        try:
            # Step 1: Music analysis and prompt generation
            self.logger.info("\n📊 PHASE 1: Audio Analysis & Prompt Generation")
            self.logger.info("-" * 70)

            if llm_client is None:
                try:
                    llm_client = get_recommended_client()
                    self.logger.info(f"Using LLM: {llm_client.get_model_name()}")
                except:
                    self.logger.info("No LLM available, using mock client")
                    llm_client = create_llm_client("mock")

            prompt_results = await self.music_pipeline.process_audio(
                audio_data=audio_data,
                metadata=metadata,
                llm_client=llm_client
            )

            results["audio_analysis"] = prompt_results
            self.logger.info("\n✓ Audio analysis complete")

            # Step 2: Image generation
            if self.image_generation_enabled and self.image_generator:
                self.logger.info("\n🎨 PHASE 2: Image Generation")
                self.logger.info("-" * 70)

                visual_prompt = prompt_results.get("final_image_prompt", "")

                if visual_prompt:
                    self.logger.info(f"\n📝 Using visual prompt ({len(visual_prompt)} chars):")
                    self.logger.info(f"{visual_prompt[:200]}...")

                    try:
                        # Generate images
                        images, gen_metadata = self.image_generator.generate(
                            prompt=visual_prompt,
                            num_images=1,
                            guidance_scale=7.5,
                            num_steps=30,
                            seed=42
                        )

                        results["generated_images"] = images
                        results["image_metadata"] = gen_metadata

                        # Save images if requested
                        if save_images and images:
                            self._save_generated_images(
                                images,
                                prompt_results.get("features", {}).get("overall_mood", "unknown"),
                                metadata
                            )

                        self.logger.info(f"\n✓ Generated {len(images)} image(s)")

                    except Exception as e:
                        self.logger.error(f"Image generation failed: {e}")
                        self.logger.info("Continuing with prompt results only...")
                else:
                    self.logger.warning("No visual prompt available for image generation")
            else:
                self.logger.info("\n⏭️  Image generation disabled or not initialized")

            self.logger.info("\n" + "=" * 70)
            self.logger.info("✅ Complete pipeline execution successful!")
            self.logger.info("=" * 70)

            return results

        except Exception as e:
            self.logger.error(f"Pipeline error: {e}")
            import traceback
            traceback.print_exc()
            raise

    def _save_generated_images(self,
                              images: list,
                              mood: str,
                              metadata: Dict[str, Any]):
        """Save generated images with metadata"""
        try:
            output_path = Path(self.image_output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            for idx, image in enumerate(images):
                filename = f"music_{mood}_{idx:02d}.png"
                filepath = output_path / filename
                image.save(filepath)
                self.logger.info(f"  ✓ Saved: {filename}")

        except Exception as e:
            self.logger.error(f"Failed to save images: {e}")

    async def process_batch(self,
                           audio_samples: List[tuple],
                           llm_client=None,
                           save_images: bool = True) -> List[Dict[str, Any]]:
        """
        Process multiple audio samples

        Args:
            audio_samples: List of (audio_data, metadata) tuples
            llm_client: LLM client
            save_images: Whether to save images

        Returns:
            List of results for each sample
        """
        self.logger.info(f"\n🎵 Batch Processing: {len(audio_samples)} samples")
        self.logger.info("=" * 70)

        results = []

        for idx, (audio_data, metadata) in enumerate(audio_samples):
            self.logger.info(f"\n[{idx + 1}/{len(audio_samples)}] Processing sample...")

            try:
                result = await self.process_audio_to_images(
                    audio_data=audio_data,
                    metadata=metadata,
                    llm_client=llm_client,
                    save_images=save_images
                )
                results.append(result)

            except Exception as e:
                self.logger.error(f"Failed to process sample {idx}: {e}")
                results.append({"error": str(e)})

        self.logger.info("\n" + "=" * 70)
        self.logger.info(f"✅ Batch processing complete: {len(results)} samples")
        self.logger.info("=" * 70)

        return results

    def cleanup(self):
        """Clean up resources"""
        self.logger.info("Cleaning up resources...")
        if self.image_generator:
            self.image_generator.free_memory()
        self.logger.info("✓ Cleanup complete")


async def main():
    """Example usage of complete pipeline"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger.info("\n")
    logger.info("╔" + "=" * 68 + "╗")
    logger.info("║" + " " * 10 + "Complete Music-to-Image Pipeline Example" + " " * 18 + "║")
    logger.info("╚" + "=" * 68 + "╝")

    # Create pipeline
    pipeline = CompleteMusicToImagePipeline(
        sample_rate=16000,
        generation_mode="convergent",
        use_designer_agents=True,
        use_mel_spectrogram=False,  # Set to True to use mel-spectrogram
        image_generation_enabled=True,
        image_output_dir="./generated_images"
    )

    # Load audio sample
    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"
    audio_loader = AudioLoaderFromNPY()

    try:
        audio, metadata = audio_loader.load_sample(dataset_path, sample_idx=0)

        # Process single sample
        logger.info("\n📍 Processing single sample...")
        result = await pipeline.process_audio_to_images(
            audio_data=audio,
            metadata=metadata,
            save_images=True
        )

        # Display results
        if "generated_images" in result and result["generated_images"]:
            logger.info(f"\n✅ Generated {len(result['generated_images'])} image(s)")

        # Process batch (optional)
        logger.info("\n\n📍 Processing batch (first 3 samples)...")
        batch_samples = audio_loader.load_batch(dataset_path, indices=[0, 1, 2])
        batch_results = await pipeline.process_batch(
            audio_samples=batch_samples,
            save_images=True
        )

        logger.info(f"✅ Batch results: {len(batch_results)} samples")

    except FileNotFoundError:
        logger.error(f"Dataset not found at {dataset_path}")
        logger.info("Make sure the audio dataset is at: ./FA_project/dataset/label_data_with_16kHz_audio.npy")

    finally:
        pipeline.cleanup()
        logger.info("\n✨ Pipeline execution complete!")


if __name__ == "__main__":
    asyncio.run(main())
