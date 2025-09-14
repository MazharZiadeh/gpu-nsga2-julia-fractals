#!/usr/bin/env python3
"""
Main entry point for the Julia Fractal Evolution system.

This script provides a clean, professional interface for running
multi-objective evolutionary optimization of Julia set fractals.
"""

import argparse
import sys
import os
import pandas as pd
from typing import Optional

from config import get_config, SCENARIOS
from evolution_engine import EvolutionEngine
from visualization import FractalVisualizer

def print_banner():
    """Print a professional banner."""
    print("=" * 70)
    print("🔮 GPU-NSGA2-Julia-Fractals")
    print("   Multi-Objective Evolution of Visual Complexity")
    print("=" * 70)
    print()

def print_scenario_info(scenario: str, config):
    """Print information about the selected scenario."""
    scenario_names = {
        "S1": "Entropy Optimization (Complex Patterns)",
        "S2": "Contrast vs Time Balance", 
        "S3": "Full Multi-Objective Exploration"
    }
    
    print(f"📊 Scenario: {scenario} - {scenario_names.get(scenario, 'Unknown')}")
    print(f"   Population: {config.evolution.mu}")
    print(f"   Offspring: {config.evolution.lambda_}")
    print(f"   Generations: {config.evolution.ngen}")
    print(f"   Crossover Rate: {config.evolution.cxpb}")
    print(f"   Mutation Rate: {config.evolution.mutpb}")
    print()

def run_evolution(scenario: str, verbose: bool = True) -> tuple:
    """
    Run the evolutionary algorithm.
    
    Args:
        scenario: Scenario identifier (S1, S2, S3)
        verbose: Whether to print progress
        
    Returns:
        Tuple of (final_population, pareto_front, statistics)
    """
    # Get configuration
    config = get_config(scenario)
    
    if verbose:
        print_scenario_info(scenario, config)
    
    # Initialize evolution engine
    engine = EvolutionEngine(config)
    
    if verbose:
        print("🧬 Initializing population...")
    
    # Run evolution
    final_population = engine.evolve(verbose=verbose)
    pareto_front = engine.get_pareto_front()
    statistics = engine.get_statistics()
    
    if verbose:
        print(f"\n✅ Evolution completed!")
        print(f"   Final population size: {len(final_population)}")
        print(f"   Pareto front size: {len(pareto_front)}")
    
    return final_population, pareto_front, statistics

def save_results(pareto_front, statistics, config, verbose: bool = True):
    """
    Save evolution results to files.
    
    Args:
        pareto_front: List of Pareto optimal individuals
        statistics: DEAP logbook with statistics
        config: Configuration object
        verbose: Whether to print progress
    """
    if verbose:
        print("\n💾 Saving results...")
    
    # Save fitness data to Excel
    records = []
    for ind in pareto_front:
        record = {
            "c_real": ind[0],
            "c_imag": ind[1], 
            "zoom": ind[2],
            "entropy": ind.fitness.values[0],
            "contrast": ind.fitness.values[1],
            "compute_time": ind.fitness.values[2],
            "generation": getattr(ind, "generation", "N/A")
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    excel_path = os.path.join(config.results_dir, "evolution_results.xlsx")
    df.to_excel(excel_path, index=False)
    
    if verbose:
        print(f"✅ Evolution data saved to {excel_path}")
    
    return df

def create_visualizations(pareto_front, statistics, df, config, verbose: bool = True):
    """
    Create and save visualizations.
    
    Args:
        pareto_front: List of Pareto optimal individuals
        statistics: DEAP logbook with statistics
        df: DataFrame with fitness data
        config: Configuration object
        verbose: Whether to print progress
    """
    if verbose:
        print("\n🎨 Creating visualizations...")
    
    visualizer = FractalVisualizer(config)
    
    # Plot Pareto fronts
    pareto_path = os.path.join(config.pareto_dir, "pareto_fronts.png")
    visualizer.plot_pareto_fronts(pareto_front, save_path=pareto_path)
    
    # Plot convergence
    convergence_path = os.path.join(config.results_dir, "convergence.png")
    visualizer.plot_convergence(statistics, save_path=convergence_path)
    
    # Save top fractals
    visualizer.save_top_fractals(pareto_front, num_fractals=20)
    
    # Create fractal grid
    visualizer.create_fractal_grid(num_fractals=20, grid_size=(4, 5))
    
    # Normalized Pareto plots
    normalized_path = os.path.join(config.pareto_dir, "normalized_pareto.png")
    visualizer.plot_normalized_pareto(df, save_path=normalized_path)
    
    # Calculate and save spread metrics
    metrics = visualizer.calculate_spread_metrics(df)
    metrics_path = os.path.join(config.results_dir, "spread_metrics.txt")
    with open(metrics_path, 'w') as f:
        f.write(f"Spread (Time vs Entropy): {metrics['spread_time_entropy']:.4f}\n")
        f.write(f"Spread (Contrast vs Entropy): {metrics['spread_contrast_entropy']:.4f}\n")
    
    if verbose:
        print("✅ All visualizations created!")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Multi-objective evolution of Julia set fractals using NSGA-II",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --scenario S1          # Run entropy-focused scenario
  python main.py --scenario S2 --quiet  # Run contrast-time scenario quietly
  python main.py --list-scenarios       # List available scenarios
        """
    )
    
    parser.add_argument(
        "--scenario", "-s",
        choices=list(SCENARIOS.keys()),
        default="S3",
        help="Evolution scenario to run (default: S3)"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress verbose output"
    )
    
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List available scenarios and exit"
    )
    
    args = parser.parse_args()
    
    if args.list_scenarios:
        print("Available scenarios:")
        for scenario, params in SCENARIOS.items():
            print(f"  {scenario}: μ={params.mu}, λ={params.lambda_}, "
                  f"cxpb={params.cxpb}, mutpb={params.mutpb}, ngen={params.ngen}")
        return
    
    verbose = not args.quiet
    
    if verbose:
        print_banner()
    
    try:
        # Run evolution
        final_pop, pareto_front, stats = run_evolution(args.scenario, verbose)
        
        if not pareto_front:
            print("❌ No Pareto front found! Evolution may have failed.")
            sys.exit(1)
        
        # Save results
        df = save_results(pareto_front, stats, get_config(args.scenario), verbose)
        
        # Create visualizations
        create_visualizations(pareto_front, stats, df, get_config(args.scenario), verbose)
        
        if verbose:
            print(f"\n🎉 All done! Check the 'results/' directory for outputs.")
            print("   - evolution_results.xlsx: Fitness data")
            print("   - fractal_grid.png: Combined fractal grid")
            print("   - top20/: Individual fractal images")
            print("   - pareto_fronts/: Pareto front visualizations")
            print("   - convergence.png: Evolution convergence")
        
    except KeyboardInterrupt:
        print("\n⚠️  Evolution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
