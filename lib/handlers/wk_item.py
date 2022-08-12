import os
import requests
import time
import json

from lib.utils.constants import ITEM_TYPE, ITEM_DB_FILE


def find_item(char: str, database: list):
    """Find an item from WaniKani items data."""
    for item in database:
        meanings = [meaning.lower() for meaning in item["meanings"]]
        if char == item["char"] or char.lower() in meanings:
            return item
    return None


def load_item_db(wk_token: str, item_dbs: dict, cache: bool = False):
    """Main function to load WaniKani subject items to the bot."""
    os.makedirs("data/items", exist_ok=True)
    
    if cache:
        for item_type, name in ITEM_TYPE.items():
            name = name.lower()
            print(f"Caching WaniKani {name} items:")

            # Setup cache and base files and direcory
            base_fp = ITEM_DB_FILE[item_type]
            file_status(base_fp)
            cache_dir = f"data/items/{name}"
            os.makedirs(cache_dir, exist_ok=True)
            
            # Cache items by level
            for level in range(1, 61):
                cache_fp = os.path.join(cache_dir, f"{name}_lvl{level}.json")
                file_status(cache_fp)
                cache_data = cache_item(wk_token, name, level)
                with open(cache_fp, 'wb') as output:
                    output.write(json.dumps(cache_data, ensure_ascii=False, indent=4, default=str).encode("utf8"))

            # Combine cache files
            item_db = []
            for cache_file in os.listdir(cache_dir):
                with open(os.path.join(cache_dir, cache_file), 'r') as input:
                    item_db.extend(json.load(input))
            with open(base_fp, 'wb') as output:
                output.write(json.dumps(item_db, ensure_ascii=False, indent=4, default=str).encode("utf8"))
            
            print(f"Finished caching {name} items.")
    else:
        print("Items not renewed.")
    
    # Now load the data
    for type, file in ITEM_DB_FILE.items():
        with open(file, "r") as data:
            item_dbs[type] = json.load(data)
            print(f"- {file} loaded")


def file_status(filepath: str):
    """Indicator whether the file is new or existing."""
    if os.path.isfile(filepath):
        print(f"! Overwriting '{filepath}'")
    else:
        print(f"- Creating '{filepath}'")


def filter_raw_cache(data: list, item_type: str) -> dict:
    """Filter raw WaniKani item data for the given item type."""
    if item_type == "radical":
        for image in data["data"]["character_images"]:
            if image["content_type"] == "image/png" and image["metadata"]["style_name"] == "original":
                char_image = image["url"]
            else:
                char_image = None
        meanings = [meaning["meaning"] for meaning in data["data"]["meanings"]]
        return {
            "id": data["id"],
            "item_type": data["object"],
            "level": data["data"]["level"],
            "url": data["data"]["document_url"],
            "char": data["data"]["characters"],
            "char_image": char_image,
            "meanings": meanings,
            "meaning_mnemonic": data["data"]["meaning_mnemonic"]
        }

    elif item_type == "kanji":
        meanings = [meaning["meaning"] for meaning in data["data"]["meanings"]]
        readings = {
            "onyomi": None,
            "kunyomi": None,
            "nanori": None
        }
        for reading in data["data"]["readings"]:
            reading_type = reading["type"]
            if readings[reading_type] is None:
                readings[reading_type] = [reading["reading"]]
            else:
                readings[reading_type].append(reading["reading"])
        return {
            "id": data["id"],
            "item_type": data["object"],
            "level": data["data"]["level"],
            "url": data["data"]["document_url"],
            "char": data["data"]["characters"],
            "meanings": meanings,
            "meaning_mnemonic": data["data"]["meaning_mnemonic"],
            "meaning_hint": data["data"]["meaning_hint"],
            "readings": readings,
            "reading_mnemonic": data["data"]["reading_mnemonic"],
            "reading_hint": data["data"]["reading_hint"]
        }
        
    elif item_type == "vocabulary":
        meanings = [meaning["meaning"] for meaning in data["data"]["meanings"]]
        readings = [reading["reading"] for reading in data["data"]["readings"]]
        return {
            "id": data["id"],
            "item_type": data["object"],
            "level": data["data"]["level"],
            "url": data["data"]["document_url"],
            "char": data["data"]["characters"],
            "meanings": meanings,
            "meaning_mnemonic": data["data"]["meaning_mnemonic"],
            "readings": readings,
            "reading_mnemonic": data["data"]["reading_mnemonic"],
        }


def cache_item(wk_token: str, item_type: str, level: int) -> list:
    """Requests WaniKani subjects using its API based on item_type and level."""
    # Execute requests
    endpoint = f"https://api.wanikani.com/v2/subjects?types={item_type}&levels={level}"
    req = requests.get(endpoint, headers={
        "Authorization": f"Bearer {wk_token}"
    })
    time.sleep(0.5)

    # Filter output data based on item_type
    data_raw = req.json()["data"]
    data_filtered = [filter_raw_cache(item, item_type) for item in data_raw]
    return data_filtered