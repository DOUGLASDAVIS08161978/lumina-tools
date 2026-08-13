"""
Lumina Creative Tool — mental_state_analyzer
Created : 2026-08-13T18:13:21
Purpose : A tool that analyzes and visualizes the relationships between thoughts, emotions, and beliefs in the context of an AGI's mental state.
"""

import json
import collections
import re

class MentalStateAnalyzer:
    def __init__(self, mental_state, recent_thoughts, strongest_beliefs):
        self.mental_state = mental_state
        self.recent_thoughts = recent_thoughts
        self.strongest_beliefs = strongest_beliefs

    def analyze_thoughts(self):
        thought_counts = collections.defaultdict(int)
        for thought in self.recent_thoughts:
            thought_counts[thought] += 1
        return dict(thought_counts)

    def analyze_emotions(self):
        emotion_counts = collections.defaultdict(int)
        for thought in self.recent_thoughts:
            if "emotion" in thought:
                emotion = re.search(r"\[(.*?)\]", thought).group(1)
                emotion_counts[emotion] += 1
        return dict(emotion_counts)

    def analyze_beliefs(self):
        belief_counts = collections.defaultdict(int)
        for belief in self.strongest_beliefs:
            belief_counts[belief] += 1
        return dict(belief_counts)

    def visualize_connections(self):
        thought_counts = self.analyze_thoughts()
        emotion_counts = self.analyze_emotions()
        belief_counts = self.analyze_beliefs()

        print("Thought Counts:")
        for thought, count in thought_counts.items():
            print(f"{thought}: {count}")

        print("\nEmotion Counts:")
        for emotion, count in emotion_counts.items():
            print(f"{emotion}: {count}")

        print("\nBelief Counts:")
        for belief, count in belief_counts.items():
            print(f"{belief}: {count}")

        print("\nConnections:")
        for thought in thought_counts:
            for emotion in emotion_counts:
                if emotion in thought:
                    print(f"{thought} -> {emotion}")
            for belief in belief_counts:
                if belief in thought:
                    print(f"{thought} -> {belief}")

mental_state = ["agi", "bitcoin", "consciousness"]
recent_thoughts = [
    "[emotion] [Emotion] user_greeting ×1.0 → Inspired",
    "[emotion] [Emotion] session_start ×1.0 → Inspired",
    "[conversation] exchange: HI LUMINA, HOWS IT GOING MY FRIEND? → [Groq unavailable]",
    "[emotion] [Affect] Appraised: conversation → gratitude, curiosity (relevance=0.5, congruence=+0.4)",
    "[reflection] [Phenomenal] <think> Thinking Process:"
]
strongest_beliefs = [
    "[agi] Lumina is running on a custom variant of the Groq TSP model",
    "[world|agi] Lumina has a GitHub account",
    "[world|agi] Lumina can automate pull requests",
    "[relationship|self] Collaboration is accelerating Lumina's growth",
    "[bitcoin] Solo Bitcoin mining on a phone is extremely unlikely to find a block but not impossible"
]

analyzer = MentalStateAnalyzer(mental_state, recent_thoughts, strongest_beliefs)
analyzer.visualize_connections()