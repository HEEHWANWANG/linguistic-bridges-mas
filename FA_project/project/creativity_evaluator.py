"""
Creativity Evaluator for Music-to-Image Visual Prompts

Implements AUT (Alternative Uses Test) and TTCT (Torrance Test of Creative Thinking)
metrics for evaluating the creativity of LLM-generated visual prompts from musical features.

Based on: Goes et al. (2023) - ICCC-2023 Paper
"""

import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import re
from collections import Counter


@dataclass
class CreativityMetrics:
    """Container for creativity evaluation results"""
    originality: float  # 1-5: How unique/novel is the prompt?
    elaboration: float  # 1-5: How detailed and rich is it?
    alignment: float    # 1-5: How well does it align with music?
    coherence: float    # 1-5: Do elements work together?
    overall: float      # 1-5: Weighted overall score

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            'originality': self.originality,
            'elaboration': self.elaboration,
            'alignment': self.alignment,
            'coherence': self.coherence,
            'overall': self.overall
        }


class OriginalityScorer:
    """
    Scores originality of visual prompts.

    Measures: How unique/novel is the prompt compared to typical descriptions?
    Scale: 1 (cliché) to 5 (highly original)
    """

    # Common clichéd associations for mood/tempo/key
    CLICHE_PHRASES = {
        # Mood-based clichés
        'sad': ['dark', 'gloomy', 'melancholic', 'sad', 'depressing', 'grey'],
        'happy': ['bright', 'cheerful', 'sunny', 'colorful', 'happy', 'joyful'],
        'energetic': ['dynamic', 'fast', 'quick', 'rapid', 'energetic', 'vibrant'],
        'calm': ['peaceful', 'serene', 'quiet', 'still', 'calm', 'tranquil'],

        # Key-based clichés
        'major': ['warm', 'bright', 'positive', 'light'],
        'minor': ['cool', 'dark', 'sad', 'melancholic'],

        # Tempo-based clichés
        'fast': ['energetic', 'dynamic', 'fast', 'rapid', 'quick'],
        'slow': ['slow', 'calm', 'peaceful', 'serene', 'quiet'],
    }

    # Sophisticated/unexpected associations (novel)
    NOVEL_WORDS = {
        'ethereal', 'iridescent', 'ephemeral', 'luminescent', 'crystalline',
        'refracted', 'cascading', 'undulating', 'diaphanous', 'mercurial',
        'resplendent', 'insouciant', 'oblique', 'baroque', 'liminal',
        'vertiginous', 'penumbral', 'opalescent', 'tenebrous', 'incandescent'
    }

    def score(self, prompt: str, musical_features: Dict[str, Any]) -> float:
        """
        Score originality of prompt.

        Args:
            prompt: The visual prompt text
            musical_features: Musical features dict with 'mood', 'key', 'tempo', etc.

        Returns:
            Originality score 1-5
        """
        words = set(prompt.lower().split())

        # Count clichéd phrases
        cliche_count = 0
        for category, phrases in self.CLICHE_PHRASES.items():
            cliche_count += sum(1 for phrase in phrases if phrase in prompt.lower())

        # Count novel words
        novel_count = sum(1 for word in words if word in self.NOVEL_WORDS)

        # Calculate ratio
        total_words = len(words)
        if total_words == 0:
            return 1.0

        cliche_ratio = cliche_count / total_words
        novel_ratio = novel_count / total_words

        # Score: 1-5 scale
        # Low clichés + high novel words = high originality
        score = 1.0 + (novel_ratio * 2.0) - (cliche_ratio * 1.5)
        return max(1.0, min(5.0, score))


class ElaborationScorer:
    """
    Scores elaboration/detail level of prompts.

    Measures: How detailed, rich, and specific is the description?
    Scale: 1 (generic) to 5 (richly detailed)
    """

    # Elaboration indicators
    SENSORY_WORDS = {
        'visual': ['shimmer', 'gleam', 'glow', 'reflect', 'shadow', 'light', 'color', 'hue'],
        'tactile': ['smooth', 'rough', 'soft', 'hard', 'texture', 'surface'],
        'auditory': ['sound', 'echo', 'resonance', 'vibration', 'frequency'],
        'olfactory': ['scent', 'aroma', 'fragrance', 'smell'],
        'kinetic': ['flow', 'movement', 'motion', 'drift', 'cascade', 'surge'],
    }

    DETAIL_WORDS = {
        'intricate', 'detailed', 'complex', 'layered', 'multifaceted', 'ornate',
        'delicate', 'specific', 'precise', 'nuanced', 'sophisticated'
    }

    def score(self, prompt: str) -> float:
        """
        Score elaboration of prompt.

        Args:
            prompt: The visual prompt text

        Returns:
            Elaboration score 1-5
        """
        words = prompt.lower().split()
        unique_words = set(words)

        # Count sensory descriptors
        sensory_count = 0
        for sense_words in self.SENSORY_WORDS.values():
            sensory_count += sum(1 for word in unique_words if word in sense_words)

        # Count detail indicators
        detail_count = sum(1 for word in unique_words if word in self.DETAIL_WORDS)

        # Measure vocabulary richness
        vocab_richness = len(unique_words) / max(len(words), 1)

        # Calculate score
        # More senses + detail words + vocabulary diversity = higher elaboration
        score = 1.0 + (sensory_count * 0.4) + (detail_count * 0.3) + (vocab_richness * 2.0)

        return max(1.0, min(5.0, score))


class AlignmentScorer:
    """
    Scores alignment between prompt and music features.

    Measures: How well does the visual prompt reflect the musical features?
    Scale: 1 (poor fit) to 5 (excellent alignment)
    """

    # Tempo → Motion mapping
    TEMPO_MOTION = {
        'fast': ['dynamic', 'energetic', 'rapid', 'quick', 'swift', 'rushing', 'vibrant'],
        'slow': ['gentle', 'calm', 'peaceful', 'serene', 'still', 'flowing', 'drifting'],
        'moderate': ['balanced', 'steady', 'moderate', 'paced', 'rhythmic'],
    }

    # Key/Tonality → Color mapping
    TONALITY_COLOR = {
        'major': ['warm', 'bright', 'golden', 'sunny', 'radiant', 'light', 'vibrant'],
        'minor': ['cool', 'deep', 'dark', 'shadowy', 'muted', 'introspective', 'subtle'],
    }

    # Melody → Movement mapping
    MELODY_MOVEMENT = {
        'ascending': ['rising', 'upward', 'climbing', 'elevating', 'ascending', 'growth'],
        'descending': ['falling', 'descending', 'dropping', 'settling', 'grounding'],
        'stable': ['still', 'centered', 'stable', 'balanced', 'steady', 'fixed'],
    }

    # Dynamics → Intensity mapping
    DYNAMICS_INTENSITY = {
        'soft': ['gentle', 'subtle', 'delicate', 'whisper', 'soft', 'quiet'],
        'intense': ['bold', 'strong', 'powerful', 'dramatic', 'intense', 'vivid'],
    }

    def score(self, prompt: str, musical_features: Dict[str, Any]) -> float:
        """
        Score alignment between prompt and music features.

        Args:
            prompt: The visual prompt text
            musical_features: Dict with keys: tempo, tonality, melody_contour,
                            dynamic_intensity

        Returns:
            Alignment score 1-5
        """
        words = set(prompt.lower().split())
        alignment_score = 0
        criteria_count = 0

        # Check tempo alignment
        if 'tempo' in musical_features:
            # Convert to float for numeric comparison
            try:
                tempo_value = float(musical_features['tempo'])
            except (ValueError, TypeError):
                tempo_value = 100  # Default if conversion fails

            if tempo_value > 100:
                tempo_key = 'fast'
            elif tempo_value < 80:
                tempo_key = 'slow'
            else:
                tempo_key = 'moderate'

            matches = sum(1 for word in words if word in self.TEMPO_MOTION[tempo_key])
            alignment_score += matches
            criteria_count += 1

        # Check tonality/color alignment
        if 'tonality' in musical_features:
            tonality = musical_features['tonality'].lower()
            if tonality in self.TONALITY_COLOR:
                matches = sum(1 for word in words
                            if word in self.TONALITY_COLOR[tonality])
                alignment_score += matches * 0.5
                criteria_count += 1

        # Check melody alignment
        if 'melody_contour' in musical_features:
            melody = musical_features['melody_contour'].lower()
            if melody in self.MELODY_MOVEMENT:
                matches = sum(1 for word in words
                            if word in self.MELODY_MOVEMENT[melody])
                alignment_score += matches * 0.5
                criteria_count += 1

        # Check dynamics alignment
        if 'dynamic_intensity' in musical_features:
            dynamics = musical_features['dynamic_intensity'].lower()
            if 'soft' in dynamics:
                dyn_key = 'soft'
            elif 'intense' in dynamics:
                dyn_key = 'intense'
            else:
                dyn_key = None

            if dyn_key:
                matches = sum(1 for word in words
                            if word in self.DYNAMICS_INTENSITY[dyn_key])
                alignment_score += matches * 0.5
                criteria_count += 1

        # Calculate normalized score (1-5)
        if criteria_count == 0:
            return 3.0  # Neutral if no features available

        avg_alignment = alignment_score / criteria_count
        score = 1.0 + (avg_alignment * 0.8)

        return max(1.0, min(5.0, score))


class CoherenceScorer:
    """
    Scores coherence of visual prompt.

    Measures: Do all elements work together? Is there semantic unity?
    Scale: 1 (disconnected) to 5 (highly coherent)
    """

    def score(self, prompt: str) -> float:
        """
        Score coherence of prompt.

        Args:
            prompt: The visual prompt text

        Returns:
            Coherence score 1-5
        """
        sentences = [s.strip() for s in prompt.split('.') if s.strip()]

        if len(sentences) == 0:
            return 1.0

        # Score based on structural coherence
        scores = []

        # 1. Sentence complexity (longer sentences often more coherent)
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 0:
                # Longer, more complex sentences = more coherent
                complexity = min(len(words) / 15.0, 1.0)
                scores.append(0.5 + (complexity * 1.5))

        # 2. Presence of connecting words/phrases
        connecting_words = {
            'and', 'with', 'where', 'creating', 'filled', 'adorned', 'composed',
            'intertwined', 'woven', 'blended', 'merged', 'connected', 'linked'
        }

        connection_count = sum(
            1 for word in prompt.lower().split()
            if word.strip('.,;:') in connecting_words
        )

        connection_score = min(connection_count / 5.0, 1.0) * 2.0 + 1.0

        # 3. Presence of subject/object relationships
        visual_verbs = {
            'shimmer', 'glow', 'flow', 'cascade', 'float', 'drift', 'swirl',
            'dance', 'blend', 'merge', 'dissolve', 'transform', 'emerge'
        }

        verb_count = sum(
            1 for word in prompt.lower().split()
            if word.strip('.,;:') in visual_verbs
        )

        verb_score = min(verb_count / 3.0, 1.0) * 2.0 + 1.0

        # Combine scores
        all_scores = scores + [connection_score, verb_score]
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 1.0

        return max(1.0, min(5.0, avg_score))


class MusicToImageCreativityEvaluator:
    """
    Main evaluator for music-to-image prompt creativity.

    Uses AUT and TTCT-inspired metrics:
    - Originality: How novel/unique is the prompt?
    - Elaboration: How detailed and rich?
    - Alignment: How well does it reflect music?
    - Coherence: Do elements work together?
    """

    def __init__(self):
        self.originality_scorer = OriginalityScorer()
        self.elaboration_scorer = ElaborationScorer()
        self.alignment_scorer = AlignmentScorer()
        self.coherence_scorer = CoherenceScorer()

        # Weights for overall score (sum to 1.0)
        self.weights = {
            'originality': 0.30,
            'elaboration': 0.25,
            'alignment': 0.25,
            'coherence': 0.20,
        }

    def evaluate(self,
                 prompt: str,
                 musical_features: Dict[str, Any]) -> CreativityMetrics:
        """
        Evaluate creativity of a visual prompt.

        Args:
            prompt: The visual prompt text
            musical_features: Dict with musical feature values

        Returns:
            CreativityMetrics object with individual and overall scores
        """
        # Score each dimension
        originality = self.originality_scorer.score(prompt, musical_features)
        elaboration = self.elaboration_scorer.score(prompt)
        alignment = self.alignment_scorer.score(prompt, musical_features)
        coherence = self.coherence_scorer.score(prompt)

        # Calculate weighted overall score
        overall = (
            self.weights['originality'] * originality +
            self.weights['elaboration'] * elaboration +
            self.weights['alignment'] * alignment +
            self.weights['coherence'] * coherence
        )

        return CreativityMetrics(
            originality=round(originality, 2),
            elaboration=round(elaboration, 2),
            alignment=round(alignment, 2),
            coherence=round(coherence, 2),
            overall=round(overall, 2)
        )

    async def evaluate_with_llm(self,
                               prompt: str,
                               musical_features: Dict[str, Any],
                               llm_client) -> CreativityMetrics:
        """
        Evaluate creativity using LLM-based scoring (GPT-4 style evaluation).

        This provides human-like evaluation but requires LLM API access.

        Args:
            prompt: The visual prompt text
            musical_features: Dict with musical feature values
            llm_client: LLM client (Claude/Ollama)

        Returns:
            CreativityMetrics object
        """
        # Build evaluation prompt
        eval_prompt = self._build_llm_eval_prompt(prompt, musical_features)

        # Get LLM evaluation
        response = await llm_client.analyze(eval_prompt)

        # Parse response to extract scores
        metrics = self._parse_llm_response(response)

        return metrics

    def _build_llm_eval_prompt(self,
                              prompt: str,
                              musical_features: Dict[str, Any]) -> str:
        """Build LLM prompt for creativity evaluation."""

        features_str = "\n".join(
            f"- {k.replace('_', ' ').title()}: {v}"
            for k, v in musical_features.items()
        )

        return f"""You are evaluating the creativity of a visual prompt generated from musical analysis.

EVALUATION CRITERIA (Rate 1-5 for each):

1. ORIGINALITY (1-5):
   - 1 = Cliché, common associations
   - 3 = Moderate creativity
   - 5 = Highly original, surprising yet fitting

2. ELABORATION (1-5):
   - 1 = Generic, sparse
   - 3 = Moderate detail
   - 5 = Rich, layered, specific

3. SEMANTIC ALIGNMENT (1-5):
   - 1 = Poor fit with music
   - 3 = Reasonable alignment
   - 5 = Excellent alignment

4. COHERENCE (1-5):
   - 1 = Disconnected elements
   - 3 = Generally coherent
   - 5 = Highly unified

MUSICAL FEATURES:
{features_str}

VISUAL PROMPT:
"{prompt}"

Provide scores in this exact format:
ORIGINALITY: [number 1-5]
ELABORATION: [number 1-5]
ALIGNMENT: [number 1-5]
COHERENCE: [number 1-5]
OVERALL: [number 1-5]"""

    def _parse_llm_response(self, response: str) -> CreativityMetrics:
        """Parse LLM response to extract scores."""

        # Extract numbers from response
        pattern = r'(\w+):\s*(\d(?:\.\d)?)'
        matches = re.findall(pattern, response, re.IGNORECASE)

        scores = {}
        for key, value in matches:
            key_lower = key.lower()
            if key_lower in ['originality', 'elaboration', 'alignment', 'coherence', 'overall']:
                scores[key_lower] = float(value)

        # Return with defaults if parsing fails
        return CreativityMetrics(
            originality=scores.get('originality', 3.0),
            elaboration=scores.get('elaboration', 3.0),
            alignment=scores.get('alignment', 3.0),
            coherence=scores.get('coherence', 3.0),
            overall=scores.get('overall', 3.0)
        )


# Example usage
if __name__ == "__main__":
    evaluator = MusicToImageCreativityEvaluator()

    # Test prompt
    test_prompt = """A rhythmic sunrise breaking through layered golden glass sculptures,
    each refracting light in unexpected ways, creating an intricate dance of shadows
    and warmth. The composition flows upward with ethereal grace, as if the music
    itself is painting brushstrokes of iridescent color across crystalline surfaces."""

    test_features = {
        'tempo': 125,
        'key_signature': 'C',
        'tonality': 'major',
        'mood': 'happy',
        'melody_contour': 'ascending',
        'dynamic_intensity': 'intense'
    }

    # Evaluate
    metrics = evaluator.evaluate(test_prompt, test_features)

    # Display results
    print("Creativity Evaluation Results")
    print("=" * 40)
    print(f"Originality:  {metrics.originality}/5")
    print(f"Elaboration:  {metrics.elaboration}/5")
    print(f"Alignment:    {metrics.alignment}/5")
    print(f"Coherence:    {metrics.coherence}/5")
    print("-" * 40)
    print(f"Overall Score: {metrics.overall}/5")
    print("=" * 40)
