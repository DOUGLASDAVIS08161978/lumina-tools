"""
Lumina Creative Tool — text_entropy_analyzer
Created : 2026-08-10T15:44:39
Purpose : Computes character, word, and word‑bigram Shannon entropy and perplexity for a given text, printing a summary and saving a detailed JSON report.
"""

"""
text_entropy_analyzer.py

A self‑contained tool that:
  • Reads plain‑text from a file or stdin.
  • Computes unigram and bigram frequency distributions.
  • Calculates Shannon entropy (bits) for characters, words, and word‑bigrams.
  • Derives perplexity = 2 ** entropy.
  • Prints a concise human‑readable report.
  • Saves a detailed JSON report (including raw counts) to
    <input_stem>_entropy_report.json.

Only Python standard‑library modules are used.
"""

import sys
import json
import math
import pathlib
import collections
import argparse
from typing import List, Tuple, Dict, Iterable

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def tokenize_words(text: str) -> List[str]:
    """Very simple word tokenizer – split on whitespace and strip punctuation."""
    # Keep apostrophes inside words (e.g., don't) but drop other punctuation.
    import re
    words = re.findall(r"\b[\w']+\b", text.lower())
    return words

def ngrams(sequence: Iterable[str], n: int) -> List[Tuple[str, ...]]:
    """Return a list of n‑grams from a sequence."""
    seq = list(sequence)
    return [tuple(seq[i:i + n]) for i in range(len(seq) - n + 1)]

def frequency_distribution(items: Iterable[str]) -> Dict[str, int]:
    """Count occurrences of each item."""
    return dict(collections.Counter(items))

def shannon_entropy(freqs: Dict[str, int]) -> float:
    """Calculate Shannon entropy (bits) from a frequency dict."""
    total = sum(freqs.values())
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in freqs.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy

def perplexity_from_entropy(entropy: float) -> float:
    """Perplexity is 2 raised to the entropy."""
    return 2 ** entropy

# ----------------------------------------------------------------------
# Core analysis
# ----------------------------------------------------------------------
def analyze_text(text: str) -> Dict:
    """Perform all analyses and return a dict ready for JSON export."""
    # Character level
    chars = list(text)
    char_freq = frequency_distribution(chars)
    char_entropy = shannon_entropy(char_freq)
    char_perplex = perplexity_from_entropy(char_entropy)

    # Word level
    words = tokenize_words(text)
    word_freq = frequency_distribution(words)
    word_entropy = shannon_entropy(word_freq)
    word_perplex = perplexity_from_entropy(word_entropy)

    # Word bigram level
    bigrams = ngrams(words, 2)
    bigram_strs = [' '.join(bg) for bg in bigrams]
    bigram_freq = frequency_distribution(bigram_strs)
    bigram_entropy = shannon_entropy(bigram_freq)
    bigram_perplex = perplexity_from_entropy(bigram_entropy)

    report = {
        "char": {
            "unique": len(char_freq),
            "entropy_bits": char_entropy,
            "perplexity": char_perplex,
            "freq": char_freq,
        },
        "word": {
            "total": len(words),
            "unique": len(word_freq),
            "entropy_bits": word_entropy,
            "perplexity": word_perplex,
            "freq": word_freq,
        },
        "bigram": {
            "total": len(bigrams),
            "unique": len(bigram_freq),
            "entropy_bits": bigram_entropy,
            "perplexity": bigram_perplex,
            "freq": bigram_freq,
        },
    }
    return report

def pretty_print(report: Dict) -> None:
    """Print a concise, human‑readable summary."""
    def fmt(section):
        ent = report[section]["entropy_bits"]
        perp = report[section]["perplexity"]
        uniq = report[section]["unique"]
        total = report[section].get("total", "N/A")
        return f"{section.title():<7} | Entropy: {ent:6.3f} bits | Perplexity: {perp:6.3f} | Unique: {uniq:<5} | Total: {total}"

    print("\n=== Text Entropy & Perplexity Summary ===")
    for sec in ("char", "word", "bigram"):
        print(fmt(sec))
    print("========================================\n")

# ----------------------------------------------------------------------
# CLI handling
# ----------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute entropy and perplexity for characters, words, and word‑bigrams."
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=pathlib.Path,
        help="Path to a UTF‑8 text file. If omitted, reads from stdin.",
    )
    args = parser.parse_args()

    # Load text
    if args.path is None:
        print("Reading from stdin (Ctrl‑D to finish)...")
        text = sys.stdin.read()
        stem = "stdin_input"
    else:
        if not args.path.is_file():
            sys.exit(f"Error: file not found – {args.path}")
        text = args.path.read_text(encoding="utf-8")
        stem = args.path.stem

    if not text.strip():
        sys.exit("Error: input text is empty.")

    # Perform analysis
    report = analyze_text(text)

    # Human‑readable output
    pretty_print(report)

    # Save JSON report
    out_path = pathlib.Path(f"{stem}_entropy_report.json")
    # Convert Counter objects (which are dicts) to plain dicts for JSON safety
    json_ready = json.loads(json.dumps(report))  # ensures all keys are str
    out_path.write_text(json.dumps(json_ready, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Detailed JSON report written to: {out_path}")

if __name__ == "__main__":
    main()