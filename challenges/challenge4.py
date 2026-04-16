# challenge4.py — SQL Explorer
# Present an interactive menu that runs different SQL queries on favorites.db.
# Requires favorites.db — see week2/README.md for setup instructions.

import sqlite3

# Your code here

def run_query(query):
    """Connects to the DB, executes a query, and prints results."""
    try:
        conn = sqlite3.connect("favorites.db")

        conn.row_factory = sqlite3.Row
        db = conn.cursor()

        rows = db.execute(query).fetchall()

        if not rows:
            print("\nNo results found.")
        else:

            print(f"\n{' | '.join(rows[0].keys())}")
            print("-" * 30)
            for row in rows:
                print(" | ".join(str(value) for value in row))

        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def main():
    while True:
        print("\n--- SQL Explorer Menu ---")
        print("1. Show all favorites")
        print("2. Count occurrences of a specific language")
        print("3. Search by title")
        print("4. Exit")

        choice = input("Select an option (1-4): ")

        if choice == '1':
            run_query("SELECT * FROM favorites")

        elif choice == '2':
            language = input("Enter language (e.g., Python, C, SQL): ")
            run_query(f"SELECT language, COUNT(*) as count FROM favorites WHERE language LIKE '{language}'")

        elif choice == '3':
            title = input("Enter title to search for: ")
            run_query(f"SELECT * FROM favorites WHERE title LIKE '%{title}%'")

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
