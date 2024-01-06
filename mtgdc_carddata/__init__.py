import gzip
import json
import os
import re
from datetime import datetime, timedelta

import requests


class MTGJSON:
    def __init__(self) -> None:
        self.allcards = "https://mtgjson.com/api/v5/AtomicCards.json.gz"
        self.allsets = "https://mtgjson.com/api/v5/SetList.json.gz"

    @staticmethod
    def control(wanted: str, path: str):
        mtgjson = MTGJSON()
        url = (
            mtgjson.allcards
            if wanted == "cards"
            else mtgjson.allsets
            if wanted == "sets"
            else None
        )

        if not os.path.isfile(path) or mtgjson._file_older_than(path, 7):
            mtgjson._download(url, path)

    def _file_older_than(self, filepath: str, age: int):
        file_timestamp = os.path.getmtime(filepath)
        file_timestamp = datetime.fromtimestamp(file_timestamp)
        current_time = datetime.now()
        return (current_time - file_timestamp) > timedelta(days=age)

    def _download(self, link: str, filepath: str):
        response = requests.get(link, stream=True)
        with open(filepath, "wb") as file:
            file.write(response.content)


class CardDatabase:
    def __init__(self) -> None:
        self._filepath = "mtgdc_carddata/AtomicCards.json.gz"
        MTGJSON.control("cards", self._filepath)
        self.atomic_cards = json.load(gzip.open(self._filepath))["data"]
        self.sets = SetDatabase()

    def card(self, card_name) -> dict:
        if card_name in self.atomic_cards.keys():
            return self.atomic_cards[card_name][0]

        card_name = re.sub(r'(?<!\s)/(?!\s)', ' / ', card_name)

        if " / " in card_name:
            card_name = re.sub(" / ", " // ", card_name)

        keys = [key for key in self.atomic_cards.keys() if key.startswith(card_name)]

        if len(keys) == 0:
            card_name = re.sub(" // ", " ", card_name)
            keys = [
                key for key in self.atomic_cards.keys() if key.startswith(card_name)
            ]
            if len(keys) == 0:
                print(card_name)

        if len(keys) > 1:
            print(
                card_name,
                "n'est pas une entrée unique. Possibilités uniques:",
                ", ".join(keys),
            )
            print(keys[0], "est retournée par défaut")

        return self.atomic_cards[keys[0]][0]

    def firstprint(self, card_name) -> datetime:
        return datetime.strptime(self.sets.set(self.card(card_name)["firstPrinting"])["releaseDate"], "%Y-%m-%d")

class SetDatabase:
    def __init__(self) -> None:
        self._filepath = "mtgdc_carddata/AllSets.json.gz"
        MTGJSON.control("sets", self._filepath)
        json_file = json.load(gzip.open(self._filepath))["data"]

        self.allsets = {}
        for set in json_file:
            self.allsets[set["code"]] = set

    def set(self, code):
        return self.allsets[code]


class DecklistBuilder:
    def __init__(self) -> None:
        self.database = CardDatabase()
        self.ordre = {
            "Land": 0,
            "Creature": 1,
            "Planeswalker": 2,
            "Instant": 3,
            "Sorcery": 4,
            "Artifact": 5,
            "Enchantment": 6,
            "Battle": 7,
            "Tribal": 10,
        }
        self.decklist = {
            "Creature": [],
            "Planeswalker": [],
            "Instant": [],
            "Sorcery": [],
            "Artifact": [],
            "Enchantment": [],
            "Battle": [],
            "Land": [],
        }

    @staticmethod
    def build_deck(cards_list: dict):
        self = DecklistBuilder()
        for card, qty in cards_list.items():
            types = self.database.card(card)["types"]
            lowest_type = min([self.ordre[item] for item in types])
            self.decklist[{v: k for k, v in self.ordre.items()}[lowest_type]].append(
                f"{qty} {card}"
            )

        tmp = ""
        for key in self.decklist.keys():
            if self.decklist[key]:
                qty = sum(
                    [
                        int("".join(filter(str.isdigit, line)))
                        for line in self.decklist[key]
                    ]
                )
                if key == "Sorcery":
                    tmp += f"\n// Sorceries ({qty})\n"
                else:
                    tmp += f"\n// {key}s ({qty})\n"
                tmp += "\n".join(sorted(self.decklist[key]))
                tmp += "\n"

        return tmp
