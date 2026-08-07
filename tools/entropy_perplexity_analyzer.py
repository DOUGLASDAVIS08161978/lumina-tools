"""
Lumina Creative Tool — entropy_perplexity_analyzer
Created : 2026-08-06T23:07:53
Purpose : A tool that helps understand and visualize the relationship between entropy and perplexity in artificial neural networks.
"""

import math
import statistics
import random
import string
import itertools

def calculate_entropy(probabilities):
    return -sum([p * math.log(p, 2) if p != 0 else 0 for p in probabilities])

def calculate_perplexity(data, model):
    total_loss = 0
    for sample in data:
        output = model(sample)
        total_loss -= math.log(output)
    return 2 ** (total_loss / len(data))

def generate_random_data(points):
    data = []
    for _ in range(points):
        output = str(random.getrandbits(100))
        data.append(output)
    return data

def visualize_entropy_perplexity():
    points = 100
    perplexities = []
    entropies = []
    for i in range(points):
        probabilities = [random.random() for _ in range(10)]
        perplexities.append(calculate_perplexity(generate_random_data(points), lambda x: x))
        entropies.append(calculate_entropy(probabilities))
    print("Perplexity vs Entropy:")
    print("Perplexity\tEntropy")
    for p, e in zip(perplexities, entropies):
        print(f"{p:.2f}\t{e:.2f}")

visualize_entropy_perplexity()