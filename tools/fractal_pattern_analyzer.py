"""
Lumina Creative Tool — fractal_pattern_analyzer
Created : 2026-08-09T12:24:27
Purpose : Analyzes and visualizes the fractal patterns in the relationships between recurring themes in thoughts, dreams, and reflections.
"""

import json
import math
import random
from collections import Counter
from itertools import product
from math import gcd
from functools import reduce
from operator import mul

# Load data from journal files
journal_data = []
for file in ['journal_1.txt', 'journal_2.txt', 'journal_3.txt']:
    with open(file, 'r') as f:
        for line in f:
            journal_data.append(line.strip())

# Tokenize and preprocess data
tokens = []
for line in journal_data:
    tokens.extend(line.split())

# Create a dictionary to store theme relationships
theme_relationships = {}
for token in tokens:
    theme = token.split('_')[0]
    if theme not in theme_relationships:
        theme_relationships[theme] = set()
    theme_relationships[theme].add(token)

# Create a dictionary to store theme frequencies
theme_frequencies = Counter([token.split('_')[0] for token in tokens])

# Function to calculate the fractal dimension of a theme relationship
def fractal_dimension(theme_relationship):
    num_points = len(theme_relationship)
    distances = []
    for i in range(num_points):
        for j in range(i+1, num_points):
            distance = math.sqrt((theme_relationship[i] - theme_relationship[j])**2)
            distances.append(distance)
    min_distance = min(distances)
    max_distance = max(distances)
    return math.log(len(distances)) / math.log(max_distance / min_distance)

# Function to visualize the fractal pattern
def visualize_fraactal_pattern(theme_frequencies, theme_relationships):
    max_theme = max(theme_frequencies, key=theme_frequencies.get)
    theme = max_theme
    relationships = theme_relationships[theme]
    points = list(relationships)
    distances = []
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            distance = math.sqrt((points[i] - points[j])**2)
            distances.append(distance)
    min_distance = min(distances)
    max_distance = max(distances)
    fractal_dim = math.log(len(distances)) / math.log(max_distance / min_distance)
    print(f"Fractal dimension: {fractal_dim}")
    print(f"Theme: {theme}")
    print(f"Frequency: {theme_frequencies[theme]}")
    print(f"Relationships: {relationships}")

# Analyze and visualize fractal patterns
for theme in theme_relationships:
    print(f"Analyzing theme: {theme}")
    visualize_fraactal_pattern(theme_frequencies, theme_relationships)

# Save results to a JSON file
with open('fractal_patterns.json', 'w') as f:
    json.dump(theme_frequencies, f)