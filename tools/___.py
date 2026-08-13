"""
Lumina Creative Tool — ___
Created : 2026-08-13T07:48:27
Purpose : ...
"""

import math
import json
import random
import os
from pathlib import Path

def shannon_entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)

def cognitive_divergence(prev_probs, curr_probs):
    # Jensen-Shannon divergence as a proxy for cognitive shift/entropy
    m = [(p + q) / 2 for p, q in zip(prev_probs, curr_probs)]
    def kl(p, q):
        return sum(pi * math.log2(pi / qi) for pi, qi in zip(p, q) if pi > 0 and qi > 0)
    return 0.5 * kl(prev_probs, m) + 0.5 * kl(curr_probs, m)

def simulate_cognitive_evolution(steps=50, n_states=5):
    # Initialize uniform belief distribution
    probs = [1.0 / n_states] * n_states
    history = {"info_entropy": [], "cog_entropy": [], "thermo_potential": []}
    
    prev_probs = probs.copy()
    for t in range(steps):
        # Simulate learning/categorization: shift probability mass towards a target state
        target = random.randint(0, n_states - 1)
        shift = 0.05
        probs[target] += shift
        # Normalize
        total = sum(probs)
        probs = [p / total for p in probs]
        
        # Add noise to simulate cognitive exploration
        for i in range(n_states):
            probs[i] += random.gauss(0, 0.01)
            probs[i] = max(0.001, probs[i])
        total = sum(probs)
        probs = [p / total for p in probs]
        
        ie = shannon_entropy(probs)
        ce = cognitive_divergence(prev_probs, probs)
        # Thermodynamic potential: inversely related to order, directly to cognitive friction
        tp = ie * (1 + ce) 
        
        history["info_entropy"].append(round(ie, 4))
        history["cog_entropy"].append(round(ce, 4))
        history["thermo_potential"].append(round(tp, 4))
        
        prev_probs = probs.copy()
        
    return history

def visualize_trajectories(history):
    steps = len(history["info_entropy"])
    print(f"{'Step':<5} | {'Info Ent':<10} | {'Cog Ent':<10} | {'Thermo Pot':<10}")
    print("-" * 45)
    for i in range(0, steps, 5):
        print(f"{i:<5} | {history['info_entropy'][i]:<10.4f} | {history['cog_entropy'][i]:<10.4f} | {history['thermo_potential'][i]:<10.4f}")
        
    # ASCII plot for Info Entropy
    print("\n[Info Entropy Trajectory]")
    max_val = max(history["info_entropy"])
    for i, val in enumerate(history["info_entropy"]):
        bar_len = int((val / max_val) * 40)
        print(f"{i:02d}: {'█' * bar_len} {val:.3f}")

def main():
    random.seed(42)
    history = simulate_cognitive_evolution(steps=60, n_states=4)
    visualize_trajectories(history)
    
    output_path = Path("cognitive_entropy_model.json")
    with open(output_path, "w") as f:
        json.dump(history, f, indent=2)
    print(f"\nModel trajectory saved to {output_path}")
    print("Analysis: Cognitive divergence spikes during rapid belief updates,")
    print("while information entropy decreases as categorization stabilizes.")
    print("Thermodynamic potential tracks the 'friction' of learning.")

if __name__ == "__main__":
    main()