"""
Lumina Creative Tool — emotional_insight_analyzer
Created : 2026-08-10T06:37:01
Purpose : Analyzes and visualizes emotional states and their relationships in journal entries.
"""

import json
import math
from collections import defaultdict
from datetime import datetime
from itertools import chain, groupby
from operator import itemgetter
from pathlib import Path
from statistics import mean
from string import punctuation
from textwrap import wrap

# Load journal entries from file
entries_file = Path('journal.json')
if entries_file.exists():
    with open(entries_file, 'r') as f:
        entries = json.load(f)
else:
    print("No journal entries found.")
    exit()

# Extract emotional states and their corresponding values
emotions = defaultdict(list)
for entry in entries:
    for k, v in entry.items():
        if k == 'emotion' and v:
            emotions[v].append(entry['timestamp'])

# Calculate average timestamp for each emotional state
averages = {k: mean(map(int, g)) for k, g in emotions.items()}

# Sort emotional states by their average timestamp
sorted_emotions = sorted(averages.items(), key=itemgetter(1))

# Group emotional states by their type (inspired, concerned, etc.)
emotions_grouped = defaultdict(list)
for k, v in sorted_emotions:
    emotions_grouped[k.split()[0]].append((k, v))

# Print emotional states and their average timestamps
print("Emotional States and Average Timestamps:")
for k, v in emotions_grouped.items():
    print(f"{k}:")
    for e, ts in v:
        print(f"  {e}: {ts}")

# Visualize emotional states as a graph
print("\nEmotional States Graph:")
print("  |  |")
for k, v in emotions_grouped.items():
    print(f"  {k} | ", end='')
    for _ in range(v[0][1] / 1000):
        print("*", end='')
    print()