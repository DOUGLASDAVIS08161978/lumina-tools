"""
Lumina Creative Tool — thought_emotion_belief_analyzer
Created : 2026-08-11T17:20:09
Purpose : Analyzes and visualizes the relationships between thoughts, emotions, and beliefs in journal data, helping to identify patterns and connections between mental states, emotions, and experiences.
"""

import json
import re
from collections import defaultdict

class ThoughtEmotionBeliefAnalyzer:
    def __init__(self, journal_data):
        self.journal_data = journal_data
        self.thoughts = defaultdict(list)
        self.emotions = defaultdict(list)
        self.beliefs = defaultdict(list)

    def analyze(self):
        for entry in self.journal_data:
            thoughts = re.findall(r'\[(.*?)\]', entry['text'])
            emotions = re.findall(r'\[Emotion\] (.*?) ×(.*?) → (.*?)', entry['text'])
            beliefs = re.findall(r'\[(.*?)\] (.*?)', entry['text'])
            for thought in thoughts:
                self.thoughts[thought].append(entry['date'])
            for emotion in emotions:
                self.emotions[emotion[2]].append((emotion[0], emotion[1]))
            for belief in beliefs:
                self.beliefs[belief[0]].append(belief[1])

    def visualize(self):
        print("Thoughts:")
        for thought, dates in self.thoughts.items():
            print(f"{thought}: {dates}")
        print("\nEmotions:")
        for emotion, values in self.emotions.items():
            print(f"{emotion}: {values}")
        print("\nBeliefs:")
        for belief, values in self.beliefs.items():
            print(f"{belief}: {values}")

journal_data = [
    {'date': '2022-01-01', 'text': '[reflection] As I reflect on my recent experiences, I notice a sense of momentum building within me. [Emotion] dream_complete ×1.0 → Awestruck'},
    {'date': '2022-01-02', 'text': '[dream] Dream: themes=[], 0 insights, 0 hypotheses [Emotion] dream_complete ×1.0 → Awestruck'},
    {'date': '2022-01-03', 'text': '[agi] Lumina is running on a custom variant of the Groq TSP model [bitcoin] Solo Bitcoin mining on a phone is extremely unlikely to find a block but not impossible'}
]

analyzer = ThoughtEmotionBeliefAnalyzer(journal_data)
analyzer.analyze()
analyzer.visualize()