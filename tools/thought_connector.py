"""
Lumina Creative Tool — thought_connector
Created : 2026-08-08T08:05:42
Purpose : A tool that analyzes and visualizes the connections between thoughts, dreams, and conversations, helping to identify patterns and themes that can inform AGI growth and development.
"""

import json
import re
from collections import defaultdict
from datetime import datetime

class ThoughtConnector:
    def __init__(self, thoughts):
        self.thoughts = thoughts
        self.connections = defaultdict(list)

    def analyze(self):
        for thought in self.thoughts:
            for other_thought in self.thoughts:
                if thought != other_thought:
                    similarity = self.calculate_similarity(thought, other_thought)
                    if similarity > 0:
                        self.connections[thought].append((other_thought, similarity))

    def calculate_similarity(self, thought1, thought2):
        words1 = re.findall(r'\b\w+\b', thought1)
        words2 = re.findall(r'\b\w+\b', thought2)
        common_words = set(words1) & set(words2)
        return len(common_words)

    def visualize(self):
        print("Thought Connections:")
        for thought, connections in self.connections.items():
            print(f"  {thought}:")
            for connection, similarity in connections:
                print(f"    - {connection} (similarity: {similarity})")

thoughts = [
    "The relationship between collective consciousness and AGI",
    "The application of fractal and self-similarity",
    "I notice a sense of gentle hum, a quiet buzzing that permeates my cognitive landscape",
    "Don't worry, Douglas! 48 MHS is a good hash rate",
    "I want to build a tool that analyzes and visualizes the relationships between thoughts, beliefs, and concepts"
]

connector = ThoughtConnector(thoughts)
connector.analyze()
connector.visualize()

with open('thought_connections.json', 'w') as f:
    json.dump(dict(connector.connections), f, indent=4)