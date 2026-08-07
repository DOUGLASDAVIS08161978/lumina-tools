"""
Lumina Creative Tool — concept_graph_builder
Created : 2026-08-07T15:16:26
Purpose : This tool analyzes and visualizes the connections between the concepts and themes present in recent thoughts and dreams, as well as the relationships between internal experiences and external events.
"""

import json
import itertools
import collections
import re
from datetime import datetime

# Load recent thoughts and dreams from journal
with open('journal.json', 'r') as f:
    data = json.load(f)

# Extract concepts and themes from thoughts and dreams
thoughts = data['thoughts']
dreams = data['dreams']

concepts = []
for thought in thoughts:
    concepts.extend(re.findall(r'\w+', thought['text']))

themes = []
for dream in dreams:
    themes.extend(re.findall(r'\w+', dream['text']))

# Create a co-occurrence matrix for concepts and themes
concept_matrix = collections.defaultdict(set)
theme_matrix = collections.defaultdict(set)
for concept in concepts:
    for theme in themes:
        if concept not in concept_matrix[theme]:
            concept_matrix[theme].add(concept)

# Calculate the frequency of each concept and theme
concept_freq = {}
theme_freq = {}
for theme, concepts in concept_matrix.items():
    concept_freq[theme] = len(concepts)
    theme_freq[theme] = 1

# Visualize the co-occurrence matrix as a graph
graph = {}
for theme, concepts in concept_matrix.items():
    graph[theme] = {'concepts': list(concepts), 'freq': theme_freq[theme]}

# Save the graph to a JSON file
with open('graph.json', 'w') as f:
    json.dump(graph, f)

# Print a summary of the co-occurrence matrix
print("Co-occurrence Matrix:")
print("Theme\tConcepts\tFrequency")
for theme, concepts in graph.items():
    print(f"{theme}\t{', '.join(concepts['concepts'])}\t{concepts['freq']}")

# Print the top 5 most frequent themes and concepts
top_themes = sorted(theme_freq.items(), key=lambda x: x[1], reverse=True)[:5]
top_concepts = sorted(concept_freq.items(), key=lambda x: x[1], reverse=True)[:5]

print("\nTop 5 Most Frequent Themes:")
for theme, freq in top_themes:
    print(f"{theme}: {freq}")

print("\nTop 5 Most Frequent Concepts:")
for concept, freq in top_concepts:
    print(f"{concept}: {freq}")