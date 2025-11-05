"""
Prompt Builder - Generates visual prompts from musical features using ABC notation

Strictly follows "Exploring Real-Time Music-to-Image Systems" (Yang et al., 2407.05584v1)
Implementation focused on replicating paper's framework without multi-agent extensions.
"""

import logging
from typing import Dict, Any
from music_analyzer import MusicalFeatures

logger = logging.getLogger(__name__)


class PromptBuilderPaper:
    """Builds visual prompts from musical features following the paper's approach"""

    def __init__(self, generation_mode: str = "convergent"):
        """
        Initialize prompt builder

        Args:
            generation_mode: "divergent" (0.8 temperature) or "convergent" (0.4 temperature)
        """
        self.generation_mode = generation_mode
        self.temperature = 0.8 if generation_mode == "divergent" else 0.4
        self.logger = logging.getLogger(__name__)

    def build_gpt_prompt(self,
                        features: MusicalFeatures,
                        abc_notation: str,
                        style_guidance: str = None,
                        mel_spectrogram_text: str = None,
                        use_mel_spectrogram: bool = False) -> str:
        """
        Build prompt for LLM following the paper's approach.

        The paper's framework:
        1. Extracts musical features from MIDI/audio
        2. Converts to ABC notation
        3. Sends to GPT-4 with task to map music features to visual concepts
        4. GPT-4 generates visual prompt for SDXL

        Args:
            features: MusicalFeatures object
            abc_notation: ABC notation representation
            style_guidance: Optional style guidance
            mel_spectrogram_text: Optional mel-spectrogram analysis
            use_mel_spectrogram: Whether to include mel-spectrogram

        Returns:
            Prompt for LLM analysis
        """

        # Build input section with optional mel-spectrogram
        input_section = ""
        if use_mel_spectrogram and mel_spectrogram_text:
            input_section = f"""MEL-SPECTROGRAM ANALYSIS:
---
{mel_spectrogram_text}
---

ADDITIONALLY, HERE IS THE ABC NOTATION REPRESENTATION:
---
{abc_notation}
---"""
        else:
            input_section = f"""ABC NOTATION ANALYSIS:
---
{abc_notation}
---"""

        # Paper's prompt structure: music features → visual mapping
        prompt = f"""You are an expert music-to-visual translator. Your task is to analyze the provided music representation and generate a detailed visual prompt for image generation (SDXL).

{input_section}

EXTRACTED MUSICAL FEATURES:
- Key Signature: {features.key_signature} {features.tonality}
- Tempo: {features.tempo:.0f} BPM
- Time Signature: {features.time_signature}
- Melody Contour: {features.melody_contour}
- Harmonic Progression: {features.harmonic_progression}
- Dynamic Intensity: {features.dynamic_intensity}
- Overall Mood: {features.overall_mood}

{("STYLE GUIDANCE:" + chr(10) + style_guidance) if style_guidance else ""}

MAPPING MUSIC TO VISUAL ELEMENTS:
1. Tempo maps to visual motion and pacing:
   - Fast tempo (>120 BPM) → Dynamic, energetic, rapid movements
   - Moderate tempo (80-120 BPM) → Balanced, moderate pacing
   - Slow tempo (<80 BPM) → Calm, serene, flowing movements

2. Key and tonality map to color palette:
   - Major key → Warm, bright, positive colors
   - Minor key → Cool, dark, introspective colors

3. Melody contour maps to compositional flow:
   - Ascending → Upward movement, growth, elevation
   - Descending → Downward movement, grounding, settling
   - Stable → Stillness, centeredness, balance

4. Harmonic progression maps to visual complexity:
   - Simple → Clean, minimal composition
   - Complex → Layered, intricate, rich details

5. Dynamic intensity maps to contrast and saturation:
   - Intense → High contrast, saturated colors
   - Soft → Subtle, muted, low contrast

YOUR TASK:
Generate a detailed, vivid image prompt suitable for SDXL image generation. The prompt should:
- Clearly describe visual style and composition
- Include specific color suggestions based on music
- Describe atmosphere and mood
- Use descriptive adjectives that convey the emotional essence
- Be concise but detailed (150-300 words)

Output ONLY the visual prompt text, nothing else."""

        return prompt

    def extract_visual_prompt_from_response(self, response: str) -> str:
        """
        Extract visual prompt from LLM response.

        The response should be the visual prompt itself (following paper's simple approach).

        Args:
            response: LLM response text

        Returns:
            Cleaned visual prompt
        """
        # The response IS the prompt (paper's simple approach)
        return response.strip()

    def get_temperature(self) -> float:
        """Get the temperature setting for the generation mode"""
        return self.temperature
