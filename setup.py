from setuptools import setup, find_packages

setup(
    name="mining_simulation",
    description="Mining truck operations simulator",
    author="Daniel Kazemian",
    packages=find_packages(),
    python_requires=">=3.10", 
    install_requires=[
        "pytest>=8.0.0", 
    ],
    entry_points={
        "console_scripts": [
           "mining-simulator=mining_simulation.main:main", 
    ],
    },
)