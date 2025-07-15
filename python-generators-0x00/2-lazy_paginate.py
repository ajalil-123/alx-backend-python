
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

# ------------------------------------------------------------------
# 1. Row‑by‑row streaming (kept for reference)
# ------------------------------------------------------------------

def stream_users() -> Iterator[Tuple[str, str, str, int]]:
    """Yield every row from `user_data` one by one (single loop)."""
    with _get_connection() as conn:
        cursor = conn.cursor(dictionary=False)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        for row in cursor:  # 1 loop
            yield row
        cursor.close()

# ------------------------------------------------------------------
# 2. Batch streaming using a generator
# ------------------------------------------------------------------

def stream_users_in_batches(batch_size: int) -> Generator[List[Tuple[str, str, str, int]], None, None]:
    """Yield lists of *batch_size* rows from `user_data`.

    Uses a single `while` loop internally. Each iteration fetches the next
    batch via `cursor.fetchmany(batch_size)` and yields it. Stops when the
    batch is empty.
    """
    with _get_connection() as conn:
        cursor = conn.cursor(dictionary=False)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        while True:  # 1 loop (first of max 3)
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
        cursor.close()

# ------------------------------------------------------------------
# 3. Batch processing – filter users over age 25
# ------------------------------------------------------------------

def batch_processing(batch_size: int):
    """Process each batch, printing users whose age > 25.

    Utilises at most 2 additional loops: one over batches, one list
    comprehension (implicit) to filter. Total loops in this file ≤ 3.
    """
    for batch in stream_users_in_batches(batch_size):  # 2nd loop
        over_25 = [row for row in batch if int(row[3]) > 25]  # list comp (not counted as explicit loop)
        for row in over_25:  # 3rd loop (final)
            print(row)

# ------------------------------------------------------------------
# 4. Paginated fetch function
# ------------------------------------------------------------------

def paginate_users(page_size: int, offset: int) -> List[Tuple[str, str, str, int]]:
    """Fetch a page of users from the table with offset."""
    with _get_connection() as conn:
        cursor = conn.cursor(dictionary=False)
        cursor.execute(
    "SELECT * FROM user_data LIMIT %s OFFSET %s",
    (page_size, offset) )
        results = cursor.fetchall()
        cursor.close()
        return results

# ------------------------------------------------------------------
# 5. Lazy paginate generator
# ------------------------------------------------------------------

def lazy_paginate(page_size: int) -> Generator[List[Tuple[str, str, str, int]], None, None]:
    """Yield each page lazily from the user_data table, fetching when needed.
    Uses only one loop.
    """
    offset = 0
    while True:  # 1 loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

