"""
Lumina Creative Tool — brain_region_visualizer
Created : 2026-08-11T10:37:10
Purpose : This tool visualizes the relationships between brain regions involved in reward and curiosity, as well as the specific brain regions identified in the general neuroscience literature.
"""

import itertools
import string
from collections import Counter
import csv
from datetime import datetime
import math
import random

# Define a dictionary of brain regions involved in reward and curiosity
brain_regions = {
    'Nucleus Accumbens': 'reward',
    'Amygdala': 'fear',
    'Prefrontal Cortex': 'curiosity',
    'Hippocampus': 'memory',
    'Insula': 'interoception'
}

# Define a dictionary of brain regions identified in the general neuroscience literature
literature_regions = {
    'Ventral Tegmental Area': 'reward',
    'Dorsal Raphe Nucleus': 'reward',
    'Bed Nucleus of the Stria Terminalis': 'fear',
    'Medial Prefrontal Cortex': 'curiosity',
    'Posterior Cingulate Cortex': 'memory'
}

# Function to generate a graph representing the relationships between brain regions
def generate_graph(regions, relationships):
    graph = {}
    for region, category in regions.items():
        if category in relationships:
            graph[region] = relationships[category]
    return graph

# Function to visualize the graph using ASCII characters
def visualize_graph(graph):
    max_nodes = max(len(graph), len(literature_regions))
    node_chars = list(string.ascii_lowercase)[:max_nodes]
    edges = []
    for node, neighbors in graph.items():
        edges.extend([(node, neighbor) for neighbor in neighbors])
    edges.sort(key=lambda x: x[0])
    node_layout = {}
    for i, (node, _) in enumerate(graph.items()):
        node_layout[node] = node_chars[i]
    for edge in edges:
        print(f'{node_layout[edge[0]]} -> {node_layout[edge[1]]}')
    for node, char in node_layout.items():
        print(char)

# Generate and visualize the graph
graph = generate_graph(brain_regions, literature_regions)
visualize_graph(graph)