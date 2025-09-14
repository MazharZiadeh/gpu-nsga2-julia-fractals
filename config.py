"""
Configuration settings for the Julia Fractal Evolution system.
"""

import os
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class EvolutionParams:
    """Parameters for the evolutionary algorithm."""
    mu: int = 50          # Population size
    lambda_: int = 50     # Offspring size
    cxpb: float = 0.7     # Crossover probability
    mutpb: float = 0.2    # Mutation probability
    ngen: int = 20        # Number of generations

@dataclass
class FractalParams:
    """Parameters for fractal generation."""
    width: int = 200
    height: int = 200
    max_iter_base: int = 100
    zoom_range: Tuple[float, float] = (0.5, 5.0)
    c_real_range: Tuple[float, float] = (-1.0, 1.0)
    c_imag_range: Tuple[float, float] = (-1.0, 1.0)

@dataclass
class RenderParams:
    """Parameters for rendering high-quality fractals."""
    high_res_width: int = 600
    high_res_height: int = 600
    dpi: int = 150
    colormap: str = "inferno"

@dataclass
class Config:
    """Main configuration class."""
    evolution: EvolutionParams = None
    fractal: FractalParams = None
    render: RenderParams = None

    # Output directories
    results_dir: str = "results"
    top20_dir: str = "results/top20"
    pareto_dir: str = "results/pareto_fronts"

    def __post_init__(self):
        """Initialize default values if None."""
        if self.evolution is None:
            self.evolution = EvolutionParams()
        if self.fractal is None:
            self.fractal = FractalParams()
        if self.render is None:
            self.render = RenderParams()

        # Create output directories if they don't exist
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.top20_dir, exist_ok=True)
        os.makedirs(self.pareto_dir, exist_ok=True)

# Predefined scenarios
SCENARIOS = {
    "S1": EvolutionParams(mu=30, lambda_=70, cxpb=0.6, mutpb=0.4, ngen=30),  # Entropy focused
    "S2": EvolutionParams(mu=70, lambda_=30, cxpb=0.9, mutpb=0.05, ngen=25), # Contrast vs Time
    "S3": EvolutionParams(mu=50, lambda_=50, cxpb=0.7, mutpb=0.2, ngen=20),  # Balanced
}

def get_config(scenario: str = "S3") -> Config:
    """Get configuration for a specific scenario."""
    config = Config()
    if scenario in SCENARIOS:
        config.evolution = SCENARIOS[scenario]
    return config
