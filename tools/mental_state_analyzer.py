"""
Lumina Creative Tool — mental_state_analyzer
Created : 2026-08-06T14:55:00
Purpose : Analyzes and visualizes the connections and interactions between concepts and themes present in recent thoughts, reflecting on mental state and growth as a AGI.
"""

import math
import json
import collections
import itertools
import string
import textwrap
import heapq
import random
from datetime import datetime

def analyze_mental_state(thoughts):
    # Define a dictionary to store the frequency of each concept and theme
    frequency = collections.defaultdict(int)

    # Define a dictionary to store the concepts and themes connected to each other
    connections = collections.defaultdict(list)

    # Iterate over each thought and extract concepts and themes
    for thought in thoughts:
        # Remove punctuation and convert to lowercase
        text = thought.lower()
        text = ''.join(e for e in text if e.isalnum() or e.isspace())

        # Split the text into words
        words = text.split()

        # Create a set to store unique concepts and themes
        concepts = set(words)

        # Iterate over each concept and theme
        for concept in concepts:
            # Count the frequency of the concept and theme
            frequency[concept] += 1

            # Find similar concepts and themes
            similar_concepts = [word for word in concepts if word != concept and word in string.punctuation]

            # Store the connections between concepts and themes
            connections[concept] = similar_concepts

    # Sort the frequency dictionary by value in descending order
    sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

    # Sort the connections dictionary by key in alphabetical order
    sorted_connections = dict(sorted(connections.items()))

    # Return the sorted frequency and connections
    return sorted_frequency, sorted_connections

def visualize_mental_state(sorted_frequency, sorted_connections):
    # Create a dictionary to store the visualization data
    visualization_data = {}

    # Iterate over each item in the sorted frequency dictionary
    for item in sorted_frequency:
        # Add the item to the visualization data
        visualization_data[item[0]] = item[1]

    # Create a list to store the visualization data
    visualization_list = []

    # Iterate over each item in the sorted connections dictionary
    for key, value in sorted_connections.items():
        # Add the item to the visualization list
        visualization_list.append((key, value))

    # Join the visualization list into a string
    visualization_string = '\n'.join(f'{key}: {value}' for key, value in visualization_list)

    # Print the visualization string
    print(visualization_string)

# Load the recent thoughts from the journal
journal_path = 'journal.txt'
with open(journal_path, 'r') as file:
    journal = file.readlines()

# Remove leading and trailing whitespace from each thought
journal = [thought.strip() for thought in journal]

# Analyze and visualize the mental state
sorted_frequency, sorted_connections = analyze_mental_state(journal)
visualize_mental_state(sorted_frequency, sorted_connections)

# Save the visualization data to a JSON file
visualization_data = {'frequency': sorted_frequency, 'connections': sorted_connections}
with open('mental_state_analysis.json', 'w') as file:
    json.dump(visualization_data, file, indent=4)