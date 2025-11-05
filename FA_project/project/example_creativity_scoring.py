"""
Examples: Calculate Creativity Scores for Batch-Generated Prompts

Demonstrates different ways to:
1. Calculate creativity scores for all generated prompts
2. Compare convergent vs divergent prompts
3. Analyze results by musical features
4. Generate reports and visualizations
"""

import asyncio
import json
from pathlib import Path
from calculate_batch_creativity_scores import BatchCreativityCalculator


async def example_1_simple_scoring():
    """Example 1: Simple one-line creativity scoring"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Simple Creativity Scoring")
    print("=" * 70)

    # Create calculator
    calculator = BatchCreativityCalculator(
        prompts_file="generated_prompts/visual_prompts_complete.json",
        output_dir="creativity_scores"
    )

    # Run evaluation
    print("Running creativity evaluation on all prompts...")
    await calculator.run_full_evaluation()

    # Save results
    calculator.save_prompt_scores()
    calculator.save_sample_summaries()
    calculator.save_dataset_stats()

    # Print summary
    calculator.print_summary()


async def example_2_detailed_analysis():
    """Example 2: Detailed analysis of results"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Detailed Analysis")
    print("=" * 70)

    calculator = BatchCreativityCalculator(
        prompts_file="generated_prompts/visual_prompts_complete.json",
        output_dir="creativity_scores"
    )

    await calculator.run_full_evaluation()

    stats = calculator.dataset_stats

    print(f"\nDetailed Creativity Analysis:")
    print(f"\n1. Overall Statistics:")
    print(f"   Mean creativity score: {stats.mean_overall:.2f}/5.00")
    print(f"   Standard deviation: {stats.std_overall:.2f}")
    print(f"   Score range: {stats.min_overall:.2f} - {stats.max_overall:.2f}")

    print(f"\n2. By Creativity Dimension:")
    print(f"   Originality:  {stats.mean_originality:.2f}/5.00 (σ={stats.std_originality:.2f})")
    print(f"   Elaboration:  {stats.mean_elaboration:.2f}/5.00 (σ={stats.std_elaboration:.2f})")
    print(f"   Alignment:    {stats.mean_alignment:.2f}/5.00 (σ={stats.std_alignment:.2f})")
    print(f"   Coherence:    {stats.mean_coherence:.2f}/5.00 (σ={stats.std_coherence:.2f})")

    print(f"\n3. Generation Mode Comparison:")
    print(f"   Convergent (T=0.4): {stats.convergent_mean:.2f}/5.00 (σ={stats.convergent_std:.2f})")
    print(f"   Divergent (T=0.8):  {stats.divergent_mean:.2f}/5.00 (σ={stats.divergent_std:.2f})")
    diff = stats.divergent_mean - stats.convergent_mean
    direction = "MORE" if diff > 0 else "LESS"
    print(f"   → Divergent prompts are {direction} creative by {abs(diff):.2f} points")

    print(f"\n4. Feature Correlations (with overall creativity):")
    if 'tempo' in stats.correlations:
        tempo_corr = stats.correlations['tempo'].get('overall', 0.0)
        direction = "positive" if tempo_corr > 0 else "negative"
        print(f"   Tempo → Creativity: {tempo_corr:.3f} ({direction})")
        if abs(tempo_corr) > 0.3:
            print(f"     → Moderate to strong correlation detected")
        elif abs(tempo_corr) > 0.1:
            print(f"     → Weak correlation detected")
        else:
            print(f"     → Negligible correlation")

    # Save all results
    calculator.save_prompt_scores()
    calculator.save_sample_summaries()
    calculator.save_dataset_stats()
    calculator.save_comparison_report()

    print(f"\n5. Output Files Created:")
    print(f"   ✓ creativity_prompt_scores.json - All individual prompt scores")
    print(f"   ✓ creativity_sample_summaries.json - Per-sample aggregates")
    print(f"   ✓ creativity_dataset_stats.json - Overall statistics")
    print(f"   ✓ creativity_comparison_report.json - Convergent vs divergent")


async def example_3_score_inspection():
    """Example 3: Inspect individual prompt scores"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Inspecting Prompt Scores")
    print("=" * 70)

    # Load existing scores (from previous run)
    scores_file = Path("creativity_scores/creativity_prompt_scores.json")

    if not scores_file.exists():
        print(f"Scores file not found: {scores_file}")
        print("Run Example 1 first to generate scores")
        return

    with open(scores_file, 'r') as f:
        scores = json.load(f)

    print(f"\nLoaded {len(scores)} prompt scores\n")

    # Find highest and lowest scores
    highest = max(scores, key=lambda x: x['overall'])
    lowest = min(scores, key=lambda x: x['overall'])

    print("HIGHEST CREATIVITY SCORE:")
    print(f"  Sample: {highest['sample_idx']}, Prompt: {highest['prompt_id']}")
    print(f"  Mode: {highest['mode']}, Temperature: {highest['temperature']}")
    print(f"  Originality:  {highest['originality']:.2f}")
    print(f"  Elaboration:  {highest['elaboration']:.2f}")
    print(f"  Alignment:    {highest['alignment']:.2f}")
    print(f"  Coherence:    {highest['coherence']:.2f}")
    print(f"  Overall:      {highest['overall']:.2f}")
    print(f"  Text: {highest['prompt_text'][:100]}...")

    print("\nLOWEST CREATIVITY SCORE:")
    print(f"  Sample: {lowest['sample_idx']}, Prompt: {lowest['prompt_id']}")
    print(f"  Mode: {lowest['mode']}, Temperature: {lowest['temperature']}")
    print(f"  Originality:  {lowest['originality']:.2f}")
    print(f"  Elaboration:  {lowest['elaboration']:.2f}")
    print(f"  Alignment:    {lowest['alignment']:.2f}")
    print(f"  Coherence:    {lowest['coherence']:.2f}")
    print(f"  Overall:      {lowest['overall']:.2f}")
    print(f"  Text: {lowest['prompt_text'][:100]}...")

    # Group by mode
    convergent = [s for s in scores if s['mode'] == 'convergent']
    divergent = [s for s in scores if s['mode'] == 'divergent']

    print(f"\nCONVERGENT SCORES:")
    conv_overalls = [s['overall'] for s in convergent]
    print(f"  Count: {len(convergent)}")
    print(f"  Mean: {sum(conv_overalls)/len(conv_overalls):.2f}")
    print(f"  Min: {min(conv_overalls):.2f}")
    print(f"  Max: {max(conv_overalls):.2f}")

    print(f"\nDIVERGENT SCORES:")
    div_overalls = [s['overall'] for s in divergent]
    print(f"  Count: {len(divergent)}")
    print(f"  Mean: {sum(div_overalls)/len(div_overalls):.2f}")
    print(f"  Min: {min(div_overalls):.2f}")
    print(f"  Max: {max(div_overalls):.2f}")


async def example_4_comparison_report():
    """Example 4: Generate and analyze comparison report"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Convergent vs Divergent Comparison")
    print("=" * 70)

    # Load comparison report
    report_file = Path("creativity_scores/creativity_comparison_report.json")

    if not report_file.exists():
        print(f"Report file not found: {report_file}")
        print("Run Example 1 first to generate report")
        return

    with open(report_file, 'r') as f:
        report = json.load(f)

    conv_div = report['convergent_vs_divergent']
    by_dim = report['by_dimension']

    print(f"\nOVERALL COMPARISON:")
    print(f"  Convergent mean: {conv_div['convergent_mean']:.2f} (n={conv_div['convergent_count']})")
    print(f"  Divergent mean:  {conv_div['divergent_mean']:.2f} (n={conv_div['divergent_count']})")
    print(f"  Difference:      {conv_div['difference']:+.2f}")

    if conv_div['difference'] > 0:
        print(f"  → Divergent prompts are MORE creative")
    else:
        print(f"  → Convergent prompts are MORE creative")

    print(f"\nBY DIMENSION:")
    for dim_name, dim_data in by_dim.items():
        print(f"  {dim_name.upper()}:")
        print(f"    Convergent: {dim_data['convergent']:.2f}")
        print(f"    Divergent:  {dim_data['divergent']:.2f}")
        diff = dim_data['divergent'] - dim_data['convergent']
        print(f"    Difference: {diff:+.2f}")


async def example_5_custom_analysis():
    """Example 5: Custom analysis workflow"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Custom Analysis Workflow")
    print("=" * 70)

    calculator = BatchCreativityCalculator(
        prompts_file="generated_prompts/visual_prompts_complete.json",
        output_dir="creativity_scores"
    )

    print("Step 1: Calculating all creativity scores...")
    await calculator.run_full_evaluation()

    print("Step 2: Analyzing by sample...")
    summaries = calculator.sample_summaries

    # Find best and worst samples
    best_sample = max(summaries, key=lambda x: x.avg_overall)
    worst_sample = min(summaries, key=lambda x: x.avg_overall)

    print(f"\nBest performing sample: #{best_sample.sample_idx}")
    print(f"  Average creativity: {best_sample.avg_overall:.2f}")
    print(f"  Convergent avg: {best_sample.conv_overall:.2f}")
    print(f"  Divergent avg: {best_sample.div_overall:.2f}")

    print(f"\nWorst performing sample: #{worst_sample.sample_idx}")
    print(f"  Average creativity: {worst_sample.avg_overall:.2f}")
    print(f"  Convergent avg: {worst_sample.conv_overall:.2f}")
    print(f"  Divergent avg: {worst_sample.div_overall:.2f}")

    print("\nStep 3: Saving comprehensive results...")
    calculator.save_prompt_scores()
    calculator.save_sample_summaries()
    calculator.save_dataset_stats()
    calculator.save_comparison_report()

    print("✓ All results saved to creativity_scores/ directory")

    print("\nStep 4: Summary statistics...")
    stats = calculator.dataset_stats
    print(f"  Total samples evaluated: {stats.total_samples}")
    print(f"  Total prompts scored: {stats.total_prompts}")
    print(f"  Average creativity: {stats.mean_overall:.2f}/5.00")
    print(f"  Most creative dimension: ", end="")

    dims = {
        'Originality': stats.mean_originality,
        'Elaboration': stats.mean_elaboration,
        'Alignment': stats.mean_alignment,
        'Coherence': stats.mean_coherence
    }
    best_dim = max(dims, key=dims.get)
    print(f"{best_dim} ({dims[best_dim]:.2f})")

    least_dim = min(dims, key=dims.get)
    print(f"  Least developed dimension: {least_dim} ({dims[least_dim]:.2f})")


async def main():
    """Run all examples."""
    import sys

    if len(sys.argv) > 1:
        example = sys.argv[1]
    else:
        example = "1"

    if example == "1":
        await example_1_simple_scoring()
    elif example == "2":
        await example_2_detailed_analysis()
    elif example == "3":
        await example_3_score_inspection()
    elif example == "4":
        await example_4_comparison_report()
    elif example == "5":
        await example_5_custom_analysis()
    elif example == "all":
        await example_1_simple_scoring()
        await example_2_detailed_analysis()
        await example_3_score_inspection()
        await example_4_comparison_report()
        await example_5_custom_analysis()
    else:
        print(f"Unknown example: {example}")
        print("Usage: python3 example_creativity_scoring.py [1-5|all]")
        return 1

    return 0


if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
