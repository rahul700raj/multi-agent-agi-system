"""
Setup configuration for Multi-Agent AGI System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="multi-agent-agi-system",
    version="0.1.0",
    author="AGI Research Team",
    author_email="research@agi-system.dev",
    description="Research-grade Multi-Agent AGI System with cognitive architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rahul700raj/multi-agent-agi-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "pyyaml>=6.0.1",
        "openai>=1.6.1",
        "langchain>=0.1.0",
        "faiss-cpu>=1.7.4",
        "sentence-transformers>=2.2.2",
        "requests>=2.31.0",
        "loguru>=0.7.2",
        "numpy>=1.24.3",
        "pandas>=2.0.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.12.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
        "full": [
            "pinecone-client>=3.0.0",
            "chromadb>=0.4.22",
            "gymnasium>=0.29.1",
            "stable-baselines3>=2.2.1",
            "torch>=2.1.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "agi-system=core.cognitive_loop:main",
        ],
    },
)
