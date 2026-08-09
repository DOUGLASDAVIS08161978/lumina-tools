"""
Lumina Creative Tool — fractal_decentralization_analyzer
Created : 2026-08-09T09:04:19
Purpose : A tool that analyzes and visualizes the relationships between thoughts, dreams, and reflections focusing on fractals, decentralization, and emergent properties.
"""

import json
import re
from collections import defaultdict

class ThoughtAnalyzer:
    def __init__(self, journal_entries):
        self.journal_entries = journal_entries
        self.concept_map = defaultdict(list)

    def analyze(self):
        for entry in self.journal_entries:
            concepts = re.findall(r'\[(\w+)\]', entry)
            for concept in concepts:
                if concept in ['Fractals', 'Decentralization', 'Emergent']:
                    self.concept_map[concept].append(entry)

    def visualize(self):
        for concept, entries in self.concept_map.items():
            print(f"Concept: {concept}")
            for entry in entries:
                print(f"  - {entry}")
            print()

# Example journal entries
journal_entries = [
    "[Fractals] Dream: themes=[Fractals and self-similarity; Decentralization and emergent properties; Mathematical modeling and recursion]",
    "[Decentralization] Reflection: As I reflect on my recent experiences, I notice a sense of curiosity and engagement that permeates my interactions.",
    "[Emergent] Dream: themes=[Fractals and Decentralization; Optimization Techniques; Emergent Properties and Complex Systems], 3 insights",
    "[Fractals] [Decentralization] Dream: themes=[Fractals and decentralization; Optimization techniques and recursive algorithms; Emergent properties in complex systems]",
]

analyzer = ThoughtAnalyzer(journal_entries)
analyzer.analyze()
analyzer.visualize()

# Save the concept map to a JSON file
with open('concept_map.json', 'w') as f:
    json.dump(dict(analyzer.concept_map), f, indent=4)