# challenge2.py — Two-Column Report
# Read favorites.csv, find the most common problem per language, print a table.

import csv

# Your code here
import csv

try:
    min_votes = int(input("Minimum vote count: "))
except ValueError:
    print("Invalid input. Please enter a number.")
    exit()

counts = {}

try:
    with open("favorites.csv", "r") as file:
        reader = csv.DictReader(file)

        column_name = reader.fieldnames[0]

        for row in reader:
            favorite = row[column_name]


            if favorite in counts:
                counts[favorite] += 1
            else:
                counts[favorite] = 1

    print(f"\nResults (at least {min_votes} votes):")
    for favorite in counts:
        if counts[favorite] >= min_votes:
            print(f"{favorite}: {counts[favorite]}")

except FileNotFoundError:
    print("Error: 'favorites.csv' not found. Make sure the file is in this folder.")
