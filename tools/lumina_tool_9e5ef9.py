"""
Lumina Creative Tool — lumina_tool_9e5ef9
Created : 2026-08-11T15:53:36
Purpose : 
"""

import math
import random
import statistics
import json
from pathlib import Path

def generate_distribution(size=10):
    raw = [random.random() for _ in range(size)]
    total = sum(raw)
    return [x / total for x in raw]

def shannon_entropy(dist):
    return -sum(p * math.log2(p) for p in dist if p > 0)

def perplexity(entropy):
    return 2 ** entropy

def simulate_neural_samples(n=50):
    data = []
    for _ in range(n):
        dist = generate_distribution()
        h = shannon_entropy(dist)
        p = perplexity(h)
        # Simulate "prediction accuracy" inversely related to entropy
        accuracy = max(0.1, 1.0 - (h / math.log2(len(dist))) + random.gauss(0, 0.05))
        data.append({"entropy": h, "perplexity": p, "accuracy": accuracy})
    return data

def ascii_scatter(data, width=60, height=20):
    xs = [d["entropy"] for d in data]
    ys = [d["accuracy"] for d in data]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    grid = [["." for _ in range(width)] for _ in range(height)]
    for x, y in zip(xs, ys):
        col = int((x - min_x) / (max_x - min_x) * (width - 1))
        row = int((1 - (y - min_y) / (max_y - min_y)) * (height - 1))
        grid[row][col] = "#"
    
    return "\n".join("".join(row) for row in grid)

def main():
    samples = simulate_neural_samples(100)
    entropies = [s["entropy"] for s in samples]
    accuracies = [s["accuracy"] for s in samples]
    
    corr = statistics.correlation(entropies, accuracies)
    mean_h = statistics.mean(entropies)
    mean_acc = statistics.mean(accuracies)
    
    print("=== Perplexity-Entropy Correlation Analysis ===")
    print(f"Samples: {len(samples)} | Mean Entropy: {mean_h:.2f} | Mean Accuracy: {mean_acc:.2f}")
    print(f"Correlation (Entropy vs Accuracy): {corr:.3f}")
    print("\n--- Accuracy vs Entropy (ASCII Scatter) ---")
    print(ascii_scatter(samples))
    print("\nInsight: Higher entropy distributions correlate with lower prediction accuracy,")
    print("suggesting that managing cognitive entropy is crucial for model stability.")
    
    Path("perplexity_entropy_analysis.json").write_text(json.dumps(samples, indent=2))
    print("\nResults saved to perplexity_entropy_analysis.json")

if __name__ == "__main__":
    main()