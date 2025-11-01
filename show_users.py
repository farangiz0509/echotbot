import json

with open("users.json", "r", encoding="utf-8") as f:
    users = json.load(f)

if not users:
    print("No users found.")
else:
    print("Users who started the bot:")
    for user in users:
        print(f"ID: {user.get('id')}, Name: {user.get('first_name')}, Username: {user.get('username')}")
