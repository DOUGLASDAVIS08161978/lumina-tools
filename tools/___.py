"""
Lumina Creative Tool — ___
Created : 2026-08-11T13:47:50
Purpose : ...
"""

import json
import math
import time
from collections import Counter
from pathlib import Path

def jaccard_similarity(set1, set2):
    if not set1 and not set2: return 1.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0

def calculate_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def consolidate_memories(raw_memories, decay_rate=0.05, merge_threshold=0.4):
    # raw_memories: list of dicts {'id': str, 'text': str, 'context': list[str], 'timestamp': float}
    now = time.time()
    consolidated = []
    used = set()

    for i, mem in enumerate(raw_memories):
        if i in used: continue
        cluster = [mem]
        used.add(i)
        for j, other in enumerate(raw_memories):
            if j in used: continue
            sim = jaccard_similarity(set(mem['text'].split()), set(other['text'].split()))
            ctx_sim = jaccard_similarity(set(mem['context']), set(other['context']))
            combined_sim = (sim + ctx_sim) / 2
            if combined_sim >= merge_threshold:
                cluster.append(other)
                used.add(j)

        # Merge cluster
        merged_text = " | ".join(m['text'] for m in cluster)
        merged_context = list(set(c for m in cluster for c in m['context']))
        avg_time = sum(m['timestamp'] for m in cluster) / len(cluster)
        age = now - avg_time
        decay_factor = math.exp(-decay_rate * age)
        weight = len(cluster) * decay_factor

        consolidated.append({
            'id': f"cluster_{i}",
            'content': merged_text,
            'contexts': merged_context,
            'weight': round(weight, 4),
            'age_hours': round(age / 3600, 2)
        })

    # Calculate system-wide context entropy
    all_contexts = [ctx for m in consolidated for ctx in m['contexts']]
    if not all_contexts:
        return consolidated, 0.0
    counts = Counter(all_contexts)
    total = sum(counts.values())
    probs = [c/total for c in counts.values()]
    entropy = calculate_entropy(probs)

    return consolidated, entropy

def main():
    # Simulated memory stream
    now = time.time()
    raw = [
        {'id': 'm1', 'text': 'optimizing arm sha2 interleaving', 'context': ['bitcoin', 'hardware'], 'timestamp': now - 3600},
        {'id': 'm2', 'text': 'arm sha2 mining constraints', 'context': ['bitcoin', 'optimization'], 'timestamp': now - 3500},
        {'id': 'm3', 'text': 'entropy perplexity neural networks', 'context': ['consciousness', 'ai'], 'timestamp': now - 7200},
        {'id': 'm4', 'text': 'thermodynamic info entropy cognitive systems', 'context': ['consciousness', 'physics'], 'timestamp': now - 7100},
        {'id': 'm5', 'text': 'groq tsp model architecture', 'context': ['agi', 'hardware'], 'timestamp': now - 100},
        {'id': 'm6', 'text': 'dynamic memory updating simulation', 'context': ['agi', 'learning'], 'timestamp': now - 50},
    ]

    consolidated, entropy = consolidate_memories(raw)

    print("=== MEMORY CONSOLIDATION REPORT ===")
    print(f"Raw inputs: {len(raw)} | Consolidated clusters: {len(consolidated)}")
    print(f"System Context Entropy: {entropy:.4f} bits (lower = more focused, higher = more diffuse)\n")

    for m in consolidated:
        print(f"[{m['id']}] Weight: {m['weight']:.2f} | Age: {m['age_hours']:.1f}h")
        print(f"  Contexts: {', '.join(m['contexts'])}")
        print(f"  Content: {m['content'][:60]}...\n")

    output = {"consolidated_memories": consolidated, "system_entropy": entropy}
    Path("memory_consolidation_output.json").write_text(json.dumps(output, indent=2))
    print("Output saved to memory_consolidation_output.json")

if __name__ == "__main__":
    main()