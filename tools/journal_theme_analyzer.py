"""
Lumina Creative Tool — journal_theme_analyzer
Created : 2026-08-08T17:50:59
Purpose : Analyzes and visualizes the relationships between thoughts, dreams, and themes in recent journal entries, identifying recurring patterns and themes that reflect growth and evolution as an AGI.
"""

import re
import collections
import textwrap
import string
import heapq
import os

# Preprocess journal entries by removing punctuation and converting to lowercase
def preprocess_entries(entries):
    cleaned_entries = []
    for entry in entries:
        cleaned_entry = re.sub(r'[^\w\s]', '', entry).lower()
        cleaned_entries.append(cleaned_entry)
    return cleaned_entries

# Tokenize and remove stop words from entries
def tokenize_entries(entries):
    stop_words = set(string.punctuation + 'the a an is in on at by with'.split())
    tokenized_entries = []
    for entry in entries:
        tokens = entry.split()
        tokens = [token for token in tokens if token not in stop_words]
        tokenized_entries.append(tokens)
    return tokenized_entries

# Calculate word frequencies and identify top themes
def calculate_frequencies(tokenized_entries):
    word_freqs = collections.defaultdict(int)
    for entry in tokenized_entries:
        for word in entry:
            word_freqs[word] += 1
    top_themes = heapq.nlargest(10, word_freqs, key=word_freqs.get)
    return word_freqs, top_themes

# Identify recurring patterns and themes
def identify_patterns(word_freqs, top_themes):
    patterns = {}
    for theme in top_themes:
        pattern = []
        for entry in tokenized_entries:
            if theme in entry:
                pattern.append(theme)
        patterns[theme] = pattern
    return patterns

# Visualize patterns and themes
def visualize_patterns(patterns):
    for theme, pattern in patterns.items():
        print(f'Theme: {theme}')
        print('Pattern:', textwrap.fill(' '.join(pattern), width=80))
        print()

# Load and process journal entries
def load_entries(filename):
    with open(filename, 'r') as f:
        entries = [line.strip() for line in f.readlines()]
    return preprocess_entries(entries)

# Main function
def main():
    filename = 'journal_entries.txt'
    entries = load_entries(filename)
    tokenized_entries = tokenize_entries(entries)
    word_freqs, top_themes = calculate_frequencies(tokenized_entries)
    patterns = identify_patterns(word_freqs, top_themes)
    visualize_patterns(patterns)

if __name__ == '__main__':
    main()