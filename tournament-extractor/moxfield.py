import json
import re

import requests


def get_moxfield_decklist(link):
    if "moxfield" in link:
        link = re.split("/", link)[-1]
    url = "https://api.moxfield.com/v2/decks/all/"
    deck_json = requests.get(url + link).json()
    return deck_json


def get_card_data(card):
    return {
        "key": card["card"]["scryfall_id"],
        "name": re.split(" // ", card["card"]["name"])[0],
        "types": card["card"]["type"],
        "count": card["quantity"],
    }


def add_to_type(deck: dict, name: str, quantity: int, type: str):
    if type == "0":
        deck[type]["cards"].append(name)
    else:
        deck[type]["cards"].append(str(quantity) + " " + name)


def build_deck(list):
    deck = {
        "0": {"name": "Command Zone", "cards": []},
        "1": {"name": "Planeswalkers", "cards": []},
        "2": {"name": "Creatures", "cards": []},
        "3": {"name": "Sorceries", "cards": []},
        "4": {"name": "Instants", "cards": []},
        "5": {"name": "Artifacts", "cards": []},
        "6": {"name": "Enchantments", "cards": []},
        "7": {"name": "Lands", "cards": []},
    }
    for k, v in list["mainboard"].items():
        card = get_card_data(v)
        add_to_type(deck, card["name"], card["count"], card["types"])

    for k, v in list["commanders"].items():
        card = get_card_data(v)
        add_to_type(deck, card["name"], 1, "0")

    return deck


def extract(fInput, fOutput):
    # Open raw data
    with open(fInput, "r") as f:
        tournament = json.load(f)

    for deck in tournament["players"]:
        try:
            display = build_deck(
                get_moxfield_decklist(tournament["players"][deck]["moxfield"])
            )
            # Command Zone
            cz = display.pop("0")
            tournament["players"][deck]["command_zone"] = cz["cards"]
            # Main
            for item in display.keys():
                tournament["players"][deck]["deck"].extend(display[item]["cards"])
        except:
            pass

    with open(fOutput, "w+") as f:
        json.dump(tournament, f, indent=4)
