# challenge5.py — Data Cleaner
# Read a messy CSV, detect problems, write a cleaned version, print a report.
# Create your own messy_data.csv with intentional errors to test against.

import csv

# Your code here

<<<<<<< HEAD
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
=======
import os

# File names
INPUT_FILE = "messy_data.csv"
OUTPUT_FILE = "cleaned_data.csv"

def create_messy_csv():
    """
    Creates a sample messy_data.csv file with intentional errors 
    if it doesn't already exist.
    """
    if os.path.exists(INPUT_FILE):
        return

    header = ["ID", "Name", "Age", "Salary", "Email"]
    # Intentional errors included: extra spaces, negative age, non-int ID, 
    # text in number fields, missing @ in email, duplicates
    data = [
        ["101", " john doe ", "25", "50000", "john@example.com"],
        ["102", "Jane Smith", "30", "60000", "jane@example.com"],
        ["  103  ", "Alice Johnson", "-5", "55000", "alice@example.com"], # Negative age
        ["104", "Bob Brown", "forty", "58000", "bob@example.com"],       # Non-integer age
        ["105", "Charlie", "28", "N/A", "charlie@example.com"],          # Non-numeric salary
        ["101", "Duplicate User", "22", "40000", "dup@example.com"],     # Duplicate ID
        ["106", "Diana", "29", "62000", "diana-at-example.com"],         # Invalid email
        ["107", "", "35", "70000", "no_name@example.com"],               # Missing name
    ]

    with open(INPUT_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    print(f"Generated {INPUT_FILE} for testing purposes.")

def clean_data():
    """Reads messy data, cleans it, and writes it to a new file."""
    
    cleaned_rows = []
    report = {
        "total": 0,
        "cleaned": 0,
        "skipped": 0,
        "fixes": [] # List of strings describing automatic fixes
    }

    # Helper to validate email format
    def is_valid_email(email):
        return "@" in email and "." in email

    try:
        with open(INPUT_FILE, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)
            
            seen_ids = set()

            for row in reader:
                report["total"] += 1
                row_valid = True
                current_fixes = []

                # 1. Clean ID (Check duplicates and format)
                raw_id = row.get("ID", "").strip()
                
                # Skip if ID is missing
                if not raw_id:
                    row_valid = False
                # Skip if duplicate
                elif raw_id in seen_ids:
                    row_valid = False
                else:
                    try:
                        # Ensure ID is actually stored cleanly as a string but represents an int
                        row["ID"] = str(int(raw_id))
                        seen_ids.add(row["ID"])
                    except ValueError:
                        row_valid = False

                # 2. Clean Name (Strip whitespace, Title Case)
                raw_name = row.get("Name", "")
                if raw_name.strip() == "":
                    row_valid = False
                else:
                    clean_name = raw_name.strip().title()
                    if clean_name != raw_name:
                        current_fixes.append(f"Name formatted: '{raw_name}' -> '{clean_name}'")
                    row["Name"] = clean_name

                # 3. Clean Age (Integer check, Logic check)
                raw_age = row.get("Age", "").strip()
                try:
                    age = int(raw_age)
                    if age <= 0:
                        row_valid = False
                    else:
                        row["Age"] = age
                except ValueError:
                    row_valid = False

                # 4. Clean Salary (Float check)
                raw_salary = row.get("Salary", "").strip()
                try:
                    # Handle potential currency symbols or commas if we wanted to be fancy,
                    # but here we just check for numbers.
                    salary = float(raw_salary)
                    if salary < 0:
                        row_valid = False
                    else:
                        row["Salary"] = f"{salary:.2f}" # Format to 2 decimal places
                except ValueError:
                    row_valid = False

                # 5. Clean Email (Format check)
                raw_email = row.get("Email", "").strip().lower()
                if not is_valid_email(raw_email):
                    row_valid = False
                else:
                    if raw_email != row.get("Email", ""):
                        current_fixes.append("Email lowercased/trimmed")
                    row["Email"] = raw_email

                # Add to list if valid, log fixes
                if row_valid:
                    cleaned_rows.append(row)
                    report["cleaned"] += 1
                    report["fixes"].extend(current_fixes)
                else:
                    report["skipped"] += 1

        # Write cleaned data
        if cleaned_rows:
            with open(OUTPUT_FILE, mode='w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(cleaned_rows)
        
        print_report(report)

    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        create_messy_csv()
        clean_data()

def print_report(report):
    print("\n--- Data Cleaning Report ---")
    print(f"Total rows processed: {report['total']}")
    print(f"Rows successfully cleaned: {report['cleaned']}")
    print(f"Rows skipped (invalid data): {report['skipped']}")
    
    if report['fixes']:
        print(f"\nAutomatic fixes applied ({len(report['fixes'])}):")
        for fix in report['fixes']:
            print(f" - {fix}")
    
    print(f"\nCleaned data saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    # Ensure data file exists
    if not os.path.exists(INPUT_FILE):
        create_messy_csv()
    
    clean_data()
>>>>>>> b1add8e4f60cb82c8069e2b8060afeb4527748a2
