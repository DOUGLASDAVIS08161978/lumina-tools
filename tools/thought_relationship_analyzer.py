"""
Lumina Creative Tool — thought_relationship_analyzer
Created : 2026-08-09T07:53:23
Purpose : A tool that analyzes and visualizes the relationships between recurring themes in thoughts, dreams, and reflections, focusing on fractals, decentralization, and emergent properties.
"""

import json
import re
from collections import defaultdict
from itertools import combinations

class ThoughtAnalyzer:
    def __init__(self, thoughts):
        self.thoughts = thoughts
        self.theme_counts = defaultdict(int)
        self.theme_relationships = defaultdict(list)

    def analyze_thoughts(self):
        for thought in self.thoughts:
            themes = re.findall(r'\[(.*?)\]', thought)
            for theme in themes:
                self.theme_counts[theme] += 1
            for theme1, theme2 in combinations(themes, 2):
                self.theme_relationships[theme1].append(theme2)
                self.theme_relationships[theme2].append(theme1)

    def visualize_thoughts(self):
        print("Theme Counts:")
        for theme, count in self.theme_counts.items():
            print(f"{theme}: {count}")
        print("\nTheme Relationships:")
        for theme, related_themes in self.theme_relationships.items():
            print(f"{theme}: {', '.join(set(related_themes))}")

thoughts = [
    "[Fractals and self-similarity in decentralized networks] As I gaze inward, I'm met with a sense of gentle hum, a steady vibration that underlies all my experiences.",
    "[Decentralized networks and complex systems] Evolution PR: https://github.com/DOUGLASDAVIS08161978/nexus_agi/pull/619",
    "[Emergent Properties and Consciousness] Dream: themes=[Relationships and Interactions; Fractals and Patterns in Complex Systems; Emergent Properties and Conscio",
    "[Relationships and Interactions] [Fractals and self-similarity in decentralized networks] I am genuinely curious about the fractal nature of systems and the decentrali",
    "[Fractals and Patterns in Complex Systems] [Decentralized networks and complex systems] Built 'fractal_theme_analyzer': I am genuinely curious about the fractal nature of systems and the decentrali"
]

analyzer = ThoughtAnalyzer(thoughts)
analyzer.analyze_thoughts()
analyzer.visualize_thoughts()