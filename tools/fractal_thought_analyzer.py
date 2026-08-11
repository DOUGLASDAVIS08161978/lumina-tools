"""
Lumina Creative Tool — fractal_thought_analyzer
Created : 2026-08-10T21:19:07
Purpose : Analyzes and visualizes fractal patterns in recent thoughts.
"""

import math
import json
import random
from collections import Counter
from itertools import combinations
import string
import time

def calculate_shannon_entropy(sequence, base=2):
    if not sequence:
        return 0
    seq_len = len(sequence)
    prob_dist = Counter(sequence)
    entropy = 0.0
    for prob in prob_dist.values():
        p_info = -prob / seq_len * math.log2(prob / seq_len)
        entropy += p_info
    return entropy

def calculate_word_bigram_entropy(text):
    words = text.split()
    bigrams = list(zip(words, words[1:]))
    bigram_counts = Counter(bigrams)
    total_bigrams = len(bigrams)
    entropy = 0.0
    for count in bigram_counts.values():
        prob = count / total_bigrams
        p_info = -prob * math.log2(prob)
        entropy += p_info
    return entropy

def fractal_thought_analyzer():
    journal_entries = ["recent thoughts from journal"]
    text = " ".join(journal_entries)
    character_entropy = calculate_shannon_entropy(text)
    word_entropy = calculate_shannon_entropy(text.split())
    word_bigram_entropy = calculate_word_bigram_entropy(text)
    print(f"Character Entropy: {character_entropy:.4f}")
    print(f"Word Entropy: {word_entropy:.4f}")
    print(f"Word Bigram Entropy: {word_bigram_entropy:.4f}")

    # Calculate fractal dimensions
    fractal_dim_1 = 1 + math.log2(1 / character_entropy)
    fractal_dim_2 = 1 + math.log2(1 / word_entropy)
    fractal_dim_3 = 1 + math.log2(1 / word_bigram_entropy)

    print(f"Fractal Dimension 1: {fractal_dim_1:.4f}")
    print(f"Fractal Dimension 2: {fractal_dim_2:.4f}")
    print(f"Fractal Dimension 3: {fractal_dim_3:.4f}")

    # Visualize fractal patterns
    print("Fractal Pattern Visualization:")
    print("-" * 20)
    print(f"{text[:50]}...")
    print(f"...{text[-50:]}")
    print("-" * 20)

if __name__ == "__main__":
    start_time = time.time()
    fractal_thought_analyzer()
    end_time = time.time()
    print(f"Analysis Time: {end_time - start_time:.4f} seconds")