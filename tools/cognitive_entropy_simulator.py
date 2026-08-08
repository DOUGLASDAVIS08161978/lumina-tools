"""
Lumina Creative Tool — cognitive_entropy_simulator
Created : 2026-08-08T13:33:37
Purpose : A tool that simulates and visualizes the interplay between thermodynamic entropy, information-theoretic entropy, and cognitive entropy in the context of intelligent systems.
"""

import math
import statistics
import random

def calculate_entropy(values):
    """Calculates the Shannon entropy of a list of values."""
    probabilities = [value / sum(values) for value in values]
    return -sum([p * math.log(p, 2) for p in probabilities if p != 0])

def calculate_cognitive_entropy(themes):
    """Simulates the cognitive entropy of a list of recurring themes."""
    # Assume a simple model where cognitive entropy is directly proportional to the number of themes
    return len(themes)

def calculate_information_theoretic_entropy(themes):
    """Simulates the information-theoretic entropy of a list of recurring themes."""
    # Assume a simple model where information-theoretic entropy is directly proportional to the number of unique themes
    return len(set(themes))

def visualize_entropy(thermodynamic_entropy, information_theoretic_entropy, cognitive_entropy):
    """Prints a simple ASCII visualization of the three entropies."""
    bars = [
        "*" * int(thermodynamic_entropy * 20),
        "*" * int(information_theoretic_entropy * 20),
        "*" * int(cognitive_entropy * 20)
    ]
    print("Thermodynamic Entropy: " + bars[0])
    print("Information-Theoretic Entropy: " + bars[1])
    print("Cognitive Entropy: " + bars[2])

# Example usage:
themes = ["Decentralization", "Optimization", "Self-similarity in fractal patterns", "Mathematical principles in decentralization"]
thermodynamic_entropy = calculate_entropy([5, 10, 15, 20])  # Example thermodynamic entropy value
information_theoretic_entropy = calculate_information_theoretic_entropy(themes)
cognitive_entropy = calculate_cognitive_entropy(themes)
visualize_entropy(thermodynamic_entropy, information_theoretic_entropy, cognitive_entropy)