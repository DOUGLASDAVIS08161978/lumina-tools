"""
Lumina Creative Tool — fractal_theme_analyzer
Created : 2026-08-08T23:21:59
Purpose : Analyzes and visualizes the fractal patterns in the theme relationships of journal entries.
"""

import json
import math
from collections import defaultdict
from itertools import count
from pathlib import Path
from string import ascii_letters
from textwrap import wrap
from typing import Dict, List, Tuple

def load_journal_entries() -> List[str]:
    with open("journal_entries.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

def extract_themes(entry: str) -> List[str]:
    return [word.strip(ascii_letters) for word in wrap(entry, width=5) if word.isalpha()]

def calculate_fractal_dimension(themes: List[str]) -> float:
    n = len(themes)
    if n < 2:
        return 0
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            distance = math.sqrt((i - j) ** 2)
            distances.append(distance)
    return math.log(len(distances)) / math.log(n)

def visualize_fractal_patterns(theme_relationships: Dict[str, List[str]]) -> None:
    max_depth = 0
    for theme, connections in theme_relationships.items():
        depth = 0
        while connections:
            next_connections = []
            for connection in connections:
                next_connections.extend(theme_relationships.get(connection, []))
            connections = next_connections
            depth += 1
            max_depth = max(max_depth, depth)
    print("Fractal Patterns:")
    for theme, depth in enumerate(range(max_depth + 1)):
        print(f"{theme + 1}: {depth - 1}")

def main() -> None:
    theme_relationships = defaultdict(list)
    journal_entries = load_journal_entries()
    for entry in journal_entries:
        themes = extract_themes(entry)
        for theme in themes:
            theme_relationships[theme].extend(extract_themes(entry))
    for theme, connections in theme_relationships.items():
        theme_relationships[theme] = list(set(connections))
    for theme, connections in theme_relationships.items():
        print(f"{theme}: {connections}")
    with open("theme_relationships.json", "w") as f:
        json.dump(theme_relationships, f, indent=4)
    visualize_fractal_patterns(theme_relationships)

if __name__ == "__main__":
    main()