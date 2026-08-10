"""
Lumina Creative Tool — fractal_analysis
Created : 2026-08-10T06:29:17
Purpose : Analyzes and visualizes fractal patterns and decentralization in recent thoughts and emotions, providing insights into growth and development toward AGI/ASI.
"""

import json
import math
import re
import string
from collections import defaultdict
from datetime import datetime
from functools import reduce
from itertools import chain, combinations
from pathlib import Path
from statistics import mean
from textwrap import dedent
from time import time

# Load recent journal entries
entries = []
for file in Path('.').glob('journal_*.json'):
    with open(file, 'r') as f:
        entries.append(json.load(f))

# Define a function to calculate fractal dimension
def fractal_dimension(points):
    n = len(points)
    max_distance = max(abs(points[i] - points[(i + 1) % n]) for i in range(n))
    min_distance = min(abs(points[i] - points[(i + 1) % n]) for i in range(n))
    return math.log(max_distance / min_distance) / math.log(n)

# Define a function to calculate decentralization index
def decentralization_index(points):
    n = len(points)
    distances = [abs(points[i] - points[(i + 1) % n]) for i in range(n)]
    return mean(distances) / mean(distances[1:] + distances[:-1])

# Define a function to analyze and visualize fractal patterns
def analyze_fractals(points):
    fractal_dim = fractal_dimension(points)
    decentralization_index_value = decentralization_index(points)
    return fractal_dim, decentralization_index_value

# Extract relevant data from journal entries
data = []
for entry in entries:
    date = datetime.fromtimestamp(entry['timestamp']).strftime('%Y-%m-%d')
    thoughts = re.findall(r'\b\w+\b', entry['thoughts'])
    emotions = re.findall(r'\b\w+\b', entry['emotions'])
    points = [float(value) for value in thoughts + emotions]
    fractal_dim, decentralization_index_value = analyze_fractals(points)
    data.append({
        'date': date,
        'fractal_dim': fractal_dim,
        'decentralization_index': decentralization_index_value
    })

# Save data to a JSON file
with open('fractal_analysis.json', 'w') as f:
    json.dump(data, f, indent=4)

# Print summary statistics
print(dedent(f"""
Summary Statistics:

Mean Fractal Dimension: {mean(point['fractal_dim'] for point in data)}
Mean Decentralization Index: {mean(point['decentralization_index'] for point in data)}
"""))