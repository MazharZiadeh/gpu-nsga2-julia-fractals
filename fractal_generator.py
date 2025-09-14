"""
Julia set fractal generation module.
"""

import time
import numpy as np
from typing import Tuple, List
from config import FractalParams

class JuliaGenerator:
    """Generator for Julia set fractals."""

    def __init__(self, params: FractalParams):
        self.params = params

    def generate_julia(self,
                      c: complex,
                      width: int = None,
                      height: int = None,
                      xlim: Tuple[float, float] = None,
                      ylim: Tuple[float, float] = None,
                      max_iter: int = None) -> np.ndarray:
        """
        Generate a Julia set fractal.

        Args:
            c: Complex constant for Julia set
            width: Image width (default from params)
            height: Image height (default from params)
            xlim: X-axis limits (default calculated from zoom)
            ylim: Y-axis limits (default calculated from zoom)
            max_iter: Maximum iterations (default calculated from zoom)

        Returns:
            NumPy array representing the fractal
        """
        width = width or self.params.width
        height = height or self.params.height
        max_iter = max_iter or self.params.max_iter_base

        # Create coordinate grids
        real = np.linspace(xlim[0], xlim[1], width)
        imag = np.linspace(ylim[0], ylim[1], height)
        Z = real[:, None] + 1j * imag[None, :]
        C = np.full_like(Z, c)

        # Initialize escape time array
        M = np.zeros(Z.shape, dtype=int)
        mask = np.ones(Z.shape, bool)

        # Iterate until escape or max iterations
        for i in range(max_iter):
            Z[mask] = Z[mask]**2 + C[mask]
            escaped = np.abs(Z) > 2
            M[mask & escaped] = i
            mask &= ~escaped

            # Early termination if all points have escaped
            if not mask.any():
                break

        return M

    def calculate_bounds(self, zoom: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Calculate x and y limits based on zoom level."""
        xlim = (-1.5/zoom, 1.5/zoom)
        ylim = (-1.5/zoom, 1.5/zoom)
        return xlim, ylim

    def calculate_max_iter(self, zoom: float) -> int:
        """Calculate maximum iterations based on zoom level."""
        return int(self.params.max_iter_base * zoom)

class FractalEvaluator:
    """Evaluates fractal fitness based on multiple objectives."""

    def __init__(self, generator: JuliaGenerator):
        self.generator = generator

    def evaluate_fractal(self, individual: List[float]) -> Tuple[float, float, float]:
        """
        Evaluate a fractal's fitness across three objectives:
        1. Image entropy (maximize)
        2. Image contrast (maximize)
        3. Computation time (minimize)

        Args:
            individual: [c_real, c_imag, zoom]

        Returns:
            Tuple of (entropy, contrast, computation_time)
        """
        c = complex(individual[0], individual[1])
        zoom = individual[2]

        # Calculate bounds and max iterations
        xlim, ylim = self.generator.calculate_bounds(zoom)
        max_iter = self.generator.calculate_max_iter(zoom)

        # Generate fractal and measure computation time
        start_time = time.time()
        M = self.generator.generate_julia(c, xlim=xlim, ylim=ylim, max_iter=max_iter)
        comp_time = time.time() - start_time

        # Calculate fitness metrics
        img_entropy = self._calculate_entropy(M, max_iter)
        img_contrast = self._calculate_contrast(M)

        return img_entropy, img_contrast, comp_time

    def _calculate_entropy(self, M: np.ndarray, max_iter: int) -> float:
        """Calculate image entropy."""
        from scipy.stats import entropy

        # Create histogram of escape times
        hist, _ = np.histogram(M, bins=range(max_iter + 2), density=True)
        # Add small epsilon to avoid log(0)
        return entropy(hist + 1e-8)

    def _calculate_contrast(self, M: np.ndarray) -> float:
        """Calculate image contrast as standard deviation."""
        max_M = np.max(M)
        if max_M == 0:
            return 0.0

        norm_M = M / max_M
        return np.std(norm_M)
