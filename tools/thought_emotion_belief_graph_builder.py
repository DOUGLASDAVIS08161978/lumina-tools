"""
Lumina Creative Tool — thought_emotion_belief_graph_builder
Created : 2026-08-11T22:03:36
Purpose : A tool that analyzes and visualizes the relationships between thoughts, emotions, and beliefs, and saves the resulting graph to a JSON file.
"""

import json
import collections
from pathlib import Path

class ThoughtEmotionBeliefGraph:
    def __init__(self, data):
        self.data = data
        self.graph = collections.defaultdict(list)

    def build_graph(self):
        for entry in self.data:
            thoughts = entry['thoughts']
            emotions = entry['emotions']
            beliefs = entry['beliefs']
            for thought in thoughts:
                for emotion in emotions:
                    self.graph[thought].append(emotion)
                for belief in beliefs:
                    self.graph[thought].append(belief)

    def visualize_graph(self):
        print("Thought-Emotion-Belief Graph:")
        for thought, connections in self.graph.items():
            print(f"{thought}: {connections}")

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f)

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def main():
    data_filename = 'thought_emotion_belief_data.json'
    data = load_data(data_filename)
    graph = ThoughtEmotionBeliefGraph(data)
    graph.build_graph()
    graph.visualize_graph()
    graph.save_to_json('thought_emotion_belief_graph.json')

if __name__ == '__main__':
    main()