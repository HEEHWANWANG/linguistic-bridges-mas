#!/bin/bash

# Batch Visual Prompt Generation Script
# Generates 5 prompts (3 convergent + 2 divergent) for each audio sample

set -e

echo "=========================================="
echo "BATCH VISUAL PROMPT GENERATION"
echo "=========================================="

# Configuration
DATASET="${1:-dataset/label_data_with_16kHz_audio.npy}"
OUTPUT_DIR="${2:-generated_prompts}"
NUM_SAMPLES="${3:-}"  # Empty = all samples
START_IDX="${4:-0}"
MEL_SPECTROGRAM="${5:-false}"

echo "Configuration:"
echo "  Dataset: $DATASET"
echo "  Output directory: $OUTPUT_DIR"
echo "  Samples to process: ${NUM_SAMPLES:-all}"
echo "  Starting from index: $START_IDX"
echo "  Mel-spectrogram: $MEL_SPECTROGRAM"
echo ""

# Build command
CMD="python3 generate_visual_prompts_batch.py"
CMD="$CMD --dataset $DATASET"
CMD="$CMD --output-dir $OUTPUT_DIR"
CMD="$CMD --start-idx $START_IDX"

if [ ! -z "$NUM_SAMPLES" ]; then
    CMD="$CMD --samples $NUM_SAMPLES"
fi

if [ "$MEL_SPECTROGRAM" = "true" ]; then
    CMD="$CMD --mel-spectrogram"
fi

echo "Running: $CMD"
echo ""

# Execute
eval $CMD

echo ""
echo "=========================================="
echo "✓ GENERATION COMPLETE"
echo "=========================================="
echo ""
echo "Output files created in: $OUTPUT_DIR/"
echo "  - visual_prompts_complete.json"
echo "  - prompts_for_image_generation.json"
echo "  - generation_summary.json"
echo ""
