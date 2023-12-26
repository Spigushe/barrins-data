import gzip
import json
import os
import re
from datetime import datetime, timedelta

import requests


class CardDatabase:
    def __init__(self) -> None:
        self._mtgjson = "https://mtgjson.com/api/v5/AtomicCards.json.gz"
        self._filepath = "mtgdc_carddata/AtomicCards.json.gz"

        if not os.path.isfile(self._filepath) or self._file_older_than(
            self._filepath, 7
        ):
            self._download(self._mtgjson, self._filepath)

        self.atomic_cards = json.load(gzip.open(self._filepath))["data"]

    def _file_older_than(self, filepath: str, age: int):
        file_timestamp = os.path.getmtime(filepath)
        file_timestamp = datetime.fromtimestamp(file_timestamp)
        current_time = datetime.now()
        return (current_time - file_timestamp) > timedelta(days=age)

    def _download(self, link: str, filepath: str):
        response = requests.get(link, stream=True)
        with open(filepath, "wb") as file:
            file.write(response.content)

    def card(self, card_name) -> dict:
        if card_name in self.atomic_cards.keys():
            return self.atomic_cards[card_name][0]

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
