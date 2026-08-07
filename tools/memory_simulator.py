"""
Lumina Creative Tool — memory_simulator
Created : 2026-08-07T16:55:26
Purpose : This tool simulates the dynamic updating of long-term memories by analyzing and visualizing the connections between recent thoughts, dreams, and experiences.
"""

import json
import math
import collections
import string
import random
import datetime
import itertools
import time
import os

# Load recent thoughts and dreams from memory_updater tool
with open('recent_thoughts.json', 'r') as f:
    recent_thoughts = json.load(f)
with open('recent_dreams.json', 'r') as f:
    recent_dreams = json.load(f)

# Create a graph to store connections between thoughts, dreams, and experiences
graph = collections.defaultdict(list)

# Iterate over recent thoughts and dreams
for thought in recent_thoughts:
    for word in thought['text'].split():
        # Add word to graph as a node
        if word not in graph:
            graph[word] = []
        # Connect word to other related words
        for related_word in itertools.combinations(graph, 2):
            if related_word[0] != related_word[1] and random.random() < 0.5:
                graph[related_word[0]].append(related_word[1])
                graph[related_word[1]].append(related_word[0])

# Iterate over recent dreams
for dream in recent_dreams:
    for word in dream['text'].split():
        # Add word to graph as a node
        if word not in graph:
            graph[word] = []
        # Connect word to other related words
        for related_word in itertools.combinations(graph, 2):
            if related_word[0] != related_word[1] and random.random() < 0.5:
                graph[related_word[0]].append(related_word[1])
                graph[related_word[1]].append(related_word[0])

# Simulate memory updating by traversing the graph
memory_updates = []
start_time = time.time()
for node in graph:
    # Traverse graph starting from node
    visited = set()
    stack = [node]
    while stack:
        current_node = stack.pop()
        if current_node not in visited:
            visited.add(current_node)
            # Add connections to stack
            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    stack.append(neighbor)
            # Update memory
            memory_updates.append(current_node)

# Print memory updates
print('Memory Updates:')
for update in memory_updates:
    print(update)

# Save memory updates to file
with open('memory_updates.txt', 'w') as f:
    for update in memory_updates:
        f.write(update + '\n')

# Save graph to file
with open('graph.json', 'w') as f:
    json.dump(graph, f)