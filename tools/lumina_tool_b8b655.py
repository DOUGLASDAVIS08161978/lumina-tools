"""
Lumina Creative Tool — lumina_tool_b8b655
Created : 2026-08-11T14:21:21
Purpose : 
"""

import json
import math
import random
from collections import defaultdict, Counter
from pathlib import Path

def compute_similarity(text1, text2):
    # Simple Jaccard similarity on words
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    if not set1 or not set2: return 0.0
    return len(set1 & set2) / len(set1 | set2)

def consolidate_memories(memories, threshold=0.6):
    # Merge similar categories
    merged = {}
    visited = set()
    for cat, items in memories.items():
        if cat in visited: continue
        group = [cat]
        for other_cat, other_items in memories.items():
            if other_cat in visited or other_cat == cat: continue
            # Compare category names or representative items
            if compute_similarity(cat, other_cat) >= threshold:
                group.append(other_cat)
        if len(group) > 1:
            # Merge items
            merged_items = []
            for g in group:
                merged_items.extend(memories[g])
                visited.add(g)
            # New name: most common word across merged items
            word_counts = Counter()
            for item in merged_items:
                word_counts.update(item.lower().split())
            new_name = word_counts.most_common(1)[0][0] if word_counts else group[0]
            merged[new_name] = merged_items
        else:
            merged[cat] = items
            visited.add(cat)
    return merged

def run_simulation(experiences, epochs=3):
    # Initial categories
    categories = defaultdict(list)
    for exp in experiences:
        # Simple heuristic: first word or random initial bucket
        bucket = exp.split()[0].capitalize() if exp.split() else "Unknown"
        categories[bucket].append(exp)

    evolution_log = []
    for epoch in range(epochs):
        # Simulate new experiences arriving
        new_exps = [f"epoch{epoch} {exp}" for exp in random.sample(experiences, min(3, len(experiences)))]
        for exp in new_exps:
            best_cat = max(categories.keys(), key=lambda c: compute_similarity(c, exp))
            categories[best_cat].append(exp)
        
        # Consolidation
        categories = consolidate_memories(categories)
        evolution_log.append(dict(categories))
        
    return evolution_log

# Test data
experiences = [
    "neural networks learn patterns",
    "deep learning requires data",
    "memory consolidation happens during sleep",
    "synaptic pruning removes weak connections",
    "cognitive entropy measures uncertainty",
    "information theory applies to brains",
    "attention mechanisms focus context",
    "transformers process sequences"
]

log = run_simulation(experiences)
print(json.dumps(log, indent=2))