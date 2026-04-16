# challenge4.py — SQL Explorer
# Present an interactive menu that runs different SQL queries on favorites.db.
# Requires favorites.db — see week2/README.md for setup instructions.

import sqlite3

# Your code here

def main():
    # Connect to the database
    conn = sqlite3.connect("favorites.db")
    cursor = conn.cursor()

    # Main interactive loop
    while True:
        print("\n--- Favorites Explorer ---")
        print("1. List all shows")
        print("2. List all people")
        print("3. List all genres")
        print("4. Search shows by title")
        print("5. Search shows by genre")
        print("6. Search shows starring a person")
        print("7. Top-rated shows")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            cursor.execute("SELECT title FROM shows")
            for row in cursor.fetchall():
                print(row[0])

        elif choice == "2":
            cursor.execute("SELECT name FROM people")
            for row in cursor.fetchall():
                print(row[0])

        elif choice == "3":
            cursor.execute("SELECT DISTINCT genre FROM genres")
            for row in cursor.fetchall():
                print(row[0])

        elif choice == "4":
            title = input("Enter title substring: ")
            cursor.execute("SELECT title FROM shows WHERE title LIKE ?", (f"%{title}%",))
            rows = cursor.fetchall()
            if not rows:
                print("No shows found.")
            else:
                for row in rows:
                    print(row[0])

        elif choice == "5":
            genre = input("Enter genre: ")
            cursor.execute(
                "SELECT title FROM shows WHERE id IN "
                "(SELECT show_id FROM genres WHERE genre = ?)",
                (genre,)
            )
            rows = cursor.fetchall()
            if not rows:
                print("No shows found.")
            else:
                for row in rows:
                    print(row[0])

        elif choice == "6":
            name = input("Enter person name: ")
            cursor.execute(
                "SELECT title FROM shows WHERE id IN "
                "(SELECT show_id FROM stars WHERE person_id = "
                "(SELECT id FROM people WHERE name = ?))",
                (name,)
            )
            rows = cursor.fetchall()
            if not rows:
                print("No shows found.")
            else:
                for row in rows:
                    print(row[0])

        elif choice == "7":
            cursor.execute(
                "SELECT title FROM shows WHERE id IN "
                "(SELECT show_id FROM ratings ORDER BY rating DESC LIMIT 10)"
            )
            rows = cursor.fetchall()
            if not rows:
                print("No rating data available.")
            else:
                for row in rows:
                    print(row[0])

        elif choice == "8":
            break

        else:
            print("Invalid choice. Please try again.")

    # Close the connection when done
    conn.close()

if __name__ == "__main__":
    main()