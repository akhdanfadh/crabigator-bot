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


def find_item(data, name):
    """Find an item from WaniKani items data."""
    for item in data:
        meanings = [meaning.lower() for meaning in item["meanings"]]
        if name == item["char"] or name.lower() in meanings:
            return item