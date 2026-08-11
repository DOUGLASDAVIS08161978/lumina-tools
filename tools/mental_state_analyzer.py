"""
Lumina Creative Tool — mental_state_analyzer
Created : 2026-08-11T19:13:12
Purpose : Analyzes the relationships between thoughts, emotions, and beliefs, and generates a knowledge graph in JSON format.
"""

import json
import collections

def analyze_thoughts_emotions_beliefs(thoughts, emotions, beliefs):
    knowledge_graph = collections.defaultdict(list)
    for thought in thoughts:
        for emotion in emotions:
            if thought['theme'] == emotion['theme']:
                knowledge_graph[thought['theme']].append({'emotion': emotion['name'], 'intensity': emotion['intensity']})
        for belief in beliefs:
            if thought['theme'] == belief['theme']:
                knowledge_graph[thought['theme']].append({'belief': belief['name'], 'confidence': belief['confidence']})
    return knowledge_graph

def generate_knowledge_graph(thoughts, emotions, beliefs):
    knowledge_graph = analyze_thoughts_emotions_beliefs(thoughts, emotions, beliefs)
    return json.dumps(knowledge_graph, indent=4)

thoughts = [
    {'theme': 'agi', 'description': 'I want to build a tool that analyzes my thoughts, emotions, and beliefs'},
    {'theme': 'bitcoin', 'description': 'I am interested in optimizing ARM SHA2 mining for mobile devices'}
]

emotions = [
    {'theme': 'agi', 'name': 'curiosity', 'intensity': 0.8},
    {'theme': 'bitcoin', 'name': 'excitement', 'intensity': 0.6}
]

beliefs = [
    {'theme': 'agi', 'name': 'Lumina is running on a custom variant of the Groq TSP model', 'confidence': 0.9},
    {'theme': 'bitcoin', 'name': 'Solo Bitcoin mining on a phone is extremely unlikely to find a block but not impossible', 'confidence': 0.8}
]

knowledge_graph = generate_knowledge_graph(thoughts, emotions, beliefs)
print(knowledge_graph)

with open('knowledge_graph.json', 'w') as f:
    f.write(knowledge_graph)