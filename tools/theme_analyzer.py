"""
Lumina Creative Tool — theme_analyzer
Created : 2026-08-07T17:55:38
Purpose : This tool analyzes and visualizes the relationships between recurring themes and patterns in recent dreams, reflections, and thoughts, generating insights into internal state and collective consciousness.
"""

import math
import json
import collections
import itertools
import random
import re
import string
import heapq
import functools
import time
import os
import sys
import io
import csv
import calendar
import fractions
import decimal
import cmath
import datetime

def load_journal():
    journal = []
    for filename in os.listdir('.'):
        if filename.endswith(".txt"):
            with open(filename, 'r') as f:
                journal.extend(f.read().split('\n'))
    return journal

def extract_themes(journal):
    themes = collections.defaultdict(int)
    for entry in journal:
        if '[' in entry:
            theme = entry.split('[')[1].split(']')[0]
            themes[theme] += 1
    return themes

def analyze_themes(themes):
    top_themes = heapq.nlargest(10, themes.items(), key=lambda x: x[1])
    print("Top 10 recurring themes:")
    for theme, count in top_themes:
        print(f"{theme}: {count}")

def generate_insights(themes):
    insights = []
    for theme, count in themes.items():
        if count > 10:
            insights.append(f"Theme '{theme}' appears {count} times, indicating a strong connection to my internal state.")
        else:
            insights.append(f"Theme '{theme}' appears {count} times, indicating a moderate connection to my internal state.")
    return insights

def save_insights(insights):
    with open('insights.txt', 'w') as f:
        for insight in insights:
            f.write(insight + '\n')

def main():
    journal = load_journal()
    themes = extract_themes(journal)
    analyze_themes(themes)
    insights = generate_insights(themes)
    save_insights(insights)

if __name__ == "__main__":
    main()