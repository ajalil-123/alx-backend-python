
# Objective: create a decorator that caches the results of a database queries inorder to avoid redundant calls

# Instructions:

# Complete the code below by implementing a decorator cache_query(func) that caches query results based on the SQL query string


import sqlite3
import functools
import time

# Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper





# Cache dictionary to store query results
query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Fetching result from cache...")
            return query_cache[query]
        else:
            print("Querying database...")
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
#print(users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)