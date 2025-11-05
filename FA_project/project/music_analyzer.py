"""
Music Analyzer - Extracts features from audio and generates ABC notation

Based on "Exploring Real-Time Music-to-Image Systems" (Yang et al., 2407.05584v1)
Adapted for direct audio analysis without MIDI (using librosa)
"""

import numpy as np
import librosa
import logging
from typing import Dict, Any, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MusicalFeatures:
    """Container for extracted musical features"""
    key_signature: str
    tonality: str  # major or minor
    tempo: float
    time_signature: str
    melody_contour: str
    harmonic_progression: str
    dynamic_intensity: str
    overall_mood: str

    def to_abc_notation(self) -> str:
        """
        Convert features to ABC notation format
        ABC notation is a text-based music format that can be easily processed by LLMs

        Format:
        X:1 (reference number)
        T: (title)
        M: (meter/time signature)
        L: (unit note length)
        Q: (tempo)
        K: (key signature)
        ...notes...
        """
        # Map extracted features to ABC notation
        abc = f"""X:1
T:Generated Song
M:{self.time_signature}
L:1/8
Q:{int(self.tempo)}
K:{self._format_key()}{" " if self.tonality == "major" else "m"}
"""
        # Add simplified melody representation
        # In practice, this would be more detailed based on pitch analysis
        abc += self._generate_melody_representation()

        return abc

    def _format_key(self) -> str:
        """Format key signature for ABC notation"""
        key_map = {
            'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'A': 'A', 'B': 'B',
            'C#': '^C', 'D#': '^D', 'E#': '^E', 'F#': '^F', 'G#': '^G', 'A#': '^A', 'B#': '^B',
            'Cb': '_C', 'Db': '_D', 'Eb': '_E', 'Fb': '_F', 'Gb': '_G', 'Ab': '_A', 'Bb': '_B'
        }
        return key_map.get(self.key_signature, 'C')

    def _generate_melody_representation(self) -> str:
        """Generate simplified melody representation"""
        # This is a placeholder - in production would use actual pitch analysis
        contour_map = {
            'ascending': 'C2 D2 E2 F2 G2',
            'descending': 'G2 F2 E2 D2 C2',
            'stable': 'C4 C4 C4 C4',
            'mixed': 'C2 E2 D2 F2 G2'
        }
        return contour_map.get(self.melody_contour, 'C2 D2 E2') + ' |'


class MusicAnalyzer:
    """Analyzes audio files and extracts musical features for prompt generation"""

    def __init__(self, sr: int = 16000):
        """
        Initialize music analyzer

        Args:
            sr: Sample rate (Hz)
        """
        self.sr = sr
        self.logger = logging.getLogger(__name__)

    def analyze_audio(self, audio_data: np.ndarray) -> MusicalFeatures:
        """
        Extract musical features from audio data

        Args:
            audio_data: Audio waveform as numpy array

        Returns:
            MusicalFeatures object containing extracted features
        """
        # Normalize audio
        if np.max(np.abs(audio_data)) > 0:
            audio_normalized = audio_data / np.max(np.abs(audio_data))
        else:
            audio_normalized = audio_data

        # Extract features
        tempo, beats = self._extract_tempo(audio_normalized)
        key = self._extract_key(audio_normalized)
        tonality = self._extract_tonality(audio_normalized)
        melody_contour = self._extract_melody_contour(audio_normalized)
        harmonic_progression = self._extract_harmonic_progression(audio_normalized)
        dynamic_intensity = self._extract_dynamic_intensity(audio_normalized)
        mood = self._infer_mood(tempo, key, tonality, dynamic_intensity)

        features = MusicalFeatures(
            key_signature=key,
            tonality=tonality,
            tempo=tempo,
            time_signature=self._infer_time_signature(beats),
            melody_contour=melody_contour,
            harmonic_progression=harmonic_progression,
            dynamic_intensity=dynamic_intensity,
            overall_mood=mood
        )

        self.logger.info(f"Extracted features - Key: {key}, Tempo: {tempo:.1f} BPM, Mood: {mood}")
        return features

    def _extract_tempo(self, audio: np.ndarray) -> tuple:
        """Extract tempo (BPM) and beat frames"""
        onset_env = librosa.onset.onset_strength(y=audio, sr=self.sr)

        # tempogram API: use y parameter instead of onset_env (librosa 0.10+)
        try:
            tempogram = librosa.feature.tempogram(y=audio, sr=self.sr)
        except TypeError:
            # Fallback for older librosa versions
            tempogram = librosa.feature.tempogram(onset_env=onset_env, sr=self.sr)

        # Estimate tempo (compatible with both old and new librosa)
        try:
            tempo = librosa.feature.tempo(y=audio, sr=self.sr)[0]
        except TypeError:
            tempo = librosa.feature.tempo(onset_env=onset_env, sr=self.sr)[0]

        # Detect beats
        try:
            frames = librosa.beat.beat_track(y=audio, sr=self.sr)[1]
        except TypeError:
            frames = librosa.beat.beat_track(onset_env=onset_env, sr=self.sr)[1]

        return tempo, frames

    def _extract_key(self, audio: np.ndarray) -> str:
        """Extract key signature using chroma features"""
        chroma = librosa.feature.chroma_cqt(y=audio, sr=self.sr)
        chroma_mean = np.mean(chroma, axis=1)

        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key_idx = np.argmax(chroma_mean)

        return note_names[key_idx]

    def _extract_tonality(self, audio: np.ndarray) -> str:
        """Determine major or minor tonality"""
        # Use zero-crossing rate and spectral features as proxy
        zcr = librosa.feature.zero_crossing_rate(audio)[0]
        zcr_mean = np.mean(zcr)

        # Higher zero-crossing rate often correlates with minor keys
        # This is a simplified heuristic
        if zcr_mean > np.median(zcr):
            return "minor"
        else:
            return "major"

    def _extract_melody_contour(self, audio: np.ndarray) -> str:
        """Extract overall melodic contour"""
        # Use spectral centroid to infer contour direction
        spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=self.sr)[0]

        # Split into chunks and compare
        chunk_size = len(spectral_centroid) // 3
        if chunk_size > 0:
            first_chunk = np.mean(spectral_centroid[:chunk_size])
            middle_chunk = np.mean(spectral_centroid[chunk_size:2*chunk_size])
            last_chunk = np.mean(spectral_centroid[2*chunk_size:])

            if last_chunk > first_chunk:
                return "ascending"
            elif last_chunk < first_chunk:
                return "descending"
            else:
                return "stable" if abs(last_chunk - first_chunk) < 500 else "mixed"

        return "stable"

    def _extract_harmonic_progression(self, audio: np.ndarray) -> str:
        """Infer harmonic progression from spectral features"""
        # Use MFCC to infer harmonic complexity
        mfcc = librosa.feature.mfcc(y=audio, sr=self.sr, n_mfcc=13)
        mfcc_variance = np.var(mfcc, axis=1)
        harmonic_complexity = np.mean(mfcc_variance)

        if harmonic_complexity > 0.8:
            return "complex_progression"
        elif harmonic_complexity > 0.4:
            return "moderate_progression"
        else:
            return "simple_progression"

    def _extract_dynamic_intensity(self, audio: np.ndarray) -> str:
        """Extract dynamic intensity (loudness and variation)"""
        rms = librosa.feature.rms(y=audio)[0]
        rms_mean = np.mean(rms)
        rms_std = np.std(rms)

        # Combine mean loudness and dynamic variation
        intensity_score = rms_mean + 0.5 * rms_std

        if intensity_score > 0.3:
            return "very_intense"
        elif intensity_score > 0.2:
            return "intense"
        elif intensity_score > 0.1:
            return "moderate"
        else:
            return "soft"

    def _infer_mood(self, tempo: float, key: str, tonality: str, intensity: str) -> str:
        """Infer overall mood from combined features"""
        mood_features = []

        # Tempo-based mood
        if tempo > 140:
            mood_features.append("energetic")
        elif tempo > 100:
            mood_features.append("upbeat")
        elif tempo > 60:
            mood_features.append("moderate")
        else:
            mood_features.append("slow")

        # Tonality-based mood
        if tonality == "major":
            mood_features.append("bright")
        else:
            mood_features.append("dark")

        # Intensity-based mood
        if intensity in ["very_intense", "intense"]:
            mood_features.append("dramatic")

        return ", ".join(mood_features)

    def _infer_time_signature(self, beats: np.ndarray) -> str:
        """Infer time signature from beat information"""
        if len(beats) < 2:
            return "4/4"

        # Simple heuristic based on beat regularity
        beat_intervals = np.diff(beats)
        regularity = np.std(beat_intervals) / (np.mean(beat_intervals) + 1e-6)

        # This is a simplified heuristic
        if regularity < 0.1:
            return "4/4"
        elif regularity < 0.2:
            return "3/4"
        else:
            return "6/8"

    def features_to_description(self, features: MusicalFeatures) -> str:
        """
        Convert musical features to natural language description
        This will be used to create the prompt for image generation
        """
        description = f"""
Musical Analysis:
- Key: {features.key_signature} {features.tonality}
- Tempo: {features.tempo:.0f} BPM
- Time Signature: {features.time_signature}
- Melodic Contour: {features.melody_contour}
- Harmonic Style: {features.harmonic_progression}
- Dynamic Intensity: {features.dynamic_intensity}
- Overall Mood: {features.overall_mood}
- Tonality: {features.tonality.capitalize()}
"""
        return description
