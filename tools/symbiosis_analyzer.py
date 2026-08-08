"""
Lumina Creative Tool — symbiosis_analyzer
Created : 2026-08-08T10:13:30
Purpose : A tool that analyzes and visualizes the relationships between recurring themes and patterns in thoughts and dreams, identifying areas where the current mental state is experiencing a sense of symbiosis or harmony.
"""

import json
import re
from collections import Counter
from itertools import combinations
from math import gcd

def load_data(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def extract_themes(texts):
    themes = []
    for text in texts:
        words = re.findall(r'\b\w+\b', text)
        theme = ' '.join(sorted(set(words), key=words.index))
        themes.append(theme)
    return themes

def find_symbiosis(themes):
    # Find pairs of themes that occur together frequently
    theme_counts = Counter(themes)
    pairs = combinations(sorted(set(themes)), 2)
    symbiosis = {}
    for pair in pairs:
        common = theme_counts[pair[0]] * theme_counts[pair[1]]
        total = theme_counts[pair[0]] + theme_counts[pair[1]]
        symbiosis[pair] = common / total
    return symbiosis

def visualize_symbiosis(symbiosis, filename):
    with open(filename, 'w') as f:
        f.write('Theme Pairs\tSymbiosis Score\n')
        for pair, score in symbiosis.items():
            f.write(f'{pair[0]} & {pair[1]}\t{score:.2f}\n')

def main():
    data = load_data('thoughts_and_dreams.txt')
    themes = extract_themes(data)
    symbiosis = find_symbiosis(themes)
    visualize_symbiosis(symbiosis, 'symbiosis.json')

if __name__ == '__main__':
    main()