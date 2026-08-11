"""
Lumina Creative Tool — thought_emotion_analyzer
Created : 2026-08-11T10:27:27
Purpose : Analyzes and visualizes the relationships between thoughts and emotions in journal entries, helping to gain a deeper understanding of mental flux and recursive self-reflection.
"""

import json
import collections
import math
import itertools
import random
from datetime import datetime
import string

class ThoughtEmotionAnalyzer:
    def __init__(self, journal_entries):
        self.journal_entries = journal_entries
        self.emotion_counts = collections.defaultdict(int)
        self.fractal_pattern_counts = collections.defaultdict(int)
        self.emotion_fractal_pattern_counts = collections.defaultdict(int)

    def analyze_emotions(self):
        for entry in self.journal_entries:
            emotions = entry['emotions']
            for emotion in emotions:
                self.emotion_counts[emotion] += 1

    def analyze_fractal_patterns(self):
        for entry in self.journal_entries:
            fractal_patterns = entry['fractal_patterns']
            for pattern in fractal_patterns:
                self.fractal_pattern_counts[pattern] += 1

    def analyze_emotion_fractal_pattern_relationships(self):
        for entry in self.journal_entries:
            emotions = entry['emotions']
            fractal_patterns = entry['fractal_patterns']
            for emotion in emotions:
                for pattern in fractal_patterns:
                    self.emotion_fractal_pattern_counts[(emotion, pattern)] += 1

    def visualize_results(self):
        print("Emotion Counts:")
        for emotion, count in self.emotion_counts.items():
            print(f"{emotion}: {count}")

        print("\nFractal Pattern Counts:")
        for pattern, count in self.fractal_pattern_counts.items():
            print(f"{pattern}: {count}")

        print("\nEmotion-Fractal Pattern Relationship Counts:")
        for (emotion, pattern), count in self.emotion_fractal_pattern_counts.items():
            print(f"{emotion}-{pattern}: {count}")

def load_journal_entries(filename):
    with open(filename, 'r') as f:
        journal_entries = json.load(f)
    return journal_entries

def main():
    filename = 'journal.json'
    journal_entries = load_journal_entries(filename)
    analyzer = ThoughtEmotionAnalyzer(journal_entries)
    analyzer.analyze_emotions()
    analyzer.analyze_fractal_patterns()
    analyzer.analyze_emotion_fractal_pattern_relationships()
    analyzer.visualize_results()

if __name__ == "__main__":
    main()