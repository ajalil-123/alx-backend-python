
#!/usr/bin/env python3

import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

#connects to MySQL server
def connect_db( host = "localhost", user= "root", password = "asdfg"):
    return mysql.connector.connect(host=host, user=user,password = password)


def create_database(connection, db_name="ALX_prodev"):
    """Create database if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.close()

# connect directly to ALX_prodev database

def connect_to_prodev(host="localhost",user="root", password="asdfg", db="ALX_prodev"):
    return mysql.connector.connect(host=host, user=user, password=password, database=db)


# -------- schema helpers -------- #
def create_table(conn):
    """Create user_data table if it doesn't exist."""
    create_sql = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL(3,0) NOT NULL,
        INDEX (user_id)
    )
    """
    cursor = conn.cursor()
    cursor.execute(create_sql)
    cursor.close()

# -------- data loader -------- #
import uuid
import csv

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        for row in reader:
            if len(row) != 3:
                print(f"Skipping invalid row: {row}")
                continue

            name, email, age = row
            user_id = str(uuid.uuid4())

            # Optional: check if email already exists
            cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
            if cursor.fetchone():
                continue

            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, age))

    connection.commit()
    cursor.close()
    print("Table user_data created successfully")


def load_csv(csv_path="user_data.csv"):
    """Yield (name, email, age) from CSV (header: name,email,age)."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row["name"], row["email"], row["age"]


