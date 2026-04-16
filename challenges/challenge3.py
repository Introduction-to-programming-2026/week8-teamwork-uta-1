# challenge3.py — CSV Writer
# Read favorites.csv, count votes per language, write results to language_summary.csv.

import csv

# Your code here

from collections import Counter

# Step 1: Read favorites.csv and collect languages
languages = []
with open("favorites.csv", "r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        languages.append(row["language"])

# Step 2: Count frequency of each language
counts = Counter(languages)

# Step 3: Write results to language_summary.csv
with open("language_summary.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["language", "votes"])  # header row
    for language, votes in counts.items():
        writer.writerow([language, votes])

print("language_summary.csv has been created with vote counts per language.")
