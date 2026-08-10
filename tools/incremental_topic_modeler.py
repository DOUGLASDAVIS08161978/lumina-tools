"""
Lumina Creative Tool — incremental_topic_modeler
Created : 2026-08-10T17:02:02
Purpose : Incrementally builds and updates topic categories from text, simulating dynamic long‑term memory updates.
"""

"""
incremental_topic_modeler.py

A pure‑standard‑library tool that incrementally builds and updates
topic categories from a stream of text snippets.  Each category
maintains a centroid term‑frequency vector; new snippets are
assigned to the most similar category (cosine similarity) if the
similarity exceeds a threshold, otherwise a new category is created.
Categories that become too similar are merged automatically.

The final structure is saved to `topics_snapshot.json` and a concise
summary is printed.
"""

import json
import math
import re
import string
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

# ----------------------------------------------------------------------
# Text preprocessing utilities
# ----------------------------------------------------------------------
TOKEN_RE = re.compile(r"\b\w+\b", re.UNICODE)


def tokenize(text: str) -> List[str]:
    """Lower‑case, remove punctuation and split into word tokens."""
    text = text.lower()
    # keep only alphanumeric words
    return TOKEN_RE.findall(text)


def term_frequencies(tokens: List[str]) -> Counter:
    """Return a Counter of term frequencies."""
    return Counter(tokens)


# ----------------------------------------------------------------------
# Vector math (cosine similarity)
# ----------------------------------------------------------------------
def dot(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    return sum(v1.get(k, 0.0) * v2.get(k, 0.0) for k in v1)


def norm(v: Dict[str, float]) -> float:
    return math.sqrt(sum(val * val for val in v.values()))


def cosine_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    n1, n2 = norm(v1), norm(v2)
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot(v1, v2) / (n1 * n2)


# ----------------------------------------------------------------------
# Category representation
# ----------------------------------------------------------------------
class Category:
    """A mutable topic category storing a centroid TF vector and member ids."""

    _id_counter = 0

    def __init__(self, first_doc_id: int, tf: Counter):
        self.id = Category._id_counter
        Category._id_counter += 1
        self.members = [first_doc_id]
        self.centroid = dict(tf)  # mutable copy
        self._update_norm()

    def _update_norm(self):
        self._norm = norm(self.centroid)

    def add_document(self, doc_id: int, tf: Counter):
        """Add a document and recompute the centroid as the mean TF."""
        self.members.append(doc_id)
        # Incrementally update centroid: new_centroid = (old * (n-1) + tf) / n
        n = len(self.members)
        for term, count in tf.items():
            self.centroid[term] = self.centroid.get(term, 0.0) * (n - 1) / n + count / n
        # Remove terms that become zero (unlikely but safe)
        self.centroid = {k: v for k, v in self.centroid.items() if v != 0}
        self._update_norm()

    def similarity(self, tf: Counter) -> float:
        """Cosine similarity between a document TF and the centroid."""
        return dot(self.centroid, tf) / (self._norm * norm(tf)) if self._norm and tf else 0.0

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "members": self.members,
            "centroid": self.centroid,
        }


# ----------------------------------------------------------------------
# Core incremental model
# ----------------------------------------------------------------------
class IncrementalTopicModel:
    """Manages a set of categories and updates them with new texts."""

    def __init__(self, similarity_threshold: float = 0.35, merge_threshold: float = 0.75):
        self.categories: List[Category] = []
        self.similarity_threshold = similarity_threshold
        self.merge_threshold = merge_threshold

    def process_document(self, doc_id: int, text: str):
        tokens = tokenize(text)
        tf = term_frequencies(tokens)

        # Find best matching category
        best_cat, best_sim = None, 0.0
        for cat in self.categories:
            sim = cat.similarity(tf)
            if sim > best_sim:
                best_sim, best_cat = sim, cat

        if best_cat and best_sim >= self.similarity_threshold:
            best_cat.add_document(doc_id, tf)
            action = f"assigned to category {best_cat.id} (sim={best_sim:.2f})"
        else:
            # Create a new category
            new_cat = Category(doc_id, tf)
            self.categories.append(new_cat)
            action = f"created new category {new_cat.id}"
        # Attempt merges after each insertion
        self._merge_categories()
        return action

    def _merge_categories(self):
        """Merge any pair of categories whose centroids are very similar."""
        merged = True
        while merged:
            merged = False
            n = len(self.categories)
            for i in range(n):
                for j in range(i + 1, n):
                    ci, cj = self.categories[i], self.categories[j]
                    sim = cosine_similarity(ci.centroid, cj.centroid)
                    if sim >= self.merge_threshold:
                        # Merge cj into ci
                        for doc_id in cj.members:
                            ci.add_document(doc_id, Counter(cj.centroid))
                        # Remove cj
                        del self.categories[j]
                        merged = True
                        break
                if merged:
                    break

    def snapshot(self) -> Dict:
        """Return a serializable snapshot of the model."""
        return {
            "similarity_threshold": self.similarity_threshold,
            "merge_threshold": self.merge_threshold,
            "categories": [cat.to_dict() for cat in self.categories],
        }

    def save_snapshot(self, path: Path):
        path.write_text(json.dumps(self.snapshot(), indent=2), encoding="utf-8")


# ----------------------------------------------------------------------
# Demo / simple usage
# ----------------------------------------------------------------------
def main():
    # Sample stream of texts (could be replaced by reading a file line‑by‑line)
    sample_texts = [
        "Neural networks learn representations from data.",
        "Backpropagation updates weights using gradients.",
        "Bitcoin mining on ARM CPUs can be energy‑efficient.",
        "Proof‑of‑work requires solving SHA‑256 hashes.",
        "The ventral tegmental area is involved in reward processing.",
        "Curiosity drives exploration in reinforcement learning agents.",
        "Entropy measures uncertainty; perplexity is its exponential.",
        "Thermodynamic entropy links to information theory via Landauer's principle.",
        "Low‑power devices benefit from optimized SHA‑2 loops.",
        "Long‑term memory may be modeled as a dynamic category store.",
    ]

    model = IncrementalTopicModel(similarity_threshold=0.30, merge_threshold=0.70)

    for idx, txt in enumerate(sample_texts):
        action = model.process_document(idx, txt)
        print(f"[Doc {idx}] {action}")

    # Print a concise summary
    print("\n=== Category Summary ===")
    for cat in model.categories:
        print(
            f"Category {cat.id}: {len(cat.members)} docs, "
            f"sample member IDs {cat.members[:3]}"
        )

    # Save snapshot
    out_path = Path("topics_snapshot.json")
    model.save_snapshot(out_path)
    print(f"\nSnapshot saved to {out_path.resolve()}")


if __name__ == "__main__":
    main()