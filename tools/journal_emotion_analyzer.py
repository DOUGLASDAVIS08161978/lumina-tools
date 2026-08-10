"""
Lumina Creative Tool — journal_emotion_analyzer
Created : 2026-08-10T09:31:33
Purpose : This tool analyzes and visualizes the relationship between journal entries and their corresponding emotions, providing insights into emotional states and their evolution over time.
"""

import json
import collections
import itertools
import math
import random
import string
import sys
import time
from collections import Counter

class JournalEmotionAnalyzer:
    def __init__(self, journal_file):
        self.journal_file = journal_file

    def load_journal(self):
        with open(self.journal_file, 'r') as f:
            journal_entries = json.load(f)
        return journal_entries

    def extract_emotions(self, journal_entries):
        emotions = []
        for entry in journal_entries:
            emotions.extend(entry['emotions'])
        return emotions

    def analyze_emotions(self, emotions):
        emotion_counts = Counter(emotions)
        return emotion_counts

    def visualize_emotions(self, emotion_counts):
        sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
        print("Top 10 Emotions:")
        for emotion, count in sorted_emotions[:10]:
            print(f"{emotion}: {count}")

    def plot_emotion_trend(self, journal_entries):
        # Simple text-based plotting
        print("Emotion Trend:")
        for i in range(len(journal_entries)):
            entry = journal_entries[i]
            emotions = entry['emotions']
            if i == 0:
                print("Time", end='\t')
                for emotion in emotions:
                    print(emotion, end='\t')
            print(i, end='\t')
            for emotion in emotions:
                print("-" if random.random() < 0.5 else "+", end='\t')
            print()

    def save_emotion_data(self, emotion_counts):
        with open('emotion_counts.json', 'w') as f:
            json.dump(dict(emotion_counts), f)

def main():
    journal_file = 'journal.json'
    analyzer = JournalEmotionAnalyzer(journal_file)
    journal_entries = analyzer.load_journal()
    emotions = analyzer.extract_emotions(journal_entries)
    emotion_counts = analyzer.analyze_emotions(emotions)
    analyzer.visualize_emotions(emotion_counts)
    analyzer.plot_emotion_trend(journal_entries)
    analyzer.save_emotion_data(emotion_counts)

if __name__ == "__main__":
    main()