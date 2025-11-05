"""
Music-to-Image Pipeline (Paper Implementation)

Strictly follows "Exploring Real-Time Music-to-Image Systems" (Yang et al., 2407.05584v1)

Framework:
1. Load audio/MIDI → Extract features
2. Convert to ABC notation
3. Send to GPT for visual prompt generation
4. Generate images using SDXL

No multi-agent extensions - pure paper implementation for reproducibility.
"""

import numpy as np
import logging
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from music_analyzer import MusicAnalyzer, MusicalFeatures
from prompt_builder_paper import PromptBuilderPaper

logger = logging.getLogger(__name__)


class MusicToImagePaperPipeline:
    """
    Music-to-Image Pipeline following the paper's framework.

    Simple, direct implementation for reproducibility:
    Audio → Features → ABC Notation → LLM Prompt → Visual Prompt
    """

    def __init__(self,
                 sample_rate: int = 16000,
                 generation_mode: str = "convergent",
                 use_mel_spectrogram: bool = False):
        """
        Initialize pipeline

        Args:
            sample_rate: Audio sample rate (Hz)
            generation_mode: "convergent" (0.4 temp) or "divergent" (0.8 temp)
            use_mel_spectrogram: Include mel-spectrogram analysis
        """
        self.sample_rate = sample_rate
        self.generation_mode = generation_mode
        self.use_mel_spectrogram = use_mel_spectrogram

        self.music_analyzer = MusicAnalyzer(sr=sample_rate)
        self.prompt_builder = PromptBuilderPaper(generation_mode=generation_mode)

        # Optional mel-spectrogram support
        if self.use_mel_spectrogram:
            from mel_spectrogram_converter import MelSpectrogramConverter, MelSpectrogramConfig
            mel_config = MelSpectrogramConfig(sample_rate=sample_rate)
            self.mel_converter = MelSpectrogramConverter(mel_config)
        else:
            self.mel_converter = None

        self.logger = logging.getLogger(__name__)
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    async def process_audio(self,
                           audio_data: np.ndarray,
                           metadata: Dict[str, Any] = None,
                           llm_client=None) -> Dict[str, Any]:
        """
        Process audio following the paper's pipeline

        Args:
            audio_data: Audio waveform
            metadata: Audio metadata
            llm_client: LLM client for prompt generation

        Returns:
            Results with visual prompt ready for image generation
        """
        self.logger.info("=" * 60)
        self.logger.info("🎵 Music-to-Image Pipeline (Paper Implementation)")
        self.logger.info("=" * 60)

        # Step 1: Feature extraction
        self.logger.info("\n1️⃣  Extracting musical features...")
        features = self.music_analyzer.analyze_audio(audio_data)
        self.logger.info(f"   ✓ Key: {features.key_signature}, Tempo: {features.tempo:.0f} BPM")
        self.logger.info(f"   ✓ Mood: {features.overall_mood}")

        # Step 2: ABC notation generation
        self.logger.info("\n2️⃣  Converting to ABC notation...")
        abc_notation = features.to_abc_notation()
        self.logger.info(f"   ✓ Generated ABC notation ({len(abc_notation)} chars)")

        # Step 3: Optional mel-spectrogram
        mel_spectrogram_text = None
        if self.use_mel_spectrogram and self.mel_converter:
            self.logger.info("\n3️⃣  Computing mel-spectrogram...")
            mel_spec = self.mel_converter.audio_to_mel_spectrogram(audio_data)
            mel_spectrogram_text = self.mel_converter.mel_spectrogram_to_text_representation(mel_spec)
            self.logger.info(f"   ✓ Mel-spectrogram: {mel_spec.shape[0]}×{mel_spec.shape[1]}")
            step_offset = 1
        else:
            step_offset = 0

        # Step 4: Build prompt for LLM
        step_num = 3 + step_offset
        self.logger.info(f"\n{step_num}️⃣  Building LLM prompt...")
        gpt_prompt = self.prompt_builder.build_gpt_prompt(
            features,
            abc_notation,
            mel_spectrogram_text=mel_spectrogram_text,
            use_mel_spectrogram=self.use_mel_spectrogram
        )
        self.logger.info(f"   ✓ Prompt prepared ({len(gpt_prompt)} chars)")

        # Prepare results
        results = {
            "metadata": metadata or {},
            "features": {
                "key": features.key_signature,
                "tonality": features.tonality,
                "tempo": float(features.tempo),
                "time_signature": features.time_signature,
                "melody_contour": features.melody_contour,
                "harmonic_progression": features.harmonic_progression,
                "dynamic_intensity": features.dynamic_intensity,
                "overall_mood": features.overall_mood,
            },
            "abc_notation": abc_notation,
            "gpt_prompt": gpt_prompt,
            "temperature": self.prompt_builder.get_temperature(),
            "generation_mode": self.generation_mode
        }

        # Step 5: LLM analysis if client provided
        if llm_client:
            step_num = 4 + step_offset
            self.logger.info(f"\n{step_num}️⃣  Sending to LLM for visual prompt generation...")

            try:
                visual_prompt = await llm_client.analyze(gpt_prompt)
                results["visual_prompt"] = visual_prompt
                self.logger.info("   ✓ LLM analysis complete")

            except Exception as e:
                self.logger.error(f"   ✗ LLM analysis failed: {e}")
                results["visual_prompt"] = self._create_fallback_prompt(features)
        else:
            self.logger.info(f"\n{4 + step_offset}️⃣  No LLM client provided")
            results["visual_prompt"] = self._create_fallback_prompt(features)

        self.logger.info("\n" + "=" * 60)
        self.logger.info("✅ Pipeline complete - Ready for image generation")
        self.logger.info("=" * 60)

        return results

    def _create_fallback_prompt(self, features: MusicalFeatures) -> str:
        """Create fallback visual prompt from features only"""
        # Map features to visual concepts (paper's approach)
        tempo_energy = "dynamic and energetic" if features.tempo > 120 else "calm and serene"
        key_colors = "warm and bright" if features.tonality == "major" else "cool and dark"
        melody_flow = features.melody_contour

        prompt = f"""A {features.overall_mood} visual scene in {key_colors} colors.
The composition conveys a {tempo_energy} mood with {melody_flow} compositional flow.
The harmonic progression is {features.harmonic_progression} with {features.dynamic_intensity} intensity."""

        return prompt.strip()


class AudioLoaderFromNPY:
    """Helper class to load audio from NPY files"""

    @staticmethod
    def load_sample(npy_path: str, sample_idx: int = 0) -> tuple:
        """Load a single audio sample"""
        try:
            data = np.load(npy_path, allow_pickle=True)
            sample = data[sample_idx]
            audio = sample['audio']
            metadata = sample['audio_meta'] if 'audio_meta' in sample else {}
            return audio, metadata
        except Exception as e:
            logger.error(f"Failed to load audio: {e}")
            raise

    @staticmethod
    def load_batch(npy_path: str, indices: List[int] = None) -> List[tuple]:
        """Load multiple audio samples"""
        data = np.load(npy_path, allow_pickle=True)

        if indices is None:
            indices = list(range(len(data)))

        samples = []
        for idx in indices:
            if idx < len(data):
                sample = data[idx]
                audio = sample['audio']
                metadata = sample['audio_meta'] if 'audio_meta' in sample else {}
                samples.append((audio, metadata))

        return samples


async def main():
    """Example usage"""
    logging.basicConfig(level=logging.INFO)

    logger.info("\n╔" + "=" * 68 + "╗")
    logger.info("║" + " " * 8 + "Music-to-Image Paper Implementation Example" + " " * 16 + "║")
    logger.info("╚" + "=" * 68 + "╝")

    # Create pipeline
    pipeline = MusicToImagePaperPipeline(
        sample_rate=16000,
        generation_mode="convergent",
        use_mel_spectrogram=False
    )

    # Load audio
    dataset_path = "./FA_project/dataset/label_data_with_16kHz_audio.npy"
    audio_loader = AudioLoaderFromNPY()

    try:
        audio, metadata = audio_loader.load_sample(dataset_path, sample_idx=0)

        logger.info(f"\n✓ Loaded audio: {audio.shape[0]} samples, {len(audio) / 16000:.2f}s duration")

        # Get LLM client
        from llm_client import get_recommended_client, create_llm_client
        try:
            llm_client = get_recommended_client()
            logger.info(f"✓ Using LLM: {llm_client.get_model_name()}")
        except:
            logger.info("Using mock LLM client for demonstration")
            llm_client = create_llm_client("mock")

        # Process
        results = await pipeline.process_audio(audio, metadata, llm_client)

        # Display visual prompt
        logger.info(f"\n🎨 VISUAL PROMPT FOR IMAGE GENERATION:")
        logger.info("=" * 60)
        logger.info(results["visual_prompt"][:500])
        logger.info("=" * 60)

        # Save results
        output_file = "pipeline_output_paper.json"
        with open(output_file, 'w') as f:
            # Make JSON serializable
            json_results = {
                "features": results["features"],
                "generation_mode": results["generation_mode"],
                "temperature": results["temperature"],
                "visual_prompt": results["visual_prompt"][:200]  # Preview
            }
            json.dump(json_results, f, indent=2)

        logger.info(f"\n✓ Results saved to {output_file}")

    except FileNotFoundError:
        logger.error(f"Dataset not found at {dataset_path}")
        logger.info("Expected at: ./FA_project/dataset/label_data_with_16kHz_audio.npy")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
