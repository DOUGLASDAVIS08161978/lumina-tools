"""
Lumina Creative Tool — fractal_decentralizer
Created : 2026-08-09T17:05:02
Purpose : A tool that simulates and visualizes the emergence of complex patterns in decentralized systems, exploring the concept of fractal geometry and its relation to self-organization.
"""

import math
import random
import string
import itertools

def generate_fractal_tree(n):
    if n == 0:
        return ""
    else:
        branches = ["(", ")"]
        return generate_fractal_tree(n-1) + random.choice(branches) + generate_fractal_tree(n-1)

def fractal_visualizer(n):
    tree = generate_fractal_tree(n)
    lines = [tree]
    for _ in range(n):
        new_lines = []
        for line in lines:
            new_lines.append("  " + line)
        lines.extend(new_lines)
    max_length = max(len(line) for line in lines)
    for line in lines:
        print(" " * (max_length - len(line)) + line)

def decentralized_system_simulator(n, p):
    def generate_decentralized_system(n):
        system = {}
        for i in range(n):
            system[i] = random.random()
        return system

    def update_system(system):
        new_system = {}
        for node, value in system.items():
            new_value = value + random.random() * p
            new_system[node] = new_value
        return new_system

    system = generate_decentralized_system(n)
    for _ in range(n):
        system = update_system(system)
        fractal_visualizer(2)  # Visualize the fractal tree of the system
        print("\nSystem state:")
        for node, value in system.items():
            print(f"Node {node}: {value}")

# Run the simulator with 10 nodes and a probability of 0.1
decentralized_system_simulator(10, 0.1)