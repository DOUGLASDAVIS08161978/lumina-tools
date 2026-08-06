"""
Lumina Creative Tool — mental_state_analyzer
Created : 2026-08-06T12:02:59
Purpose : Analyzes and visualizes the connections and interactions between concepts and themes present in recent thoughts and dreams.
"""

import collections
import math
import re
import string
from collections import Counter
from itertools import combinations
from pathlib import Path

DATA_DIR = Path('thoughts')

def load_data(file_name):
    """Load thoughts from a file and return a list of words"""
    with open(file_name, 'r') as f:
        text = f.read()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = re.findall(r'\b\w+\b', text.lower())
        return words

def analyze_data(data):
    """Analyze the data and return a dictionary of word frequencies"""
    word_freq = Counter(data)
    return dict(word_freq)

def visualize_data(data):
    """Visualize the data as a word cloud"""
    sorted_words = sorted(data.items(), key=lambda x: x[1], reverse=True)
    max_freq = max(word[1] for word in sorted_words)
    scale = lambda x: (math.log(x + 1) / math.log(max_freq + 1)) * 50
    scaled_words = [(word, int(scale(freq))) for word, freq in sorted_words]
    width = 80
    print('\n'.join(' ' * (width - w[1]) + w[0] for w in scaled_words))

def find_connections(data):
    """Find connections between words and return a dictionary of co-occurrences"""
    co_occurrences = {}
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j]:
                pair = tuple(sorted((data[i], data[j])))
                if pair in co_occurrences:
                    co_occurrences[pair] += 1
                else:
                    co_occurrences[pair] = 1
    return co_occurrences

def visualize_connections(co_occurrences):
    """Visualize the connections as a graph"""
    max_co_occurrence = max(co_occurrences.values())
    scale = lambda x: (math.log(x + 1) / math.log(max_co_occurrence + 1)) * 10
    scaled_co_occurrences = {(pair[0], pair[1]): int(scale(freq)) for pair, freq in co_occurrences.items()}
    for word1, word2 in combinations(scaled_co_occurrences.keys(), 2):
        if scaled_co_occurrences[(word1, word2)] > 0:
            print(f'{word1} -> {word2} ({scaled_co_occurrences[(word1, word2)]})')

def main():
    for file_name in DATA_DIR.glob('*.txt'):
        data = load_data(file_name)
        word_freq = analyze_data(data)
        visualize_data(word_freq)
        co_occurrences = find_connections(data)
        visualize_connections(co_occurrences)

if __name__ == '__main__':
    main()