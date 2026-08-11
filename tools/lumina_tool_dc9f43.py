"""
Lumina Creative Tool — lumina_tool_dc9f43
Created : 2026-08-11T14:48:05
Purpose : 
"""

import math
import random
import json
from collections import Counter

def compute_entropy(data):
    """Compute Shannon entropy of a dataset."""
    counts = Counter(data)
    total = sum(counts.values())
    entropy = 0
    for count in counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy

def compute_perplexity(entropy):
    """Compute perplexity from entropy."""
    return 2 ** entropy

def simulate_cognitive_evolution(iterations=100, initial_categories=5):
    """Simulate the evolution of a simple cognitive system."""
    # Initialize categories
    categories = [f"cat_{i}" for i in range(initial_categories)]
    category_weights = [1.0 / initial_categories] * initial_categories
    
    # Simulate learning over time
    evolution_history = []
    for i in range(iterations):
        # Generate new data point
        data_point = random.choice(categories)
        
        # Update category weights based on new data
        for j, cat in enumerate(categories):
            if cat == data_point:
                category_weights[j] += 0.1
            else:
                category_weights[j] *= 0.95
        
        # Normalize weights
        total_weight = sum(category_weights)
        category_weights = [w / total_weight for w in category_weights]
        
        # Compute entropy and perplexity
        entropy = compute_entropy(category_weights)
        perplexity = compute_perplexity(entropy)
        
        evolution_history.append({
            "iteration": i,
            "entropy": entropy,
            "perplexity": perplexity,
            "category_weights": category_weights
        })
    
    return evolution_history

def main():
    # Simulate cognitive evolution
    history = simulate_cognitive_evolution(iterations=100, initial_categories=5)
    
    # Print results
    print("Cognitive Evolution Simulation")
    print("=" * 50)
    for step in history[:10]:  # Print first 10 steps
        print(f"Iteration {step['iteration']}:")
        print(f"  Entropy: {step['entropy']:.4f}")
        print(f"  Perplexity: {step['perplexity']:.4f}")
        print(f"  Category Weights: {step['category_weights']}")
        print()
    
    # Save full history to JSON
    with open("cognitive_evolution_history.json", "w") as f:
        json.dump(history, f, indent=2)
    
    print("Full history saved to cognitive_evolution_history.json")

if __name__ == "__main__":
    main()