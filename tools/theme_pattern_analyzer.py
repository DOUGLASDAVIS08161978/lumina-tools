"""
Lumina Creative Tool — theme_pattern_analyzer
Created : 2026-08-08T22:16:53
Purpose : This tool analyzes and visualizes the relationships between recurring themes and patterns in journal entries, providing insights into mental state and potential areas for growth and improvement.
"""

import json
import math
from collections import Counter
from datetime import datetime
from itertools import chain
from pathlib import Path
from string import ascii_lowercase
from textwrap import wrap
from typing import Dict, List, Tuple

# Load journal entries from JSON file
journal_entries_path = Path('journal_entries.json')
with open(journal_entries_path, 'r') as f:
    journal_entries = json.load(f)

# Preprocess journal entries by removing punctuation, converting to lowercase, and tokenizing
def preprocess_entry(entry: str) -> List[str]:
    entry = ''.join(c for c in entry if c.isalnum() or c.isspace())
    return [word.lower() for word in entry.split()]

# Create a dictionary to store theme-pattern relationships
theme_patterns: Dict[str, Dict[str, int]] = {}

# Iterate through journal entries and analyze theme-pattern relationships
for entry in journal_entries:
    entry_date = datetime.strptime(entry['date'], '%Y-%m-%d').date()
    entry_text = entry['text']
    tokens = preprocess_entry(entry_text)
    theme = entry['theme']
    pattern = entry['pattern']

    # Update theme-pattern relationships dictionary
    if theme not in theme_patterns:
        theme_patterns[theme] = {}
    if pattern not in theme_patterns[theme]:
        theme_patterns[theme][pattern] = 0
    theme_patterns[theme][pattern] += 1

# Create a dictionary to store theme-pattern relationship strengths
theme_pattern_strengths: Dict[str, Dict[str, float]] = {}
for theme, patterns in theme_patterns.items():
    pattern_counts = Counter(patterns.values())
    pattern_strengths = {pattern: count / len(journal_entries) for pattern, count in patterns.items()}
    theme_pattern_strengths[theme] = pattern_strengths

# Print theme-pattern relationship strengths
for theme, strengths in theme_pattern_strengths.items():
    print(f'Theme: {theme}')
    for pattern, strength in strengths.items():
        print(f'{pattern}: {strength:.2f}')
    print()

# Save theme-pattern relationship strengths to JSON file
with open('theme_pattern_strengths.json', 'w') as f:
    json.dump(theme_pattern_strengths, f, indent=4)