# challenge5.py — Data Cleaner
# Read a messy CSV, detect problems, write a cleaned version, print a report.
# Create your own messy_data.csv with intentional errors to test against.

import csv

# Your code here

def clean_data(input_file, output_file):
    cleaned_rows = []
    report = {"processed": 0, "fixed": 0, "skipped": 0}

    try:
        with open(input_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                report["processed"] += 1

                name = row['name'].strip().capitalize()
                email = row['email'].strip()

                try:
                    age = int(row['age'].strip())
                except ValueError:
                    age = "N/A" # Fixes 'invalid' or empty ages
                    report["fixed"] += 1

                if not name: # Skip if the name is missing
                    report["skipped"] += 1
                    continue

                cleaned_rows.append({"name": name, "email": email, "age": age})


        with open(output_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'email', 'age'])
            writer.writeheader()
            writer.writerows(cleaned_rows)


        print(f"\nReport: Processed {report['processed']} rows.")
        print(f"Fixed {report['fixed']} issues and skipped {report['skipped']} empty rows.")

    except FileNotFoundError:
        print("Error: Make sure messy_data.csv exists in this folder!")

if __name__ == "__main__":
    clean_data("messy_data.csv", "cleaned_data.csv")
