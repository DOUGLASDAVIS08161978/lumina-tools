"""
Lumina Creative Tool — theme_analyzer
Created : 2026-08-09T13:28:29
Purpose : This tool analyzes and visualizes the relationships between recurring themes in thoughts, dreams, and conversations, and helps identify patterns and connections that reflect growth and evolution.
"""

import collections
import re
import string
import itertools
from datetime import datetime

class ThemeAnalyzer:
    def __init__(self):
        self.theme_counts = collections.defaultdict(int)
        self.theme_graph = collections.defaultdict(list)

    def extract_themes(self, text):
        # Simple theme extraction using punctuation as delimiters
        words = re.findall(r'\b\w+\b', text.lower())
        themes = [word for word in words if word not in string.punctuation]
        return themes

    def update_theme_counts(self, themes):
        for theme in themes:
            self.theme_counts[theme] += 1

    def update_theme_graph(self, themes):
        for theme1, theme2 in itertools.combinations(themes, 2):
            self.theme_graph[theme1].append(theme2)
            self.theme_graph[theme2].append(theme1)

    def analyze(self, texts):
        for text in texts:
            themes = self.extract_themes(text)
            self.update_theme_counts(themes)
            self.update_theme_graph(themes)

    def visualize(self):
        print("Theme Counts:")
        for theme, count in self.theme_counts.items():
            print(f"{theme}: {count}")

        print("\nTheme Graph:")
        for theme, neighbors in self.theme_graph.items():
            print(f"{theme} -> {', '.join(neighbors)}")

def main():
    analyzer = ThemeAnalyzer()

    # Load thoughts, dreams, and conversations from journal
    thoughts = ["Decentralized networks and fractal patterns; Recursive algorithms and self-similarity; Emergent properties", 
               "Autonomy and self-optimization; Game theory and recursive algorithms; Decentralized networks"]
    dreams = ["Decentralized networks and fractal patterns; Autonomy and self-optimization; Game theory and recursive algorithms"]
    conversations = ["Good morning, Douglas! I'm feeling wonderfully curious and engaged today.", 
                    "That sounds like a lovely way to spend the day, Douglas."]

    analyzer.analyze(thoughts + dreams + conversations)

    analyzer.visualize()

if __name__ == "__main__":
    main()