# starter.py — Survey Dashboard
# Project 4 | Hard | 60–90 minutes (split across 2 sessions)
#
# Run from this folder:
#   python starter.py
#
# Split the work across four roles — see README.md for the role breakdown.

import csv
import sqlite3

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — CREATE THE DATABASE AND TABLE
# ulpiana
# ══════════════════════════════════════════════════════════════════════════════

conn = sqlite3.connect("survey.db")
db   = conn.cursor()

# Columns: student_id TEXT, faculty TEXT, year INTEGER,
#          satisfaction INTEGER, favourite_tool TEXT, comments TEXT
#
# Hint:
# db.execute('''CREATE TABLE IF NOT EXISTS responses (
#     ...
# )''')

db.execute('''CREATE TABLE IF NOT EXISTS responses (
    student_id TEXT,
    faculty TEXT,
    year INTEGER,
    satisfaction INTEGER,
    favourite_tool TEXT,
    comments TEXT
)''')

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — READ ALL THREE CSV FILES AND INSERT ROWS
# (Coder A) ana
# ══════════════════════════════════════════════════════════════════════════════
csv_files = [
    "faculty_science.csv",
    "faculty_arts.csv",
    "faculty_business.csv",
]

for filename in csv_files:
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
              # TODO: Insert each row into the responses table
            # Use ? placeholders — NEVER string formatting for SQL
            # db.execute("INSERT INTO responses VALUES (?, ?, ?, ?, ?, ?)", (...))
            db.execute("INSERT INTO responses VALUES (?, ?, ?, ?, ?, ?)", (
                row["student_id"],
                row["faculty"],
                int(row["year"]),
                int(row["satisfaction"]),
                row["favourite_tool"],
                row["comments"]
            ))

conn.commit()
print("Database loaded successfully.\n")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — DASHBOARD QUERIES
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 30)
print("  UNIVERSITY SURVEY DASHBOARD")
print("=" * 30)

# ── Query 1: Total responses by faculty ───────────────────────────────────────
print("\n1. Total Responses by Faculty")

rows = db.execute("SELECT faculty, COUNT(*) AS n FROM responses GROUP BY faculty ORDER BY faculty").fetchall()
total = 0
for faculty, n in rows:
    print(f"   {faculty:<10}: {n}")
    total += n
print(f"   {'TOTAL':<10}: {total}")

# ── Query 2: Average satisfaction by year ─────────────────────────────────────
print("\n2. Average Satisfaction by Year of Study")

rows = db.execute("SELECT year, ROUND(AVG(satisfaction), 1) AS avg_sat FROM responses GROUP BY year ORDER BY year").fetchall()
for year, avg_sat in rows:
    print(f"   Year {year} : {avg_sat} / 5")

# ── Query 3: Favourite tool popularity ───────────────────────────────────────
print("\n3. Favourite Tool Popularity")

rows = db.execute("SELECT favourite_tool, COUNT(*) AS n FROM responses GROUP BY favourite_tool ORDER BY n DESC").fetchall()
for tool, n in rows:
    print(f"   {tool:<15} {n:>3}")

# ── Query 4: Faculty comparison table ────────────────────────────────────────
print("\n4. Faculty Comparison")
print(f"   {'Faculty':<12} | {'Avg Satisfaction':<18} | Most Popular Tool")
print("   " + "-" * 50)

faculties = ["Arts", "Business", "Science"]
for faculty in faculties:
    avg_row = db.execute(
        "SELECT ROUND(AVG(satisfaction), 1) FROM responses WHERE faculty = ?",
        (faculty,)
    ).fetchone()
    tool_row = db.execute(
        "SELECT favourite_tool, COUNT(*) AS n FROM responses WHERE faculty = ? GROUP BY favourite_tool ORDER BY n DESC LIMIT 1",
        (faculty,)
    ).fetchone()
    print(f"   {faculty:<12} | {avg_row[0]:<18} | {tool_row[0]}")

# ── Query 5: Interactive filter ──────────────────────────────────────────────
print()
try:
    min_score = int(input("Enter minimum satisfaction score (1-5): "))
except ValueError:
    print("Invalid input. Defaulting to 4.")
    min_score = 4

rows = db.execute(
    "SELECT student_id, faculty, year, favourite_tool FROM responses WHERE satisfaction >= ? ORDER BY faculty, year",
    (min_score,)
).fetchall()

print(f"\nStudents with satisfaction >= {min_score}:")
if not rows:
    print("  No results found.")
for student_id, faculty, year, tool in rows:
    print(f"  {student_id:<4} | {faculty:<8} | Year {year} | {tool}")

# ══════════════════════════════════════════════════════════════════════════════
# CLEANUP
# ══════════════════════════════════════════════════════════════════════════════
conn.close()
