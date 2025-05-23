

# 🔮 GPU-NSGA2-Julia-Fractals

> A GPU-accelerated, multi-objective evolutionary framework for generating high-complexity Julia-set fractals using NSGA-II. Built for Google Colab with DEAP, NumPy, and optional CuPy acceleration.

---

## 🚀 Overview

This project implements an **evolutionary generator for Julia-set fractals** optimized across **three competing objectives**:

* 🧠 **Image Entropy** (maximize visual complexity)
* 🌈 **Image Contrast** (maximize perceptual sharpness)
* ⏱️ **Computation Time** (minimize rendering cost)

Utilizing **NSGA-II** from the DEAP library, it evolves fractal configurations (complex constant and zoom level) to explore Pareto-optimal sets in real-time. Results include:

* Ranked top-20 fractals saved as images
* Excel exports of generation-wise fitness data
* Composite 5×4 grid of elite images
* Interactive plots of Pareto fronts and convergence

---

## 🔍 Experimental Scenarios

| Scenario | Purpose              | Description                                              |
| -------- | -------------------- | -------------------------------------------------------- |
| 1        | Entropy Optimization | Prioritize complex visual patterns                       |
| 2        | Contrast vs Time     | Balance between clarity and runtime                      |
| 3        | Full Multi-objective | Explore all three objectives in a Pareto front formation |

---

## ⚙️ Requirements

* Google Colab (recommended)
* Python 3.11
* DEAP, NumPy, Matplotlib, Pandas
* CuPy (optional, for GPU speedup)

Install dependencies (if running locally):

```bash
pip install deap numpy pandas matplotlib
# Optional:
pip install cupy
```

---

## 📁 Output Structure

* `results/`

  * `top20/` – Best 20 fractal images
  * `grid_top20.png` – Final composite image (5x4 layout)
  * `evolution_results.xlsx` – Fitness + metadata (generation, scores)
  * `pareto_fronts/` – Normalized Pareto plots per objective

---

## 📈 Usage

1. Run `fractals.ipynb` in Google Colab
2. Select the scenario and set hyperparameters
3. Monitor live evolution plots
4. Download your best-ranked fractals

---

## 🧠 Citation

If you use this project in your work, please cite:

```
Ziadeh, M. (2025). GPU-NSGA2-Julia-Fractals: Multi-objective Evolution of Visual Complexity. https://github.com/MazharZiadeh/gpu-nsga2-julia-fractals
```

---

## 🧬 Credits

* **Mazhar Ziadeh** – Evolutionary algorithm design, fractal rendering engine, NSGA-II tuning
* Inspired by \[Saupe & Ruhl, 1996] on evolutionary fractal compression

---

