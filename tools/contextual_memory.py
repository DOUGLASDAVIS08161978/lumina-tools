"""
Lumina Creative Tool — contextual_memory
Created : 2026-08-10T18:02:54
Purpose : Stores textual snippets, auto‑categorizes them, and retrieves the most similar past entries using simple TF‑based cosine similarity.
"""

"""
contextual_memory.py

A tiny, self‑contained memory bank that:
* Persists entries (text + timestamp) in JSON.
* Maintains simple word‑set categories that grow as new entries arrive.
* Assigns incoming entries to the best matching category (or creates a new one).
* Retrieves the most similar past entries for a query using cosine similarity
  on term‑frequency vectors.

Only the Python standard library is used.
"""

import json
import os
import time
import math
import string
from pathlib import Path
from collections import Counter, defaultdict
from typing import List, Dict, Tuple

DATA_FILE = Path(__file__).with_name("memory_store.json")


def _load_store() -> Dict:
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    # initial empty structure
    return {"entries": [], "categories": {}}


def _save_store(store: Dict) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)


def _tokenize(text: str) -> List[str]:
    # simple whitespace + punctuation tokenization, lower‑cased
    translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
    clean = text.translate(translator).lower()
    return [t for t in clean.split() if t]


def _vectorize(tokens: List[str]) -> Counter:
    return Counter(tokens)


def _cosine_similarity(v1: Counter, v2: Counter) -> float:
    # dot product
    intersect = set(v1) & set(v2)
    dot = sum(v1[t] * v2[t] for t in intersect)
    norm1 = math.sqrt(sum(c * c for c in v1.values()))
    norm2 = math.sqrt(sum(c * c for c in v2.values()))
    return dot / (norm1 * norm2) if norm1 and norm2 else 0.0


class MemoryBank:
    """Core engine for storing, categorizing and querying memories."""

    def __init__(self):
        self.store = _load_store()
        # cache category word‑sets for fast similarity
        self._cat_wordsets: Dict[str, Counter] = {
            cat: Counter(words) for cat, words in self.store["categories"].items()
        }

    # ------------------------------------------------------------------ #
    # Persistence helpers
    # ------------------------------------------------------------------ #
    def _commit(self):
        # sync categories back to plain word‑list form for JSON
        self.store["categories"] = {
            cat: list(counter.elements()) for cat, counter in self._cat_wordsets.items()
        }
        _save_store(self.store)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def add_entry(self, text: str) -> None:
        """Add a new memory, automatically categorizing it."""
        tokens = _tokenize(text)
        tf = _vectorize(tokens)

        # find best category
        best_cat, best_score = None, 0.0
        for cat, cat_vec in self._cat_wordsets.items():
            score = _cosine_similarity(tf, cat_vec)
            if score > best_score:
                best_cat, best_score = cat, score

        # threshold to decide if we create a new category
        THRESH = 0.25
        if best_score < THRESH or best_cat is None:
            # create a fresh category named after the first few words
            base = "_".join(tokens[:3]) or "misc"
            cat_name = f"{base}_{int(time.time())}"
            self._cat_wordsets[cat_name] = Counter()
            best_cat = cat_name

        # update category word set
        self._cat_wordsets[best_cat].update(tf)

        # store entry
        entry = {
            "id": len(self.store["entries"]),
            "timestamp": time.time(),
            "text": text,
            "category": best_cat,
        }
        self.store["entries"].append(entry)
        self._commit()
        print(f"Added entry #{entry['id']} to category '{best_cat}' (score {best_score:.2f})")

    def query(self, text: str, top_n: int = 5) -> List[Tuple[int, float, str]]:
        """
        Return the top_n most similar past entries.
        Each result is (entry_id, similarity, entry_text).
        """
        query_vec = _vectorize(_tokenize(text))
        scored = []
        for entry in self.store["entries"]:
            entry_vec = _vectorize(_tokenize(entry["text"]))
            sim = _cosine_similarity(query_vec, entry_vec)
            if sim > 0:
                scored.append((entry["id"], sim, entry["text"]))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_n]

    def list_categories(self) -> List[Tuple[str, int]]:
        """Return categories with the number of entries they contain."""
        counts = defaultdict(int)
        for e in self.store["entries"]:
            counts[e["category"]] += 1
        return sorted(counts.items(), key=lambda x: -x[1])

    def dump_memory(self) -> None:
        """Pretty‑print the whole memory store (for debugging)."""
        for cat, size in self.list_categories():
            print(f"\nCategory '{cat}' – {size} entries:")
            for e in self.store["entries"]:
                if e["category"] == cat:
                    ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(e["timestamp"]))
                    print(f"  [{e['id']}] ({ts}) {e['text']}")


# ---------------------------------------------------------------------- #
# Simple interactive demo (run the script directly)
# ---------------------------------------------------------------------- #
if __name__ == "__main__":
    mb = MemoryBank()
    print("\n=== Contextual Memory Demo ===")
    while True:
        cmd = input("\nCommand (add/query/list/exit): ").strip().lower()
        if cmd == "add":
            txt = input("Enter memory text: ").strip()
            if txt:
                mb.add_entry(txt)
        elif cmd == "query":
            q = input("Query text: ").strip()
            results = mb.query(q, top_n=3)
            if results:
                print("\nTop matches:")
                for eid, sim, txt in results:
                    print(f"  [{eid}] sim={sim:.2f} → {txt}")
            else:
                print("No similar memories found.")
        elif cmd == "list":
            cats = mb.list_categories()
            print("\nCategories:")
            for name, cnt in cats:
                print(f"  {name}: {cnt} entries")
        elif cmd == "exit":
            print("Good‑bye!")
            break
        else:
            print("Unknown command. Use add, query, list, or exit.")