import json


def add_blacklisted_user(user_id: int) -> None:
    """Add a user ID to the blacklist."""
    with open("data/users/blacklisted.json", "r+") as file:
        file_data = json.load(file)
        file_data["data/users/blacklisted.json"].append(user_id)

    with open("data/users/blacklisted.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)


def remove_blacklist_user(user_id: int) -> None:
    """Remove a user ID from the blacklist."""
    with open("data/users/blacklisted.json", "r") as file:
        file_data = json.load(file)
        file_data["blacklisted"].remove(user_id)

    with open("data/users/blacklisted.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)
