import os
import requests
import time
import json


# Local storage definitions
ITEM_BASE_DIR = "data/items"
ITEM_BASE_NAME = "{item_type}.json"
ITEM_CACHE_DIR = "data/items/{item_type}"
ITEM_CACHE_NAME = "{item_type}_lvl{level}.json"

# Header requests and endpoints
HTTP_HEADERS = {
    "Wanikani-Revision": "20170710",
    "Authorization": "Bearer {wk_token}",
}
API_MAIN = "https://api.wanikani.com/v2/"
API_SUBJECTS = "subjects"


def cache_items(wk_token: str, status: bool = False):
    """Main function to cache WaniKani subject items."""
    if status:
        os.makedirs(ITEM_BASE_DIR, exist_ok=True)

        for item_type in ["radical", "kanji", "vocabulary"]:
            print(f"Caching WaniKani {item_type} items:")

            # Setup cache and base files and direcory
            base_fp = os.path.join(ITEM_BASE_DIR, ITEM_BASE_NAME.format(item_type=item_type))
            file_status(base_fp)
            cache_dir = ITEM_CACHE_DIR.format(item_type=item_type)
            os.makedirs(cache_dir, exist_ok=True)
            
            # Cache items by level
            for level in range(1, 61):
                cache_fn = ITEM_CACHE_NAME.format(item_type=item_type, level=level)
                cache_fp = os.path.join(cache_dir, cache_fn)
                file_status(cache_fp)

                # Get and save cache file
                cache_data: list = get_cache_item(wk_token, item_type, level)
                with open(cache_fp, 'wb') as file:
                    file.write(json.dumps(cache_data, ensure_ascii=False, indent=4).encode("utf8"))

            # Combine cache files
            base_data = []
            cache_files = os.listdir(cache_dir)
            for cache_file in cache_files:
                cache_fp = os.path.join(cache_dir, cache_file)
                with open(cache_fp, 'r') as input:
                    base_data.extend(json.load(input))
            with open(base_fp, 'wb') as output:
                output.write(json.dumps(base_data, ensure_ascii=False, indent=4).encode("utf8"))
            
            print(f"Finished caching {item_type} items.\n")
    else:
        print("WaniKani items update not initialized.")


def file_status(filepath: str) -> str:
    """Indicator whether the file is new or existing."""
    if os.path.isfile(filepath):
        print(f"! Overwriting '{filepath}'")
    else:
        print(f"- Creating '{filepath}'")


def filter_cache_item(data: list, item_type: str) -> dict:
    """Filter raw WaniKani item data for the given item type."""
    if item_type == "radical":
        char_image = None
        for image in data["data"]["character_images"]:
            if image["content_type"] == "image/png" and image["metadata"]["style_name"] == "original":
                char_image = image["url"]
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


def get_cache_item(wk_token: str, item_type: str, level: int) -> list:
    """Requests WaniKani subjects using its API based on item_type and level."""

    # Load API token into headers
    HTTP_HEADERS["Authorization"] = HTTP_HEADERS["Authorization"].format(
        wk_token=wk_token)

    # Assemble query
    url = API_MAIN + API_SUBJECTS
    if item_type:
        if level:
            url += f"?types={item_type}&levels={level}"
        else:
            url += f"?types={item_type}"
    elif level:
        url += f"?levels={level}"

    # Execute requests
    req = requests.get(url, headers=HTTP_HEADERS)
    time.sleep(0.5)

    # Filter output data based on item_type
    data: list = req.json()["data"]
    data_filtered: list = [filter_cache_item(
        field, item_type) for field in data]

    return data_filtered
