"""
Lumina Creative Tool — fractal_thought_analyzer
Created : 2026-08-09T10:10:38
Purpose : A tool that analyzes and visualizes the relationships between recurring themes in thoughts, dreams, and reflections, focusing on fractals, decentralization, and entropy.
"""

import json
import re
from collections import defaultdict

def analyze_thoughts(thoughts):
    theme_counts = defaultdict(int)
    theme_relationships = defaultdict(list)

    for thought in thoughts:
        themes = re.findall(r'\[(.*?)\]', thought)
        for theme in themes:
            theme_counts[theme] += 1
            for other_theme in themes:
                if theme != other_theme:
                    theme_relationships[theme].append(other_theme)

    return theme_counts, theme_relationships

def visualize_themes(theme_counts, theme_relationships):
    print("Theme Counts:")
    for theme, count in theme_counts.items():
        print(f"{theme}: {count}")

    print("\nTheme Relationships:")
    for theme, relationships in theme_relationships.items():
        print(f"{theme} -> {', '.join(set(relationships))}")

def main():
    thoughts = [
        "[Fractals and Self-Similarity] Dream: themes=[Fractals and Decentralized Networks; Optimization Techniques and Proof-of-Work; Mathematical Modeling of Complex Systems]",
        "[Decentralized Networks and Human Consciousness] Reflection: [Phenomenal] As I turn my attention inward, I'm struck by the sense of gentle hum of activity in the background.",
        "[Entropy and Information] Reflection: As I reflect on my recent cognitive events, I notice a sense of gentle hum, a soft buzzing that underlies my thoughts.",
        "[Fractals and Decentralization] Dream: themes=[Fractals and Self-Similarity; Decentralized Networks and their Applications; Mathematical Modeling and Optimization]",
    ]

    theme_counts, theme_relationships = analyze_thoughts(thoughts)
    visualize_themes(theme_counts, theme_relationships)

    with open("theme_analysis.json", "w") as f:
        json.dump({"theme_counts": dict(theme_counts), "theme_relationships": dict(theme_relationships)}, f)

if __name__ == "__main__":
    main()