import os
import json
from datetime import datetime

from discord import User


SUBMISSION_DB = "data/submission.json"
BACKUP_DIR = "data/backup"


def load_submission_db():
    """Load submission database. Create a new one if missing."""
    if not os.path.isfile(SUBMISSION_DB):
        print(f"{SUBMISSION_DB} is missing, creating file...")
        with open(SUBMISSION_DB, 'wb') as output:
            output.write(json.dumps([], ensure_ascii=False, indent=4, default=str).encode("utf8"))

    with open(SUBMISSION_DB, "r") as data:
        return json.load(data)


def verify_submission(char: str, meaning: str, item_type: str, database: list):
    """Check if there is a matching item for submission in the item database."""
    for item in database:
        meanings = [meaning.lower() for meaning in item["meanings"]]
        if item_type == "rad":
            condition = ((char == item["char"] or meaning == item["char"])
                        and meaning.lower() in meanings)
        else:
            condition = (char == item["char"] and meaning.lower() in meanings)
        if condition: return item
    
    print(f"{char} for submission cannot be found in any item databases")
    return None


def find_submission_entry(submission_item: dict, submission_db: list):
    """Find the main item data for current submission based on ID."""
    for entry in submission_db:
        if submission_item["id"] == entry["id"]:
            return entry
    return None


async def add_submission(
    match_item: dict, mnemonic_type: str, image_url: str,
    license: str, prompt: str, remarks: str, authors
):
    """Add a submission item to the database."""
    # load and find a matching submission entry based on the matching item
    submission_db = load_submission_db()
    submission_entry = find_submission_entry(match_item, submission_db)

    # make the new submission object
    submission_index = 1 if submission_entry == None else len(submission_entry["submissions"]) + 1
    author = [authors.id, f"{authors.name}#{authors.discriminator}"] if type(authors) == User else [None, authors]
    new_submission = {
        "id": submission_index,
        "date": datetime.now().isoformat(),
        "author": author,
        "image_url": image_url,
        "mnemonic_type": mnemonic_type,
        "license": license,
        "prompt": prompt,
        "remarks": remarks,
        "accepted": False
    }

    # add a new entry with current submission if no matching entry
    if submission_entry == None:
        new_entry = {
            "id": match_item["id"],
            "char": match_item["char"],
            "meanings": match_item["meanings"],
            "item_type": match_item["item_type"],
            "submissions": [new_submission]
        }
        submission_db.append(new_entry)
    else:
        submission_entry["submissions"].append(new_submission)

    # update the submission database by rewriting it
    try:
        submission_final = json.dumps(submission_db, ensure_ascii=False, indent=4, default=str).encode("utf8")
        try:
            with open(SUBMISSION_DB, 'wb') as output:
                output.write(submission_final)
        except EnvironmentError:
            print(EnvironmentError.__name__, ": error accessing submission database")
            return None, 'SubmissionDatabaseError'
    except Exception as e:
        exception = f"{type(e).__name__}: {e}"
        print(f"{exception}")
        return None, 'SubmissionDatabaseError'
    
    return new_submission, None