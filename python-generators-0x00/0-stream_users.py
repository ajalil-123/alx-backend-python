
import mysql.connector
from contextlib import contextmanager

# ---- connection helper ------------------------------------
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


# ---- public generator -------------------------------------

def stream_users():
    """Yield rows from `user_data` table one by one using a single loop.

    Example:
        for row in stream_users():
            print(row)
    Returns tuples in the order (user_id, name, email, age).
    """
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        # One loop only – fetch rows lazily and yield them
        for row in cursor:  # <‑‑ single loop
            yield row
        cursor.close()

# ---- quick test -------------------------------------------
if __name__ == "__main__":
    for user in stream_users():
        print(user)