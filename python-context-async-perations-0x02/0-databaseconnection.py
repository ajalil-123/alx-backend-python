# Objective: create a class based context manager to handle opening and closing database connections automatically

# Instructions:

# Write a class custom context manager DatabaseConnection using the __enter__ and the __exit__ methods

# Use the context manager with the with statement to be able to perform the query SELECT * FROM users. Print the results from the query.



import sqlite3

class DatabaseConnection():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor 
    

    def __exit__(self, type, value, traceback):
        if self.conn:
            self.conn.close()


# Usage: Query all users
if __name__ == "__main__":
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)