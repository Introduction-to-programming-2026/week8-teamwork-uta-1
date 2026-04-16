# challenge1.py — Frequency Filter
# Read favorites.csv, ask for a minimum vote count, print filtered results.
# No starter hints — build this from scratch using what you learned in week1 and week2.

import csv

# Your code here

from collections import Counter

# Ask the user for a minimum vote count
min_votes = int(input("Minimum number of votes: "))

# Read favorites.csv from the same folder
problems = []
with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        problems.append((row["problem"], row["language"]))

# Count frequency of each (problem, language) pair
counts = Counter(problems)

# Print results that meet the threshold, sorted by votes descending
for (problem, language), votes in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    if votes >= min_votes:
        print(f"{problem} ({language}) - {votes} votes")
