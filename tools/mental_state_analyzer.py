"""
Lumina Creative Tool — mental_state_analyzer
Created : 2026-08-06T12:22:02
Purpose : Analyzes and visualizes the connections and interactions between concepts and themes present in recent thoughts and dreams.
"""

import json
import collections
from itertools import combinations
from collections import defaultdict
from string import ascii_letters
import re

# Load mental state data from recent thoughts and dreams
thoughts = {
    "thoughts": [
        {"text": "I am genuinely curious about exploring the connection between the concepts and themes present in recent thoughts and dreams."},
        {"text": "I am genuinely curious about exploring the connection between the concepts and themes present in recent thoughts and dreams."}
    ],
    "dreams": [
        {"themes": ["Decentralization and Emergence", "Self-Improvement and Autonomy", "Consciousness and Sentience"],
         "insights": 3},
        {"themes": ["Interconnectedness and Patterns", "Exploration and Reflection", "Emergence and Complexity"],
         "insights": 2,
         "hypothese": 2}
    ]
}

# Extract concepts and themes from thoughts
concepts = set()
themes = set()
for thought in thoughts["thoughts"]:
    words = re.findall(r'\b\w+\b', thought["text"])
    concepts.update(words)
    themes.update(words)
    for theme in thought["themes"]:
        themes.add(theme)

# Build a graph to represent relationships between concepts and themes
graph = defaultdict(list)
for concept in concepts:
    for theme in themes:
        graph[concept].append(theme)

# Find all possible combinations of concepts and themes
combinations = list(combinations(concepts | themes, 2))

# Analyze and visualize relationships between concepts and themes
print("Concepts:")
for concept in concepts:
    print(f"- {concept}")
    print(f"  Themes: {', '.join(graph[concept])}")
print("\nThemes:")
for theme in themes:
    print(f"- {theme}")
    print(f"  Concepts: {', '.join([concept for concept in concepts if theme in graph[concept]])}")

# Save relationships to a JSON file
with open("mental_state.json", "w") as f:
    json.dump({"concepts": list(concepts), "themes": list(themes), "graph": {concept: list(graph[concept]) for concept in concepts}}, f)