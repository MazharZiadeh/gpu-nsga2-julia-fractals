# 🔮 GPU-NSGA2-Julia-Fractals

> A professional, multi-objective evolutionary framework for generating high-complexity Julia-set fractals using NSGA-II. Built with clean architecture, comprehensive visualization, and production-ready code quality.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🚀 Overview

This project implements a sophisticated **evolutionary generator for Julia-set fractals** optimized across **three competing objectives**:

* 🧠 **Image Entropy** (maximize visual complexity)
* 🌈 **Image Contrast** (maximize perceptual sharpness)
* ⏱️ **Computation Time** (minimize rendering cost)

Utilizing **NSGA-II** from the DEAP library, it evolves fractal configurations (complex constant and zoom level) to explore Pareto-optimal sets with professional-grade visualization and analysis tools.

### ✨ Key Features

- **Clean Architecture**: Modular, well-documented codebase with proper separation of concerns
- **Professional CLI**: Command-line interface with multiple scenarios and options
- **Comprehensive Visualization**: Pareto fronts, convergence plots, and high-quality fractal images
- **Flexible Configuration**: Easy-to-modify parameters for different optimization strategies
- **Production Ready**: Error handling, logging, and robust file management
- **Local Execution**: No Google Colab dependencies - runs on any Python environment

## 🔍 Experimental Scenarios

| Scenario | Purpose | Description | Population | Generations |
|----------|---------|-------------|------------|-------------|
| **S1** | Entropy Optimization | Prioritize complex visual patterns | μ=30, λ=70 | 30 |
| **S2** | Contrast vs Time | Balance clarity and runtime | μ=70, λ=30 | 25 |
| **S3** | Full Multi-objective | Explore all objectives in Pareto front | μ=50, λ=50 | 20 |

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MazharZiadeh/gpu-nsga2-julia-fractals.git
   cd gpu-nsga2-julia-fractals
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the evolution:**
   ```bash
   python main.py --scenario S3
   ```

### Optional GPU Acceleration

For faster computation with NVIDIA GPUs:
```bash
pip install cupy-cuda11x  # For CUDA 11.x
# or
pip install cupy-cuda12x  # For CUDA 12.x
```

## 📈 Usage

### Command Line Interface

```bash
# Run with default scenario (S3)
python main.py

# Run specific scenario
python main.py --scenario S1

# Quiet mode (minimal output)
python main.py --scenario S2 --quiet

# List available scenarios
python main.py --list-scenarios

# Get help
python main.py --help
```

### Programmatic Usage

```python
from config import get_config
from evolution_engine import EvolutionEngine
from visualization import FractalVisualizer

# Get configuration
config = get_config("S3")

# Initialize and run evolution
engine = EvolutionEngine(config)
final_population = engine.evolve(verbose=True)
pareto_front = engine.get_pareto_front()

# Create visualizations
visualizer = FractalVisualizer(config)
visualizer.save_top_fractals(pareto_front)
visualizer.plot_pareto_fronts(pareto_front)
```

## 📁 Output Structure

```
results/
├── evolution_results.xlsx          # Fitness data and metadata
├── convergence.png                 # Evolution convergence plot
├── fractal_grid.png               # 4×5 grid of best fractals
├── spread_metrics.txt             # Pareto front spread metrics
├── top20/                         # High-resolution fractal images
│   ├── fractal_01.png
│   ├── fractal_02.png
│   └── ...
└── pareto_fronts/                 # Pareto front visualizations
    ├── pareto_fronts.png          # Raw Pareto fronts
    └── normalized_pareto.png      # Normalized Pareto fronts
```

## 🏗️ Architecture

The project follows a clean, modular architecture:

```
├── main.py                 # CLI entry point
├── config.py              # Configuration management
├── fractal_generator.py   # Julia set generation and evaluation
├── evolution_engine.py    # NSGA-II evolutionary algorithm
├── visualization.py       # Plotting and image generation
├── requirements.txt       # Dependencies
└── README.md             # This file
```

### Core Components

- **`JuliaGenerator`**: Generates Julia set fractals with configurable parameters
- **`FractalEvaluator`**: Calculates multi-objective fitness (entropy, contrast, time)
- **`EvolutionEngine`**: Implements NSGA-II with DEAP framework
- **`FractalVisualizer`**: Creates professional plots and saves high-quality images

## 🧠 Algorithm Details

### Multi-Objective Optimization

The system optimizes three competing objectives:

1. **Image Entropy**: Measures visual complexity using Shannon entropy of escape time distribution
2. **Image Contrast**: Quantifies perceptual sharpness using standard deviation of normalized values
3. **Computation Time**: Tracks rendering performance for efficiency

### NSGA-II Implementation

- **Selection**: Non-dominated sorting with crowding distance
- **Crossover**: Blend crossover with α=0.5
- **Mutation**: Gaussian mutation with σ=0.2
- **Population Management**: (μ + λ) selection strategy

## 📊 Results Analysis

### Pareto Front Analysis

The system provides comprehensive Pareto front analysis:

- **Raw Pareto Fronts**: Direct visualization of objective trade-offs
- **Normalized Pareto Fronts**: Min-max normalized for better comparison
- **Spread Metrics**: Quantify diversity of Pareto optimal solutions
- **Convergence Analysis**: Track evolution progress over generations

### Performance Metrics

- **Hypervolume**: Measures Pareto front quality (when available)
- **Spread**: Quantifies solution diversity
- **Convergence**: Tracks objective improvement over time

## 🛠️ Configuration

### Customizing Evolution Parameters

Edit `config.py` to modify:

```python
@dataclass
class EvolutionParams:
    mu: int = 50          # Population size
    lambda_: int = 50     # Offspring size
    cxpb: float = 0.7     # Crossover probability
    mutpb: float = 0.2    # Mutation probability
    ngen: int = 20        # Number of generations
```

### Fractal Generation Settings

```python
@dataclass
class FractalParams:
    width: int = 200                    # Default resolution
    height: int = 200
    max_iter_base: int = 100           # Base iteration count
    zoom_range: Tuple[float, float] = (0.5, 5.0)      # Zoom limits
    c_real_range: Tuple[float, float] = (-1.0, 1.0)   # Real part limits
    c_imag_range: Tuple[float, float] = (-1.0, 1.0)   # Imaginary part limits
```

## 🧬 Citation

If you use this project in your research, please cite:

```bibtex
@misc{ziadeh2025julia,
  title={GPU-NSGA2-Julia-Fractals: Multi-objective Evolution of Visual Complexity},
  author={Ziadeh, Mazhar},
  year={2025},
  howpublished={\url{https://github.com/MazharZiadeh/gpu-nsga2-julia-fractals}},
  note={Multi-objective evolutionary optimization of Julia set fractals using NSGA-II}
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies: `pip install -r requirements.txt`
4. Make your changes
5. Run tests (if available)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **DEAP Team**: For the excellent evolutionary algorithms framework
- **NumPy/SciPy**: For numerical computing foundations
- **Matplotlib**: For visualization capabilities
- **Inspired by**: [Saupe & Ruhl, 1996] on evolutionary fractal compression

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/MazharZiadeh/gpu-nsga2-julia-fractals/issues) page
2. Create a new issue with detailed information
3. Include your Python version, operating system, and error messages

---

**Made with ❤️ by [Mazhar Ziadeh](https://github.com/MazharZiadeh)**
