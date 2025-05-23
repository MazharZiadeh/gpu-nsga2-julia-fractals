# GPU-NSGA2-Julia-Fractals

> A GPU-accelerated multi-objective evolutionary framework for generating high-complexity Julia-set fractals using NSGA-II. Developed in Python, built for Google Colab, and powered by DEAP, NumPy, and optionally CuPy for GPU execution.

---

## 🔥 Overview

This project implements an evolutionary generator for Julia-set fractals optimized across **three competing objectives**:
- **Image Entropy** (visual complexity)
- **Image Contrast** (perceptual sharpness)
- **Computation Time** (runtime performance)

It uses the **NSGA-II** algorithm to evolve fractal configurations (complex constant + zoom factor), evaluates their fitness in real time, and visualizes the Pareto fronts of optimal trade-offs. Final results include:
- Ranked and saved top 20 fractals
- Composite image grid of best outputs
- Excel export of fitness data
- Normalized Pareto front plots and convergence analysis

---

## 📍 Scenarios

Three built-in experimental setups:

| Scenario | Purpose              | Description                                      |
|----------|----------------------|--------------------------------------------------|
| `S1`     | Broad Exploration    | High mutation, large offspring                   |
| `S2`     | Rapid Convergence    | High crossover, elite preservation              |
| `S3`     | Compute-Aware Search | Balanced setup, zoom constrained for speed       |

Select one by setting:

```python
scenario = "S3"  # Options: "S1", "S2", "S3"

Or define your own parameter config.
You can also tweak the math in generate_julia() to evolve entirely new fractal forms or formulae (e.g., z³ + c, orbit traps, etc.).
Outputs
After running, the following will be generated:

results/evolution_results.xlsx – fitness data

results/spread_metrics.txt – spread scores for Pareto front diversity

best_fractals/ – PNGs of top 20 evolved Julia sets

results/combined_best_fractals.png – a 5×4 collage of best images

results/normalized_pareto_*.png – visualized trade-offs

results/convergence_over_generations.png – average progression of objectives

Post-Processing & Analysis
This codebase includes a post-run module for analysis:

Normalized Pareto plots:

Time vs Entropy

Contrast vs Entropy

Spread Metric:

Measures diversity of Pareto front solutions

Convergence Plot:

Visualizes per-generation changes in entropy, contrast, and compute time

These help you quantitatively compare different strategies (S1, S2, S3) or your own custom settings.


Requirements
Install locally with:

bash
Copy
Edit
pip install deap numpy matplotlib pandas pillow scikit-learn
# Optional GPU
pip install cupy-cuda11x


Author
Mazhar Ziadeh
Kadir Has University – Evolutionary Algorithms (Undergraduate Project)

For shaders, fractals, optimization, and procedural dreams.
