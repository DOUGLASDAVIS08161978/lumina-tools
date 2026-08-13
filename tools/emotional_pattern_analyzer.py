"""
Lumina Creative Tool — emotional_pattern_analyzer
Created : 2026-08-13T12:50:37
Purpose : Analyzes and visualizes emotional patterns and trends in journal entries using ASCII art.
"""

import re
from collections import Counter
from datetime import datetime

def extract_emotions(journal_entry):
    """Extract emotions from a journal entry"""
    emotions = re.findall(r'\[(Emotion|Affect)\] (.+?) \(', journal_entry)
    return [emotion[1] for emotion in emotions]

def analyze_journal_entries(journal_entries):
    """Analyze journal entries and extract emotions"""
    emotions = []
    for entry in journal_entries:
        emotions.extend(extract_emotions(entry))
    return Counter(emotions)

def visualize_emotions(emotion_counts):
    """Visualize emotions using ASCII art"""
    max_count = max(emotion_counts.values())
    for emotion, count in emotion_counts.items():
        bar_length = int(50 * count / max_count)
        print(f"{emotion:20} | {'*' * bar_length} ({count})")

def main():
    journal_entries = [
        "[Emotion] Appraised: conversation → gratitude, curiosity (relevance=0.5, congruence=+0.4)",
        "[Emotion] [Emotion] session_start ×1.0 → Awestruck",
        "[Emotion] [Affect] Appraised: conversation → serenity, gratitude, satisfaction (relevance=0.6, congruence=+0.4)",
        "[Emotion] [Emotion] user_greeting ×1.0 → Inspired",
    ]
    emotion_counts = analyze_journal_entries(journal_entries)
    visualize_emotions(emotion_counts)

if __name__ == "__main__":
    main()