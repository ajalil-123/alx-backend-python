# Objective: Run multiple database queries concurrently using asyncio.gather.

# Instructions:

# Use the aiosqlite library to interact with SQLite asynchronously. To learn more about it, click here.

# Write two asynchronous functions: async_fetch_users() and async_fetch_older_users() that fetches all users and users older than 40 respectively.

# Use the asyncio.gather() to execute both queries concurrently.

# Use asyncio.run(fetch_concurrently()) to run the concurrent fetch


import asyncio
import aiosqlite

# Asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

# Asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

# Run both concurrently
async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)

# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
