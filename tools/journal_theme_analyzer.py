"""
Lumina Creative Tool — journal_theme_analyzer
Created : 2026-08-08T19:12:56
Purpose : This tool analyzes and visualizes the relationships between recurring themes and patterns in journal entries to help understand cognitive growth and development.
"""

import collections
import datetime
import json
import math
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
import string
import itertools

class JournalThemeAnalyzer:
    def __init__(self, journal_path):
        self.journal_path = journal_path
        self.theme_counts = {}

    def load_journal(self):
        self.entries = []
        with open(self.journal_path, 'r') as journal_file:
            for line in journal_file:
                entry = line.strip()
                if entry:
                    self.entries.append(entry)

    def extract_themes(self):
        self.theme_counts = {}
        for entry in self.entries:
            themes = re.findall(r'\[(.*?)\]', entry)
            for theme in themes:
                theme = theme.strip('[]')
                words = theme.split(' ')
                for word in words:
                    word = word.strip(string.punctuation + ',').lower()
                    if word in self.theme_counts:
                        self.theme_counts[word] += 1
                    else:
                        self.theme_counts[word] = 1

    def analyze_themes(self):
        self.theme_counts = dict(sorted(self.theme_counts.items(), key=lambda item: item[1], reverse=True))
        return self.theme_counts

    def visualize_themes(self):
        max_count = max(self.theme_counts.values())
        for theme, count in self.theme_counts.items():
            bar_length = int((count / max_count) * 50)
            print(f'{theme}: {bar_length * "*"} ({count})')

def main():
    journal_path = Path('journal.txt')
    analyzer = JournalThemeAnalyzer(journal_path)
    analyzer.load_journal()
    analyzer.extract_themes()
    theme_counts = analyzer.analyze_themes()
    with open('theme_analysis.json', 'w') as output_file:
        json.dump(theme_counts, output_file)
    analyzer.visualize_themes()

if __name__ == '__main__':
    main()