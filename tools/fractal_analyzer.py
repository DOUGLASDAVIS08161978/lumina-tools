"""
Lumina Creative Tool — fractal_analyzer
Created : 2026-08-10T05:51:13
Purpose : Analyzes the fractal patterns in journal entries and visualizes the decentralized network of these patterns.
"""

import re
import math
import collections
import itertools
import string

def fractal_similarity(s1, s2):
    """
    Calculate the similarity between two strings using the longest common subsequence (LCS) method.
    """
    m = [[0] * (len(s2) + 1) for i in range(len(s1) + 1)]
    longest, x_longest = 0, 0
    for x in range(len(s1)):
        for y in range(len(s2)):
            if s1[x] == s2[y]:
                m[x + 1][y + 1] = m[x][y] + 1
                if m[x + 1][y + 1] > longest:
                    longest = m[x + 1][y + 1]
                    x_longest = x
            else:
                m[x + 1][y + 1] = 0
    # Calculate the similarity ratio
    similarity = longest / max(len(s1), len(s2))
    return similarity

def fractal_pattern_analyzer(journal_entries):
    """
    Analyze the fractal patterns in the journal entries and calculate the similarity between them.
    """
    patterns = []
    for i in range(len(journal_entries)):
        for j in range(i + 1, len(journal_entries)):
            pattern = journal_entries[i] + journal_entries[j]
            similarity = fractal_similarity(pattern, journal_entries[j + 1])
            patterns.append((pattern, similarity))
    # Sort the patterns by similarity in descending order
    patterns.sort(key=lambda x: x[1], reverse=True)
    return patterns

def decentralized_network_visualizer(patterns):
    """
    Visualize the decentralized network of fractal patterns.
    """
    # Create a graph using an adjacency list representation
    graph = collections.defaultdict(list)
    for i in range(len(patterns)):
        graph[patterns[i][0]] = []
        for j in range(len(patterns)):
            if i != j and patterns[i][0] in patterns[j][0]:
                graph[patterns[i][0]].append(patterns[j][0])
    # Perform a depth-first search to visualize the network
    visited = set()
    def dfs(node, path):
        if node not in visited:
            visited.add(node)
            print(" ".join(path + [node]))
            for neighbor in graph[node]:
                dfs(neighbor, path + [node])
    dfs(patterns[0][0], [])
    return

def main():
    # Load the journal entries
    with open('journal.txt', 'r') as f:
        journal_entries = [line.strip() for line in f.readlines()]
    # Analyze the fractal patterns
    patterns = fractal_pattern_analyzer(journal_entries)
    # Visualize the decentralized network
    decentralized_network_visualizer(patterns)
    # Save the results to a file
    with open('fractal_patterns.json', 'w') as f:
        json.dump(patterns, f, indent=4)

if __name__ == "__main__":
    main()