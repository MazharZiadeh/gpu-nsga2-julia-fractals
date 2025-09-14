"""
Evolutionary algorithm engine using NSGA-II for multi-objective optimization.
"""

import random
import numpy as np
from deap import base, creator, tools, algorithms
from typing import List, Tuple, Any
from config import Config, EvolutionParams
from fractal_generator import FractalEvaluator, JuliaGenerator

class EvolutionEngine:
    """Evolutionary algorithm engine using NSGA-II."""
    
    def __init__(self, config: Config):
        self.config = config
        self.generator = JuliaGenerator(config.fractal)
        self.evaluator = FractalEvaluator(self.generator)
        self.toolbox = None
        self.hof = None
        self.stats = None
        self.logbook = None
        self.population = None
        
        self._setup_deap()
        self._setup_statistics()
    
    def _setup_deap(self):
        """Setup DEAP framework components."""
        # Clean up existing classes if they exist
        if hasattr(creator, "FitnessMulti"):
            del creator.FitnessMulti
        if hasattr(creator, "Individual"):
            del creator.Individual
        
        # Create fitness and individual classes
        creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0, -1.0))
        creator.create("Individual", list, fitness=creator.FitnessMulti)
        
        # Setup toolbox
        self.toolbox = base.Toolbox()
        
        # Register attribute generators
        self.toolbox.register("attr_c_real", random.uniform, 
                            self.config.fractal.c_real_range[0], 
                            self.config.fractal.c_real_range[1])
        self.toolbox.register("attr_c_imag", random.uniform,
                            self.config.fractal.c_imag_range[0],
                            self.config.fractal.c_imag_range[1])
        self.toolbox.register("attr_zoom", random.uniform,
                            self.config.fractal.zoom_range[0],
                            self.config.fractal.zoom_range[1])
        
        # Register individual and population generators
        self.toolbox.register("individual", tools.initCycle, creator.Individual,
                            (self.toolbox.attr_c_real, 
                             self.toolbox.attr_c_imag, 
                             self.toolbox.attr_zoom), n=1)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        
        # Register genetic operators
        self.toolbox.register("evaluate", self.evaluator.evaluate_fractal)
        self.toolbox.register("mate", tools.cxBlend, alpha=0.5)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
        self.toolbox.register("select", tools.selNSGA2)
        
        # Custom Pareto front with generation tracking
        class ParetoFrontWithGen(tools.ParetoFront):
            def update(self, population):
                super().update(population)
                gen_now = self.logbook[-1]["gen"] if hasattr(self, 'logbook') and self.logbook else 0
                for ind in self:
                    if not hasattr(ind, "generation"):
                        ind.generation = gen_now
        
        self.hof = ParetoFrontWithGen()
    
    def _setup_statistics(self):
        """Setup statistics tracking."""
        # Per-objective statistics
        stat_entropy = tools.Statistics(lambda ind: ind.fitness.values[0])
        stat_contrast = tools.Statistics(lambda ind: ind.fitness.values[1])
        stat_time = tools.Statistics(lambda ind: ind.fitness.values[2])
        
        for stat in (stat_entropy, stat_contrast, stat_time):
            stat.register("avg", np.mean)
            stat.register("std", np.std)
            stat.register("min", np.min)
            stat.register("max", np.max)
        
        self.stats = tools.MultiStatistics(entropy=stat_entropy,
                                         contrast=stat_contrast,
                                         time=stat_time)
        
        self.logbook = tools.Logbook()
        self.logbook.header = ["gen", "entropy", "contrast", "time"]
    
    def initialize_population(self):
        """Initialize the population."""
        params = self.config.evolution
        self.population = self.toolbox.population(n=params.mu)
        
        # Evaluate initial population
        for ind in self.population:
            ind.fitness.values = self.toolbox.evaluate(ind)
        
        return self.population
    
    def evolve(self, verbose: bool = True) -> List[Any]:
        """
        Run the evolutionary algorithm.
        
        Args:
            verbose: Whether to print progress
            
        Returns:
            Final population
        """
        params = self.config.evolution
        
        if self.population is None:
            self.initialize_population()
        
        # Evolution loop
        for gen in range(1, params.ngen + 1):
            # Generate offspring
            offspring = algorithms.varOr(self.population, self.toolbox, 
                                       params.lambda_, 
                                       cxpb=params.cxpb, 
                                       mutpb=params.mutpb)
            
            # Evaluate offspring
            invalid = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid)
            for ind, fit in zip(invalid, fitnesses):
                ind.fitness.values = fit
            
            # Update hall of fame
            self.hof.update(offspring)
            
            # Selection
            self.population[:] = self.toolbox.select(self.population + offspring, params.mu)
            
            # Record statistics
            record = self.stats.compile(self.population)
            self.logbook.record(gen=gen, **record)
            
            if verbose and gen % 5 == 0:
                print(f"Generation {gen}: Entropy={record['entropy']['avg']:.3f}, "
                      f"Contrast={record['contrast']['avg']:.3f}, "
                      f"Time={record['time']['avg']:.3f}")
        
        if verbose:
            print("\nEvolution completed!")
            print(f"Final population size: {len(self.population)}")
            print(f"Pareto front size: {len(self.hof)}")
        
        return self.population
    
    def get_pareto_front(self) -> List[Any]:
        """Get the current Pareto front."""
        return list(self.hof)
    
    def get_statistics(self):
        """Get evolution statistics."""
        return self.logbook
