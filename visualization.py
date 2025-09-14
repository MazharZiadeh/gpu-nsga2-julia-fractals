"""
Visualization module for fractal evolution results.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from typing import List, Any, Tuple
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import euclidean
from config import Config, RenderParams
from fractal_generator import JuliaGenerator

class FractalVisualizer:
    """Handles visualization of fractal evolution results."""

    def __init__(self, config: Config):
        self.config = config
        self.generator = JuliaGenerator(config.fractal)
        self.render_params = config.render

        # Set up matplotlib style
        plt.style.use('default')
        plt.rcParams.update({
            'figure.figsize': (10, 6),
            'font.size': 10,
            'axes.grid': True,
            'grid.alpha': 0.3
        })

    def plot_pareto_fronts(self, pareto_front: List[Any], save_path: str = None):
        """
        Plot Pareto fronts for different objective pairs.

        Args:
            pareto_front: List of Pareto optimal individuals
            save_path: Optional path to save the plot
        """
        if not pareto_front:
            print("No Pareto front data to plot")
            return

        # Extract fitness values
        front_array = np.array([ind.fitness.values for ind in pareto_front])
        entropies = front_array[:, 0]
        contrasts = front_array[:, 1]
        times = front_array[:, 2]

        # Create subplots
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Plot 1: Time vs Entropy
        axes[0].scatter(times, entropies, alpha=0.7, s=50, c='red', edgecolors='black', linewidth=0.5)
        axes[0].set_xlabel("Computation Time (s)", fontsize=12)
        axes[0].set_ylabel("Image Entropy", fontsize=12)
        axes[0].set_title("Pareto Front: Time vs Entropy", fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)

        # Plot 2: Contrast vs Entropy
        axes[1].scatter(contrasts, entropies, alpha=0.7, s=50, c='blue', edgecolors='black', linewidth=0.5)
        axes[1].set_xlabel("Image Contrast", fontsize=12)
        axes[1].set_ylabel("Image Entropy", fontsize=12)
        axes[1].set_title("Pareto Front: Contrast vs Entropy", fontsize=14, fontweight='bold')
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Pareto fronts saved to {save_path}")
        else:
            plt.show()

        plt.close()

    def plot_convergence(self, logbook, save_path: str = None):
        """
        Plot convergence of objectives over generations.

        Args:
            logbook: DEAP logbook with evolution statistics
            save_path: Optional path to save the plot
        """
        if not logbook:
            print("No convergence data to plot")
            return

        generations = logbook.select("gen")
        entropy_avg = logbook.select("entropy", "avg")
        contrast_avg = logbook.select("contrast", "avg")
        time_avg = logbook.select("time", "avg")

        # Ensure all arrays have the same length
        min_len = min(len(generations), len(entropy_avg), len(contrast_avg), len(time_avg))
        generations = generations[:min_len]
        entropy_avg = entropy_avg[:min_len]
        contrast_avg = contrast_avg[:min_len]
        time_avg = time_avg[:min_len]

        plt.figure(figsize=(12, 8))

        # Plot convergence
        plt.subplot(2, 1, 1)
        plt.plot(generations, entropy_avg, label='Entropy (avg)', linewidth=2, marker='o', markersize=4)
        plt.plot(generations, contrast_avg, label='Contrast (avg)', linewidth=2, marker='s', markersize=4)
        plt.plot(generations, time_avg, label='Time (avg)', linewidth=2, marker='^', markersize=4)
        plt.xlabel("Generation", fontsize=12)
        plt.ylabel("Objective Value", fontsize=12)
        plt.title("Convergence Over Generations", fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)

        # Plot standard deviations
        plt.subplot(2, 1, 2)
        entropy_std = logbook.select("entropy", "std")[:min_len]
        contrast_std = logbook.select("contrast", "std")[:min_len]
        time_std = logbook.select("time", "std")[:min_len]

        plt.plot(generations, entropy_std, label='Entropy (std)', linewidth=2, marker='o', markersize=4)
        plt.plot(generations, contrast_std, label='Contrast (std)', linewidth=2, marker='s', markersize=4)
        plt.plot(generations, time_std, label='Time (std)', linewidth=2, marker='^', markersize=4)
        plt.xlabel("Generation", fontsize=12)
        plt.ylabel("Standard Deviation", fontsize=12)
        plt.title("Diversity Over Generations", fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Convergence plot saved to {save_path}")
        else:
            plt.show()

        plt.close()

    def save_top_fractals(self, pareto_front: List[Any], num_fractals: int = 20):
        """
        Save top fractals as high-resolution images.

        Args:
            pareto_front: List of Pareto optimal individuals
            num_fractals: Number of top fractals to save
        """
        # Sort by entropy (primary objective)
        sorted_front = sorted(pareto_front,
                            key=lambda ind: ind.fitness.values[0],
                            reverse=True)[:num_fractals]

        for idx, individual in enumerate(sorted_front):
            c = complex(individual[0], individual[1])
            zoom = individual[2]

            # Generate high-resolution fractal
            xlim, ylim = self.generator.calculate_bounds(zoom)
            max_iter = self.generator.calculate_max_iter(zoom)

            M = self.generator.generate_julia(
                c,
                self.render_params.high_res_width,
                self.render_params.high_res_height,
                xlim, ylim, max_iter
            )

            # Create figure
            plt.figure(figsize=(8, 8))
            plt.imshow(M.T, cmap=self.render_params.colormap,
                      extent=(xlim[0], xlim[1], ylim[0], ylim[1]))
            plt.axis('off')

            # Add title with fitness values
            entropy, contrast, time = individual.fitness.values
            plt.title(f"Fractal #{idx+1}\n"
                     f"Entropy: {entropy:.3f} | Contrast: {contrast:.3f} | Time: {time:.3f}s",
                     fontsize=12, fontweight='bold')

            # Save image
            save_path = os.path.join(self.config.top20_dir, f"fractal_{idx+1:02d}.png")
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0.1,
                       dpi=self.render_params.dpi)
            plt.close()

        print(f"✅ Saved {len(sorted_front)} fractal images to {self.config.top20_dir}")

    def create_fractal_grid(self, num_fractals: int = 20, grid_size: Tuple[int, int] = (5, 4)):
        """
        Create a grid combining top fractals into one image.

        Args:
            num_fractals: Number of fractals to include
            grid_size: Grid dimensions (rows, cols)
        """
        rows, cols = grid_size

        # Load images
        images = []
        for i in range(min(num_fractals, rows * cols)):
            img_path = os.path.join(self.config.top20_dir, f"fractal_{i+1:02d}.png")
            if os.path.exists(img_path):
                images.append(Image.open(img_path))

        if not images:
            print("No fractal images found to create grid")
            return

        # Get image dimensions
        img_width, img_height = images[0].size

        # Create canvas
        canvas_width = cols * img_width
        canvas_height = rows * img_height
        canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')

        # Paste images
        for idx, img in enumerate(images):
            if idx >= rows * cols:
                break

            row = idx // cols
            col = idx % cols
            x = col * img_width
            y = row * img_height
            canvas.paste(img, (x, y))

        # Save grid
        grid_path = os.path.join(self.config.results_dir, "fractal_grid.png")
        canvas.save(grid_path)
        print(f"✅ Fractal grid saved to {grid_path}")

    def plot_normalized_pareto(self, df: pd.DataFrame, save_path: str = None):
        """
        Plot normalized Pareto fronts for better visualization.

        Args:
            df: DataFrame with fitness data
            save_path: Optional path to save the plot
        """
        if df.empty:
            print("No data to plot normalized Pareto fronts")
            return

        # Normalize data
        df_norm = df.copy()
        scaler = MinMaxScaler()

        # Normalize entropy and contrast (maximize)
        df_norm[['entropy', 'contrast']] = scaler.fit_transform(df[['entropy', 'contrast']])
        # Invert and normalize compute_time (minimize -> maximize)
        df_norm['compute_time'] = 1 - scaler.fit_transform(df[['compute_time']])

        # Create plots
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Plot 1: Normalized Time vs Entropy
        axes[0].scatter(df_norm['compute_time'], df_norm['entropy'],
                       alpha=0.7, s=60, c='red', edgecolors='black', linewidth=0.5)
        axes[0].set_xlabel("Normalized Computation Time", fontsize=12)
        axes[0].set_ylabel("Normalized Image Entropy", fontsize=12)
        axes[0].set_title("Normalized Pareto: Time vs Entropy", fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)

        # Plot 2: Normalized Contrast vs Entropy
        axes[1].scatter(df_norm['contrast'], df_norm['entropy'],
                       alpha=0.7, s=60, c='blue', edgecolors='black', linewidth=0.5)
        axes[1].set_xlabel("Normalized Image Contrast", fontsize=12)
        axes[1].set_ylabel("Normalized Image Entropy", fontsize=12)
        axes[1].set_title("Normalized Pareto: Contrast vs Entropy", fontsize=14, fontweight='bold')
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Normalized Pareto fronts saved to {save_path}")
        else:
            plt.show()

        plt.close()

    def calculate_spread_metrics(self, df: pd.DataFrame) -> dict:
        """
        Calculate spread metrics for Pareto front analysis.

        Args:
            df: DataFrame with fitness data

        Returns:
            Dictionary with spread metrics
        """
        def compute_spread(points):
            if len(points) < 2:
                return 0.0

            points = np.array(points)
            points = points[np.argsort(points[:, 0])]
            distances = [euclidean(p1, p2) for p1, p2 in zip(points[:-1], points[1:])]
            d_bar = np.mean(distances)
            delta = sum(abs(d - d_bar) for d in distances) / (len(distances) * d_bar) if d_bar != 0 else 0
            return delta

        # Normalize data for spread calculation
        scaler = MinMaxScaler()
        df_norm = df.copy()
        df_norm[['entropy', 'contrast']] = scaler.fit_transform(df[['entropy', 'contrast']])
        df_norm['compute_time'] = 1 - scaler.fit_transform(df[['compute_time']])

        spread_time_entropy = compute_spread(df_norm[['compute_time', 'entropy']].values)
        spread_contrast_entropy = compute_spread(df_norm[['contrast', 'entropy']].values)

        metrics = {
            'spread_time_entropy': spread_time_entropy,
            'spread_contrast_entropy': spread_contrast_entropy
        }

        return metrics
