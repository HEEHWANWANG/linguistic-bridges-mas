"""
Mel-Spectrogram Converter - Convert between audio waveforms and mel-spectrograms

Supports:
- Raw audio waveform → Mel-spectrogram conversion
- Mel-spectrogram → Text representation for LLM processing
- Flexible parameter control (n_mels, hop_length, window type, etc.)
"""

import numpy as np
import librosa
import logging
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MelSpectrogramConfig:
    """Configuration for mel-spectrogram conversion"""
    n_mels: int = 128  # Number of mel frequency bins
    n_fft: int = 2048  # FFT window size
    hop_length: int = 512  # Number of samples between successive frames
    window: str = "hann"  # Window function type
    fmin: int = 0  # Minimum frequency (Hz)
    fmax: Optional[int] = None  # Maximum frequency (Hz)
    sample_rate: int = 16000  # Audio sample rate (Hz)
    power: float = 2.0  # Power of magnitude spectrum
    log_scale: bool = True  # Whether to use log scale (dB)
    center: bool = True  # Whether to center the signal

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "n_mels": self.n_mels,
            "n_fft": self.n_fft,
            "hop_length": self.hop_length,
            "window": self.window,
            "fmin": self.fmin,
            "fmax": self.fmax,
            "sample_rate": self.sample_rate,
            "power": self.power,
            "log_scale": self.log_scale,
            "center": self.center
        }


class MelSpectrogramConverter:
    """
    Convert between audio waveforms and mel-spectrograms

    Mel-spectrograms are useful for LLM processing because they:
    1. Compress high-dimensional audio into manageable representation
    2. Focus on perceptually relevant frequency ranges
    3. Highlight musical content vs noise
    4. Can be encoded as text/image for LLM input
    """

    def __init__(self, config: Optional[MelSpectrogramConfig] = None):
        """
        Initialize converter

        Args:
            config: MelSpectrogramConfig (uses defaults if None)
        """
        self.config = config or MelSpectrogramConfig()
        self.logger = logging.getLogger(__name__)

    def audio_to_mel_spectrogram(self, audio: np.ndarray) -> np.ndarray:
        """
        Convert audio waveform to mel-spectrogram

        Args:
            audio: Audio waveform (samples,)

        Returns:
            Mel-spectrogram (n_mels, n_frames)
        """
        if not isinstance(audio, np.ndarray):
            raise TypeError(f"Expected numpy array, got {type(audio)}")

        if len(audio.shape) != 1:
            raise ValueError(f"Expected 1D audio, got shape {audio.shape}")

        # Create mel-spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=self.config.sample_rate,
            n_fft=self.config.n_fft,
            hop_length=self.config.hop_length,
            window=self.config.window,
            center=self.config.center,
            pad_mode="reflect",
            power=self.config.power,
            n_mels=self.config.n_mels,
            fmin=self.config.fmin,
            fmax=self.config.fmax
        )

        # Convert to dB scale if requested
        if self.config.log_scale:
            mel_spec = librosa.power_to_db(mel_spec, ref=np.max)

        self.logger.info(
            f"Converted audio to mel-spectrogram: {audio.shape} → {mel_spec.shape}"
        )

        return mel_spec

    def mel_spectrogram_to_text_representation(self, mel_spec: np.ndarray) -> str:
        """
        Convert mel-spectrogram to text representation for LLM processing

        This creates a compact text representation that an LLM can understand
        and reason about without needing to process the full matrix.

        Args:
            mel_spec: Mel-spectrogram (n_mels, n_frames)

        Returns:
            Text representation of mel-spectrogram characteristics
        """
        # Analyze mel-spectrogram properties
        stats = self._analyze_mel_spectrogram(mel_spec)

        # Create text representation
        text_repr = f"""
MEL-SPECTROGRAM ANALYSIS:
- Shape: {mel_spec.shape[0]} mel bands × {mel_spec.shape[1]} time frames
- Duration: {self._frames_to_seconds(mel_spec.shape[1]):.2f} seconds
- Time Resolution: {self._get_time_resolution():.4f} seconds/frame

FREQUENCY CHARACTERISTICS:
- Total Frequency Range: 0 Hz - {self.config.fmax or self.config.sample_rate//2} Hz
- Number of Mel Bands: {self.config.n_mels}
- Distribution: Logarithmically spaced

SPECTRAL FEATURES:
- Energy Profile: {"High-energy throughout" if stats["mean_energy"] > stats["median_energy"] else "Variable energy"}
- Peak Energy: {stats["max_energy"]:.2f} dB
- Mean Energy: {stats["mean_energy"]:.2f} dB
- Energy Dynamics: {stats["energy_variance"]:.2f} (standard deviation)

TEMPORAL CHARACTERISTICS:
- Frequency Stability: {stats["frequency_stability"]:.2f} (0=changing, 1=stable)
- Energy Continuity: {stats["energy_continuity"]:.2f} (0=jumpy, 1=smooth)
- Spectral Centroid: {stats["spectral_centroid_hz"]:.0f} Hz

FREQUENCY BAND ANALYSIS (Energy distribution):
- Low (0-500 Hz): {stats["low_freq_energy"]:.1f}%
- Mid-Low (500-2K Hz): {stats["midlow_freq_energy"]:.1f}%
- Mid (2K-8K Hz): {stats["mid_freq_energy"]:.1f}%
- High (8K+ Hz): {stats["high_freq_energy"]:.1f}%

ENCODED SPECTRAL PATTERN (simplified):
{self._encode_spectral_pattern(mel_spec)}

ENERGY ENVELOPE:
{self._encode_energy_envelope(mel_spec)}
"""
        return text_repr

    def _analyze_mel_spectrogram(self, mel_spec: np.ndarray) -> Dict[str, Any]:
        """
        Analyze mel-spectrogram to extract summary statistics

        Args:
            mel_spec: Mel-spectrogram (n_mels, n_frames)

        Returns:
            Dictionary with analysis results
        """
        # Basic statistics
        mean_energy = np.mean(mel_spec)
        max_energy = np.max(mel_spec)
        median_energy = np.median(mel_spec)
        energy_variance = np.var(mel_spec)

        # Temporal smoothness
        energy_diff = np.diff(np.mean(mel_spec, axis=0))
        energy_continuity = 1.0 / (1.0 + np.std(energy_diff))  # Smooth = 1, jumpy = 0

        # Frequency stability
        temporal_mean = np.mean(mel_spec, axis=1)
        freq_stability = np.corrcoef(
            temporal_mean[:-1], temporal_mean[1:]
        )[0, 1]  # How similar consecutive frequency bands are
        freq_stability = np.clip(freq_stability, 0, 1) if not np.isnan(freq_stability) else 0.5

        # Spectral centroid in Hz
        frequencies = librosa.mel_frequencies(
            n_mels=self.config.n_mels,
            fmin=self.config.fmin,
            fmax=self.config.fmax
        )
        spectral_centroid_hz = np.average(frequencies, weights=np.mean(mel_spec, axis=1))

        # Energy in frequency bands
        total_energy = np.sum(mel_spec)
        low_freq_bins = self.config.n_mels // 8  # Lower frequencies
        midlow_freq_bins = self.config.n_mels // 4  # Mid-low
        mid_freq_bins = self.config.n_mels // 2  # Mid
        high_freq_bins = self.config.n_mels  # High

        low_energy = np.sum(mel_spec[:low_freq_bins]) / total_energy * 100 if total_energy > 0 else 0
        midlow_energy = np.sum(mel_spec[low_freq_bins:low_freq_bins+midlow_freq_bins]) / total_energy * 100
        mid_energy = np.sum(mel_spec[midlow_freq_bins:mid_freq_bins]) / total_energy * 100
        high_energy = np.sum(mel_spec[mid_freq_bins:]) / total_energy * 100

        return {
            "mean_energy": mean_energy,
            "max_energy": max_energy,
            "median_energy": median_energy,
            "energy_variance": energy_variance,
            "frequency_stability": freq_stability,
            "energy_continuity": energy_continuity,
            "spectral_centroid_hz": spectral_centroid_hz,
            "low_freq_energy": low_energy,
            "midlow_freq_energy": midlow_energy,
            "mid_freq_energy": mid_energy,
            "high_freq_energy": high_energy
        }

    def _frames_to_seconds(self, n_frames: int) -> float:
        """Convert frame count to seconds"""
        return (n_frames - 1) * self.config.hop_length / self.config.sample_rate

    def _get_time_resolution(self) -> float:
        """Get time resolution per frame in seconds"""
        return self.config.hop_length / self.config.sample_rate

    def _encode_spectral_pattern(self, mel_spec: np.ndarray, resolution: int = 8) -> str:
        """
        Create a simplified text representation of spectral pattern

        Args:
            mel_spec: Mel-spectrogram (n_mels, n_frames)
            resolution: Number of characters to use for encoding (8 = 8 time steps)

        Returns:
            Text pattern
        """
        # Downsample to resolution
        frame_indices = np.linspace(0, mel_spec.shape[1]-1, resolution, dtype=int)
        patterns = []

        for idx in frame_indices:
            # Get mean energy at this time
            frame_energy = np.mean(mel_spec[:, idx])
            # Map to character (. is low, * is high)
            if frame_energy < -20:
                char = '.'
            elif frame_energy < -10:
                char = '·'
            elif frame_energy < 0:
                char = '▫'
            elif frame_energy < 10:
                char = '▪'
            else:
                char = '█'
            patterns.append(char)

        return "[" + "".join(patterns) + "]"

    def _encode_energy_envelope(self, mel_spec: np.ndarray, height: int = 4) -> str:
        """
        Create ASCII art of energy envelope

        Args:
            mel_spec: Mel-spectrogram (n_mels, n_frames)
            height: Height of ASCII art (lines)

        Returns:
            ASCII art representation
        """
        # Get average energy over time at each frequency band
        freq_energy = np.mean(mel_spec, axis=1)

        # Normalize to 0-1
        if np.max(freq_energy) > np.min(freq_energy):
            freq_energy = (freq_energy - np.min(freq_energy)) / (np.max(freq_energy) - np.min(freq_energy))
        else:
            freq_energy = np.ones_like(freq_energy) * 0.5

        # Create ASCII visualization (side view)
        lines = []
        for level in range(height, 0, -1):
            threshold = level / height
            line = "".join("█" if e >= threshold else " " for e in freq_energy)
            lines.append("| " + line)
        lines.append("|" + "─" * len(freq_energy))

        return "\n".join(lines)

    def detect_input_type(self, data: np.ndarray) -> str:
        """
        Detect whether input is audio waveform or mel-spectrogram

        Args:
            data: Input data (1D audio or 2D mel-spectrogram)

        Returns:
            "waveform" or "melspectrogram"
        """
        if len(data.shape) == 1:
            return "waveform"
        elif len(data.shape) == 2:
            return "melspectrogram"
        else:
            raise ValueError(f"Expected 1D or 2D array, got shape {data.shape}")

    def ensure_audio_waveform(self, data: np.ndarray) -> np.ndarray:
        """
        Ensure data is audio waveform. If mel-spectrogram, raise error
        (mel-spectrogram to audio conversion is complex and lossy)

        Args:
            data: Input data

        Returns:
            Audio waveform if input is already waveform

        Raises:
            ValueError: If input is mel-spectrogram
        """
        input_type = self.detect_input_type(data)

        if input_type == "waveform":
            return data
        else:
            raise ValueError(
                "Input appears to be mel-spectrogram, not audio waveform. "
                "Converting mel-spectrogram back to audio is lossy and complex. "
                "Please provide the original audio waveform."
            )

    def ensure_mel_spectrogram(self, data: np.ndarray) -> np.ndarray:
        """
        Ensure data is mel-spectrogram. If waveform, convert it.

        Args:
            data: Input data (waveform or mel-spectrogram)

        Returns:
            Mel-spectrogram
        """
        input_type = self.detect_input_type(data)

        if input_type == "melspectrogram":
            return data
        else:
            # Convert waveform to mel-spectrogram
            return self.audio_to_mel_spectrogram(data)


def create_mel_spectrogram_text_for_llm(
    audio_data: np.ndarray,
    config: Optional[MelSpectrogramConfig] = None,
    use_mel_spectro gram: bool = True
) -> Tuple[str, Optional[np.ndarray]]:
    """
    Convenience function to create mel-spectrogram text representation for LLM

    Args:
        audio_data: Audio waveform (1D array) or mel-spectrogram (2D array)
        config: MelSpectrogramConfig
        use_mel_spectrogram: Whether to convert waveform to mel-spectrogram

    Returns:
        Tuple of (text_representation, mel_spectrogram or None)

    Example:
        text, mel_spec = create_mel_spectrogram_text_for_llm(audio)
        # text is ready to include in LLM prompts
        # mel_spec can be saved or visualized
    """
    converter = MelSpectrogramConverter(config)

    if use_mel_spectrogram:
        # Ensure we have mel-spectrogram
        mel_spec = converter.ensure_mel_spectrogram(audio_data)
        text = converter.mel_spectrogram_to_text_representation(mel_spec)
        return text, mel_spec
    else:
        # Work with waveform directly
        audio = converter.ensure_audio_waveform(audio_data)
        return "", audio  # Return empty string since not using mel-spectrogram


# Example usage and testing
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Create example audio
    sr = 16000
    duration = 3  # seconds
    t = np.linspace(0, duration, int(sr * duration))

    # Create a signal with multiple frequencies (C major chord)
    audio = (
        np.sin(2 * np.pi * 261.63 * t) +  # C4
        np.sin(2 * np.pi * 329.63 * t) +  # E4
        np.sin(2 * np.pi * 392.00 * t)    # G4
    ) / 3  # Average

    # Convert to mel-spectrogram
    converter = MelSpectrogramConverter()
    mel_spec = converter.audio_to_mel_spectrogram(audio)
    text_repr = converter.mel_spectrogram_to_text_representation(mel_spec)

    print("Audio shape:", audio.shape)
    print("Mel-spectrogram shape:", mel_spec.shape)
    print("\nText representation for LLM:")
    print(text_repr)
