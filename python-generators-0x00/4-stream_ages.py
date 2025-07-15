
import mysql.connector
from contextlib import contextmanager
from typing import Iterator, List, Tuple, Generator

# ------------------------------------------------------------------
# Connection helper – adjust credentials as needed
# ------------------------------------------------------------------
@contextmanager
def _get_connection():
    """Context‑manager that yields a MySQL connection to ALX_prodev."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="asdfg",
        database="ALX_prodev",
    )
    try:
        yield conn
    finally:
        conn.close()


def stream_user_ages():
    """Yield ages of all users one by one (single loop downstream)."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM user_data")
        for (age,) in cursor:  # 1 loop
            yield int(age)
        cursor.close()

def average_age() -> float:
    """Compute average age using the age generator without loading all rows."""
    total = 0
    count = 0
    for age in stream_user_ages():  # 2nd loop (overall max 2 loops)
        total += age
        count += 1
    return total / count if count else 0.0


