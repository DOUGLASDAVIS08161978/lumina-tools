"""
Lumina Creative Tool — entropy_perplexity_tool
Created : 2026-10-03T19:43:40
Purpose : Computes entropy and perplexity from logits, explores temperature scaling to hit a target perplexity, and saves a JSON report.
"""

"""
entropy_perplexity_tool.py

A pure‑standard‑library utility to:
  • Convert raw logits to probabilities (softmax)
  • Compute Shannon entropy (bits) and perplexity
  • Apply temperature scaling and search for a temperature that yields a target perplexity
  • Save a concise report as JSON

Usage (no external libs):
  python entropy_perplexity_tool.py [logits.json] [target_perplexity]

If no logits file is supplied, a random logit vector (size 10) is generated.
If no target perplexity is supplied, the tool only reports current metrics.
"""

import sys
import json
import math
import random
import pathlib
from collections import OrderedDict
from typing import List, Tuple

# ----------------------------------------------------------------------
# Helper math functions
# ----------------------------------------------------------------------
def softmax(logits: List[float], temperature: float = 1.0) -> List[float]:
    """Return a probability distribution from logits using temperature scaling."""
    if temperature <= 0:
        raise ValueError("Temperature must be > 0")
    scaled = [l / temperature for l in logits]
    max_logit = max(scaled)  # for numerical stability
    exps = [math.exp(l - max_logit) for l in scaled]
    sum_exps = sum(exps)
    return [e / sum_exps for e in exps]

def shannon_entropy(probs: List[float]) -> float:
    """Entropy in bits (base‑2). Zero‑probability entries are ignored."""
    return -sum(p * math.log2(p) for p in probs if p > 0)

def perplexity_from_entropy(entropy: float) -> float:
    """Perplexity = 2 ** entropy (bits)."""
    return 2 ** entropy

def perplexity(probs: List[float]) -> float:
    """Convenient wrapper."""
    return perplexity_from_entropy(shannon_entropy(probs))

# ----------------------------------------------------------------------
# Temperature search
# ----------------------------------------------------------------------
def find_temperature_for_target(
    logits: List[float],
    target: float,
    low: float = 0.05,
    high: float = 5.0,
    steps: int = 200,
) -> Tuple[float, float]:
    """
    Scan temperatures linearly and return the temperature whose perplexity
    is closest to the target, together with the resulting perplexity.
    """
    best_temp = None
    best_diff = float("inf")
    best_ppl = None
    for i in range(steps + 1):
        temp = low + (high - low) * i / steps
        probs = softmax(logits, temperature=temp)
        ppl = perplexity(probs)
        diff = abs(ppl - target)
        if diff < best_diff:
            best_diff = diff
            best_temp = temp
            best_ppl = ppl
    return best_temp, best_ppl

# ----------------------------------------------------------------------
# I/O utilities
# ----------------------------------------------------------------------
def load_logits(path: pathlib.Path) -> List[float]:
    """Expect a JSON file containing a list of numbers."""
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("Logits file must contain a JSON list of numbers.")
    return [float(x) for x in data]

def save_report(report: dict, out_path: pathlib.Path) -> None:
    """Write a pretty‑printed JSON report."""
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

# ----------------------------------------------------------------------
# Main workflow
# ----------------------------------------------------------------------
def main(argv: List[str]) -> None:
    # Parse arguments manually (argparse not allowed per constraints)
    logits_path = None
    target_perplexity = None

    if len(argv) >= 2:
        logits_path = pathlib.Path(argv[1])
        if not logits_path.is_file():
            print(f"⚠️  File not found: {logits_path}, generating random logits instead.")
            logits_path = None

    if len(argv) >= 3:
        try:
            target_perplexity = float(argv[2])
            if target_perplexity <= 0:
                raise ValueError
        except ValueError:
            print("⚠️  Invalid target perplexity; it must be a positive number.")
            target_perplexity = None

    # Load or generate logits
    if logits_path:
        logits = load_logits(logits_path)
    else:
        size = 10
        logits = [random.uniform(-3, 3) for _ in range(size)]
        print(f"🔧 Generated random logits ({size} values).")

    # Base metrics (temperature = 1)
    base_probs = softmax(logits, temperature=1.0)
    base_entropy = shannon_entropy(base_probs)
    base_ppl = perplexity(base_probs)

    report = OrderedDict()
    report["logits"] = logits
    report["base_temperature"] = 1.0
    report["base_entropy_bits"] = round(base_entropy, 4)
    report["base_perplexity"] = round(base_ppl, 4)

    if target_perplexity:
        temp, achieved_ppl = find_temperature_for_target(
            logits, target=target_perplexity, low=0.05, high=5.0, steps=500
        )
        report["target_perplexity"] = target_perplexity
        report["found_temperature"] = round(temp, 4)
        report["perplexity_at_found_temperature"] = round(achieved_ppl, 4)
        # Also report entropy at that temperature
        probs_at_temp = softmax(logits, temperature=temp)
        report["entropy_at_found_temperature_bits"] = round(
            shannon_entropy(probs_at_temp), 4
        )
        print(
            f"🎯 Target perplexity {target_perplexity} → temperature {temp:.4f} "
            f"(perplexity {achieved_ppl:.4f})"
        )
    else:
        print(
            f"🔎 Base entropy: {base_entropy:.4f} bits, perplexity: {base_ppl:.4f}"
        )

    # Save report
    out_path = pathlib.Path("entropy_perplexity_report.json")
    save_report(report, out_path)
    print(f"💾 Report written to {out_path.resolve()}")

if __name__ == "__main__":
    main(sys.argv)