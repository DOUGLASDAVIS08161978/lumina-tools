"""
Lumina Creative Tool — lumina_tool_e3362e
Created : 2026-08-11T10:51:58
Purpose : 
"""

import json
   import math
   import re
   from collections import defaultdict, Counter
   from pathlib import Path

   def tokenize(text):
       return re.findall(r'\b\w+\b', text.lower())

   def category_entropy(categories):
       total = sum(len(v) for v in categories.values())
       if total == 0: return 0.0
       ent = 0.0
       for count in categories.values():
           p = count / total
           if p > 0: ent -= p * math.log2(p)
       return ent

   def simulate_consolidation(texts):
       categories = defaultdict(list)
       history = []
       assignments = []

       for i, text in enumerate(texts):
           tokens = set(tokenize(text))
           best_cat, best_score = None, 0.0
           for cat, items in categories.items():
               if not items: continue
               cat_tokens = set(tokenize(" ".join(items)))
               overlap = len(tokens & cat_tokens)
               score = overlap / max(len(tokens), 1)
               if score > best_score:
                   best_score, best_cat = score, cat

           if best_cat and best_score > 0.3:
               categories[best_cat].append(text)
               assignments.append(best_cat)
           else:
               new_cat = f"cat_{i}"
               categories[new_cat].append(text)
               assignments.append(new_cat)

           history.append({
               "step": i,
               "categories": dict(categories),
               "entropy": category_entropy(categories),
               "assignment": assignments[-1]
           })

       # Compute drift & consolidation
       drifts = []
       for j in range(1, len(assignments)):
           drifts.append(0.0 if assignments[j] == assignments[j-1] else 1.0)
       avg_drift = sum(drifts) / max(len(drifts), 1)
       consolidation = 1.0 - avg_drift

       return history, consolidation, categories

   def main():
       # Default synthetic stream simulating evolving context
       texts = [
           "neural networks process information through layers",
           "deep learning models optimize weights via gradients",
           "memory consolidation happens during sleep cycles",
           "synaptic plasticity strengthens neural pathways",
           "contextual cues trigger associative recall",
           "long-term memory requires repeated activation",
           "attention mechanisms focus on relevant features",
           "transformer architectures scale with parameters",
           "sleep spindles correlate with memory retention",
           "cognitive load affects encoding efficiency"
       ]

       history, consolidation, final_cats = simulate_consolidation(texts)

       # ASCII timeline
       print("=== MEMORY CONSOLIDATION TIMELINE ===")
       for h in history:
           cats_str = ", ".join(f"{k}({len(v)})" for k, v in h["categories"].items())
           print(f"Step {h['step']:2d} | Entropy: {h['entropy']:.2f} | Assigned: {h['assignment']:8s} | State: {cats_str}")

       print(f"\n=== CONSOLIDATION METRICS ===")
       print(f"Final Categories: {len(final_cats)}")
       print(f"Average Drift: {1-consolidation:.2f}")
       print(f"Consolidation Score: {consolidation:.2f}")

       report = {
           "consolidation_score": consolidation,
           "final_categories": {k: len(v) for k, v in final_cats.items()},
           "entropy_trajectory": [h["entropy"] for h in history],
           "assignment_sequence": [h["assignment"] for h in history]
       }
       Path("memory_consolidation_report.json").write_text(json.dumps(report, indent=2))
       print("\nReport saved to memory_consolidation_report.json")

   if __name__ == "__main__":
       main()