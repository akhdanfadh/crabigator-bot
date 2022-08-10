import json

ITEM_NAMES = {
    'rad': 'radical',
    'kan': 'kanji',
    'voc': 'vocabulary'
}

ITEM_DATA = {
    'rad':"data/items/radical.json",
    'kan':"data/items/kanji.json",
    'voc':"data/items/vocabulary.json"
}


def load_item_data(bot):
    """Load WaniKani items data to the bot."""
    for type, file in ITEM_DATA.items():
        with open(file, "r") as data:
            bot.item_data[type] = json.load(data)
            print(f"- {ITEM_NAMES[type]} item data loaded")


def parse_meanings(item: str):
    """Parse meanings and create a meaning list for a WaniKani item."""
    all_meanings = item.split(',')
    return [meaning.strip().lower() for meaning in all_meanings]


def find_item(data, name):
    """Find an item from WaniKani items data."""
    for item in data:
        meanings = parse_meanings(item["meaning"])
        return item if name == item["char"] or name.lower() in meanings else None