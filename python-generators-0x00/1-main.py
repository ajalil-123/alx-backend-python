
#!/usr/bin/python3

from itertools import islice
stream_users = __import__('0-stream_users') # import the module
stream_users = stream_users.stream_users   # Get the function

# iterate over the generator function and print only the first 6 rows

for user in islice(stream_users(), 9):
    print(user)