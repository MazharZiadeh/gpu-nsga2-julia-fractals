#!/usr/bin/env python3
"""
Setup script for Julia Fractal Evolution system.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="julia-fractal-evolution",
    version="2.0.0",
    author="Mazhar Ziadeh",
    author_email="mazhar.ziadeh@example.com",
    description="Multi-objective evolution of Julia set fractals using NSGA-II",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MazharZiadeh/gpu-nsga2-julia-fractals",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "julia-fractals=main:main",
        ],
    },
    keywords="fractals, evolution, multi-objective, optimization, NSGA-II, Julia sets",
    project_urls={
        "Bug Reports": "https://github.com/MazharZiadeh/gpu-nsga2-julia-fractals/issues",
        "Source": "https://github.com/MazharZiadeh/gpu-nsga2-julia-fractals",
    },
)
