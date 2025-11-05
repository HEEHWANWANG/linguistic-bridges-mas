"""
Music-to-Image Pipeline - Main orchestration of the system

Based on "Exploring Real-Time Music-to-Image Systems" (Yang et al., 2407.05584v1)
Adapted to work without OpenAI subscription using Claude/local models
"""

import numpy as np
import logging
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from music_analyzer import MusicAnalyzer, MusicalFeatures
from prompt_builder import PromptBuilder
from mel_spectrogram_converter import MelSpectrogramConverter, MelSpectrogramConfig

logger = logging.getLogger(__name__)


class MusicToImagePipeline:
    """
    Main pipeline for converting music to images

    Flow:
    1. Load audio data
    2. Analyze music features (key, tempo, mood, etc.)
    3. Generate ABC notation
    4. Build GPT prompt for analysis
    5. Send to Claude/LLM for visual prompt generation
    6. Generate images using the visual prompt
    """

    def __init__(self,
                 sample_rate: int = 16000,
                 generation_mode: str = "convergent",
                 use_designer_agents: bool = True,
                 use_mel_spectrogram: bool = False,
                 mel_spectrogram_config: Optional[MelSpectrogramConfig] = None):
        """
        Initialize the pipeline

        Args:
            sample_rate: Sample rate of audio (Hz)
            generation_mode: "divergent" or "convergent"
            use_designer_agents: Whether to use multiple designer roles
            use_mel_spectrogram: Whether to convert audio to mel-spectrogram for LLM analysis
            mel_spectrogram_config: Configuration for mel-spectrogram conversion (uses defaults if None)
        """
        self.sample_rate = sample_rate
        self.generation_mode = generation_mode
        self.use_designer_agents = use_designer_agents
        self.use_mel_spectrogram = use_mel_spectrogram

        self.music_analyzer = MusicAnalyzer(sr=sample_rate)
        self.prompt_builder = PromptBuilder(generation_mode=generation_mode)

        # Initialize mel-spectrogram converter if enabled
        if self.use_mel_spectrogram:
            if mel_spectrogram_config is None:
                mel_spectrogram_config = MelSpectrogramConfig(sample_rate=sample_rate)
            self.mel_converter = MelSpectrogramConverter(mel_spectrogram_config)
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
        Process audio through the complete pipeline

        Args:
            audio_data: Audio waveform as numpy array (or mel-spectrogram if already converted)
            metadata: Optional metadata about the audio
            llm_client: LLM client for prompt analysis (e.g., Claude, Ollama, etc.)

        Returns:
            Dictionary with analysis results and generated prompts
        """
        self.logger.info("=" * 60)
        self.logger.info("🎵 Starting Music-to-Image Pipeline")
        self.logger.info("=" * 60)

        # Determine input type and convert if necessary
        mel_spectrogram_text = None
        audio_for_analysis = audio_data

        if self.use_mel_spectrogram and self.mel_converter:
            self.logger.info("\n0️⃣  Processing mel-spectrogram conversion...")
            input_type = self.mel_converter.detect_input_type(audio_data)

            if input_type == "waveform":
                # Convert audio waveform to mel-spectrogram
                self.logger.info("   Converting audio waveform to mel-spectrogram...")
                mel_spec = self.mel_converter.audio_to_mel_spectrogram(audio_data)
                mel_spectrogram_text = self.mel_converter.mel_spectrogram_to_text_representation(mel_spec)
                self.logger.info(f"   ✓ Mel-spectrogram created ({mel_spec.shape[0]} bands × {mel_spec.shape[1]} frames)")
            else:
                # Input is already mel-spectrogram
                self.logger.info("   Input is already mel-spectrogram, generating text representation...")
                mel_spectrogram_text = self.mel_converter.mel_spectrogram_to_text_representation(audio_data)
                # For feature analysis, we still need the original waveform if available
                if "audio_waveform" in metadata:
                    audio_for_analysis = metadata["audio_waveform"]
                else:
                    self.logger.warning("   ⚠️  No original waveform available for feature analysis")

        # Step 1: Analyze music features
        self.logger.info("\n1️⃣  Analyzing musical features...")
        features = self.music_analyzer.analyze_audio(audio_for_analysis)
        self.logger.info(f"   ✓ Extracted features: {features.overall_mood}")

        # Step 2: Generate ABC notation
        self.logger.info("\n2️⃣  Generating ABC notation...")
        abc_notation = features.to_abc_notation()
        self.logger.info(f"   ✓ ABC notation generated ({len(abc_notation)} chars)")

        # Step 3: Build GPT prompt (with optional mel-spectrogram)
        self.logger.info("\n3️⃣  Building GPT analysis prompt...")
        gpt_prompt = self.prompt_builder.build_gpt_prompt(
            features,
            abc_notation,
            style_guidance=metadata.get("style_guidance") if metadata else None,
            mel_spectrogram_text=mel_spectrogram_text,
            use_mel_spectrogram=self.use_mel_spectrogram
        )
        self.logger.info(f"   ✓ Prompt built ({len(gpt_prompt)} chars)")

        # Step 4: Get LLM analysis
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
            "gpt_prompt": gpt_prompt
        }

        # Include mel-spectrogram info if processed
        if mel_spectrogram_text:
            results["mel_spectrogram_text"] = mel_spectrogram_text
            results["mel_spectrogram_enabled"] = True
        else:
            results["mel_spectrogram_enabled"] = False

        if llm_client:
            self.logger.info("\n4️⃣  Sending to LLM for visual prompt generation...")
            try:
                gpt_response = await llm_client.analyze(gpt_prompt)
                visual_elements = self.prompt_builder.extract_visual_elements_from_gpt_response(gpt_response)
                results["visual_analysis"] = visual_elements
                self.logger.info("   ✓ LLM analysis completed")

                # Step 5: Build designer agent variations (if enabled)
                if self.use_designer_agents:
                    self.logger.info("\n5️⃣  Generating designer agent variations...")
                    designer_variations = await self._get_designer_variations(
                        features, llm_client
                    )
                    results["designer_variations"] = designer_variations
                    self.logger.info(f"   ✓ Generated {len(designer_variations)} designer perspectives")

                    # Step 6: Create final blended prompt
                    self.logger.info("\n6️⃣  Creating final image generation prompt...")
                    final_prompt = self.prompt_builder.create_final_image_prompt(
                        visual_elements,
                        designer_variations=list(designer_variations.values()),
                        use_consensus=True
                    )
                    results["final_image_prompt"] = final_prompt
                else:
                    # Use primary analysis directly
                    final_prompt = self.prompt_builder.create_final_image_prompt(
                        visual_elements,
                        use_consensus=False
                    )
                    results["final_image_prompt"] = final_prompt

                self.logger.info("   ✓ Final prompt created")
                self.logger.info(f"   Temperature: {self.prompt_builder.get_temperature()}")
                self.logger.info(f"   Mode: {self.generation_mode}")

            except Exception as e:
                self.logger.error(f"   ✗ LLM analysis failed: {e}")
                self.logger.info("   Falling back to direct feature-based prompt...")
                results["final_image_prompt"] = self.prompt_builder.create_final_image_prompt(
                    results["visual_analysis"] if "visual_analysis" in results else
                    self._create_fallback_visual_elements(features),
                    use_consensus=False
                )

        self.logger.info("\n" + "=" * 60)
        self.logger.info("✅ Pipeline completed successfully")
        self.logger.info("=" * 60)

        return results

    async def _get_designer_variations(self,
                                       features: MusicalFeatures,
                                       llm_client) -> Dict[str, str]:
        """
        Get variations from different designer roles

        Args:
            features: Musical features
            llm_client: LLM client for generating variations

        Returns:
            Dictionary with designer role variations
        """
        designer_roles = ["narrative", "mood", "style", "conceptual", "commercial"]
        variations = {}

        for role in designer_roles:
            try:
                role_prompt = self.prompt_builder.build_design_agent_prompt(features, role)
                role_response = await llm_client.analyze(role_prompt)
                variations[role] = role_response[:500]  # Truncate for brevity
                self.logger.info(f"   • {role.capitalize()} designer: ✓")
            except Exception as e:
                self.logger.warning(f"   • {role.capitalize()} designer failed: {e}")
                variations[role] = ""

        return variations

    def _create_fallback_visual_elements(self, features: MusicalFeatures) -> Dict[str, Any]:
        """
        Create visual elements directly from features without LLM (fallback)

        Args:
            features: Musical features

        Returns:
            Visual elements dictionary
        """
        color_map = {
            "C": "warm amber", "D": "golden yellow", "E": "bright yellow",
            "F": "soft bronze", "G": "emerald green", "A": "azure blue", "B": "deep indigo"
        }

        mood_colors = {
            "major": color_map.get(features.key_signature, "warm tones"),
            "minor": "cool tones" if features.tonality == "minor" else color_map.get(features.key_signature, "warm tones")
        }

        return {
            "visual_prompt": f"Musical visualization of {features.key_signature} {features.tonality} music with {features.overall_mood} mood",
            "color_palette": [mood_colors.get(features.tonality, "balanced colors")],
            "composition": f"{features.melody_contour} compositional flow with {features.harmonic_progression}",
            "mood": features.overall_mood,
            "temperature": self.prompt_builder.get_temperature()
        }


class AudioLoaderFromNPY:
    """Helper class to load audio from NPY files"""

    @staticmethod
    def load_sample(npy_path: str, sample_idx: int = 0) -> tuple:
        """
        Load a single audio sample from NPY dataset

        Args:
            npy_path: Path to NPY file
            sample_idx: Index of sample to load

        Returns:
            Tuple of (audio_data, metadata)
        """
        try:
            data = np.load(npy_path, allow_pickle=True)
            sample = data[sample_idx]

            audio = sample['audio']
            metadata = sample['audio_meta'] if 'audio_meta' in sample else {}

            return audio, metadata

        except Exception as e:
            logger.error(f"Failed to load audio from {npy_path}: {e}")
            raise

    @staticmethod
    def load_batch(npy_path: str, indices: List[int] = None) -> List[tuple]:
        """
        Load multiple audio samples

        Args:
            npy_path: Path to NPY file
            indices: List of indices to load (None = all)

        Returns:
            List of (audio_data, metadata) tuples
        """
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


def print_sample_output(results: Dict[str, Any]):
    """Pretty print pipeline results"""
    print("\n" + "=" * 70)
    print("📊 PIPELINE RESULTS")
    print("=" * 70)

    print("\n🎵 MUSICAL FEATURES:")
    for key, value in results.get("features", {}).items():
        print(f"   {key.replace('_', ' ').title()}: {value}")

    print("\n📝 ABC NOTATION (First 200 chars):")
    abc = results.get("abc_notation", "")
    print(f"   {abc[:200]}..." if len(abc) > 200 else f"   {abc}")

    if "visual_analysis" in results:
        print("\n🎨 VISUAL ANALYSIS:")
        visual = results["visual_analysis"]
        print(f"   Visual Prompt: {visual.get('visual_prompt', '')[:100]}...")
        print(f"   Color Palette: {', '.join(visual.get('color_palette', []))}")
        print(f"   Temperature: {visual.get('temperature', 'N/A')}")

    if "designer_variations" in results:
        print("\n👥 DESIGNER VARIATIONS:")
        for designer, variation in results["designer_variations"].items():
            print(f"   {designer.title()}: {variation[:80]}...")

    if "final_image_prompt" in results:
        print("\n🖼️  FINAL IMAGE PROMPT (First 300 chars):")
        prompt = results["final_image_prompt"]
        print(f"   {prompt[:300]}...")

    print("\n" + "=" * 70)
