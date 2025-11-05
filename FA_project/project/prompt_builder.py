"""
Prompt Builder - Generates visual prompts from musical features using ABC notation

Based on "Exploring Real-Time Music-to-Image Systems" (Yang et al., 2407.05584v1)
Uses ABC notation format for music analysis, following the paper's approach
"""

import logging
from typing import Dict, Any, List
from music_analyzer import MusicalFeatures

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builds visual generation prompts from musical features using ABC notation"""

    def __init__(self, generation_mode: str = "convergent"):
        """
        Initialize prompt builder

        Args:
            generation_mode: "divergent" (0.8 temperature, high randomness) or
                           "convergent" (0.4 temperature, low randomness)
        """
        self.generation_mode = generation_mode
        self.temperature = 0.8 if generation_mode == "divergent" else 0.4
        self.logger = logging.getLogger(__name__)

    def build_gpt_prompt(self, features: MusicalFeatures, abc_notation: str, style_guidance: str = None, mel_spectrogram_text: str = None, use_mel_spectrogram: bool = False) -> str:
        """
        Build a comprehensive prompt for GPT-4 to analyze music and generate visual descriptors

        Args:
            features: MusicalFeatures object from music analyzer
            abc_notation: ABC notation representation of the music
            style_guidance: Optional specific style guidance
            mel_spectrogram_text: Optional mel-spectrogram text representation
            use_mel_spectrogram: Whether to include mel-spectrogram in analysis

        Returns:
            A well-structured prompt for GPT-4
        """

        # Build input section based on whether mel-spectrogram is included
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

        prompt = f"""You are an expert music-to-visual translator who understands the deep connections between musical and visual elements.

Analyze the following music representation and create a detailed visual prompt for image generation.

{input_section}

EXTRACTED MUSICAL FEATURES:
- Key Signature: {features.key_signature} {features.tonality}
- Tempo: {features.tempo:.0f} BPM
- Time Signature: {features.time_signature}
- Melody Contour: {features.melody_contour}
- Harmonic Progression: {features.harmonic_progression}
- Dynamic Intensity: {features.dynamic_intensity}
- Overall Mood: {features.overall_mood}

{"STYLE GUIDANCE:" + chr(10) + style_guidance if style_guidance else ""}

YOUR TASK:
1. Analyze the musical characteristics and their emotional implications
2. Map musical features to visual characteristics:
   - Tempo → Visual motion and pacing (fast tempo = dynamic/energetic visuals)
   - Key & Tonality → Color palette (major key = warm/bright colors; minor key = cool/dark colors)
   - Melody Contour → Compositional flow (ascending = moving up/outward; descending = grounded/inward)
   - Harmonic Complexity → Visual complexity (complex harmonies = layered/intricate visuals)
   - Dynamic Intensity → Contrast and saturation (intense = high contrast/saturated; soft = subtle/muted)

3. Create a vivid, detailed visual prompt that captures the essence of this music

OUTPUT FORMAT:
Provide ONLY a detailed image prompt (no explanations, no JSON, just pure prompt text):

Visual Prompt:
[Your detailed visual description that could be used for image generation]

Color Palette:
[Key colors and their justification based on the music]

Compositional Elements:
[Visual composition, perspective, and spatial arrangement]

Mood & Atmosphere:
[The emotional and atmospheric quality of the envisioned image]
"""

        return prompt

    def build_design_agent_prompt(self, features: MusicalFeatures, designer_role: str) -> str:
        """
        Build a prompt for a specialized Designer Agent role

        Args:
            features: MusicalFeatures object
            designer_role: One of ["narrative", "mood", "style", "conceptual", "commercial"]

        Returns:
            A role-specific prompt
        """

        role_prompts = {
            "narrative": self._build_narrative_prompt(features),
            "mood": self._build_mood_prompt(features),
            "style": self._build_style_prompt(features),
            "conceptual": self._build_conceptual_prompt(features),
            "commercial": self._build_commercial_prompt(features)
        }

        return role_prompts.get(designer_role, self._build_narrative_prompt(features))

    def _build_narrative_prompt(self, features: MusicalFeatures) -> str:
        """Build prompt for Narrative Designer - focuses on story arc and emotional journey"""
        return f"""You are a Narrative Designer specializing in translating musical stories to visual narratives.

Analyze this music's emotional arc and create a visual narrative:
- Key: {features.key_signature} {features.tonality}
- Tempo: {features.tempo:.0f} BPM
- Mood: {features.overall_mood}
- Contour: {features.melody_contour}

Create a visual description that tells a story with:
1. An emotional journey or narrative arc
2. Characters or subjects that evolve with the music
3. Scene progression that mirrors the musical structure
4. Symbolic elements that represent the musical progression

Provide ONLY the visual narrative description."""

    def _build_mood_prompt(self, features: MusicalFeatures) -> str:
        """Build prompt for Mood Designer - focuses on emotional tone and colors"""
        return f"""You are a Mood Designer specializing in translating emotional music to visual aesthetics.

Analyze this music's emotional qualities:
- Overall Mood: {features.overall_mood}
- Dynamic Intensity: {features.dynamic_intensity}
- Tonality: {features.tonality}
- Tempo: {features.tempo:.0f} BPM

Create a visual description that emphasizes:
1. Color psychology matching the emotional tone
2. Lighting that conveys the mood (bright/dim, warm/cool, harsh/soft)
3. Visual texture and surface qualities that evoke the feeling
4. Atmospheric elements that reinforce the emotional state

Provide ONLY the mood-focused visual description."""

    def _build_style_prompt(self, features: MusicalFeatures) -> str:
        """Build prompt for Style Designer - focuses on artistic direction and visual language"""
        return f"""You are a Style Designer specializing in artistic visual direction.

Based on this music's characteristics:
- Harmonic Progression: {features.harmonic_progression}
- Melody Contour: {features.melody_contour}
- Tempo: {features.tempo:.0f} BPM
- Overall Mood: {features.overall_mood}

Create a visual description that specifies:
1. Artistic medium and technique (oil painting, digital, watercolor, surreal, abstract, photorealistic, etc.)
2. Visual style reference points (e.g., "inspired by impressionism" or "cyberpunk aesthetic")
3. Compositional approach (symmetrical, dynamic, minimalist, chaotic, etc.)
4. Visual language and visual metaphors specific to this artistic direction

Provide ONLY the style-focused visual description."""

    def _build_conceptual_prompt(self, features: MusicalFeatures) -> str:
        """Build prompt for Conceptual Designer - focuses on abstract concepts and symbolism"""
        return f"""You are a Conceptual Designer specializing in translating abstract musical concepts to visual metaphors.

Based on this music's conceptual qualities:
- Key: {features.key_signature} {features.tonality}
- Harmonic Complexity: {features.harmonic_progression}
- Dynamic Range: {features.dynamic_intensity}
- Emotional Essence: {features.overall_mood}

Create a visual description using:
1. Visual metaphors for abstract musical concepts
2. Symbolic representations of harmonic and melodic ideas
3. Conceptual bridges between sound and sight
4. Philosophical or thematic visual interpretations

Provide ONLY the concept-focused visual description."""

    def _build_commercial_prompt(self, features: MusicalFeatures) -> str:
        """Build prompt for Commercial Designer - focuses on audience appeal and marketability"""
        return f"""You are a Commercial Designer balancing artistic integrity with audience appeal.

Based on this music's commercial appeal:
- Mood: {features.overall_mood}
- Tempo/Energy: {features.tempo:.0f} BPM
- Tonality: {features.tonality}
- Intensity: {features.dynamic_intensity}

Create a visual description that:
1. Has immediate visual appeal to a broad audience
2. Is compelling as an album cover or thumbnail
3. Balances artistic quality with commercial viability
4. Creates an emotional connection that drives engagement
5. Is technically feasible for professional image generation

Provide ONLY the commercial-focused visual description."""

    def extract_visual_elements_from_gpt_response(self, gpt_response: str) -> Dict[str, Any]:
        """
        Parse GPT response to extract structured visual elements

        Args:
            gpt_response: Response from GPT-4

        Returns:
            Dictionary with extracted visual elements
        """
        elements = {
            "visual_prompt": "",
            "color_palette": [],
            "composition": "",
            "mood": "",
            "temperature": self.temperature
        }

        # Parse response sections
        sections = gpt_response.split("\n")
        current_section = None

        for line in sections:
            line = line.strip()

            if "Visual Prompt:" in line:
                current_section = "visual_prompt"
                continue
            elif "Color Palette:" in line:
                current_section = "color_palette"
                continue
            elif "Compositional Elements:" in line:
                current_section = "composition"
                continue
            elif "Mood & Atmosphere:" in line:
                current_section = "mood"
                continue

            if current_section and line:
                if current_section == "color_palette":
                    elements["color_palette"].append(line)
                else:
                    elements[current_section] += " " + line

        # Clean up
        for key in ["visual_prompt", "composition", "mood"]:
            elements[key] = elements[key].strip()

        return elements

    def create_final_image_prompt(self,
                                  gpt_analysis: Dict[str, Any],
                                  designer_variations: List[str] = None,
                                  use_consensus: bool = True) -> str:
        """
        Create final image generation prompt

        Args:
            gpt_analysis: Analyzed features from GPT
            designer_variations: Optional variations from different designer roles
            use_consensus: Whether to blend for consensus or preserve diversity

        Returns:
            Final prompt for image generation model
        """

        if use_consensus and designer_variations:
            # Blend variations for consensus
            combined_prompt = f"""
PRIMARY VISUAL DIRECTION:
{gpt_analysis.get('visual_prompt', '')}

DESIGN TEAM INPUT:
{chr(10).join([f"- {var}" for var in designer_variations])}

COLOR & AESTHETIC:
{chr(10).join(gpt_analysis.get('color_palette', []))}

COMPOSITION & MOOD:
{gpt_analysis.get('composition', '')}
{gpt_analysis.get('mood', '')}

GENERATION PARAMETERS:
- Temperature: {self.temperature}
- Mode: {self.generation_mode}
"""
        else:
            # Use primary analysis
            combined_prompt = f"""
{gpt_analysis.get('visual_prompt', '')}

COLORS: {', '.join(gpt_analysis.get('color_palette', []))}
COMPOSITION: {gpt_analysis.get('composition', '')}
MOOD: {gpt_analysis.get('mood', '')}
"""

        return combined_prompt.strip()

    def get_temperature(self) -> float:
        """Get the temperature setting for the generation mode"""
        return self.temperature
