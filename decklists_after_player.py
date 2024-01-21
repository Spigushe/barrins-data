import json

from mtgdc_aggregator import Aggregator
from mtgdc_decklists import ImportDecks

players = ["spigushe", "zohoz", "domino", "mars"]

if __name__ == "__main__":
    for player in players:
        decks = ImportDecks.from_directory()
        decks.load_decks(player=player)
        with open(f"output/{player}_palmares.json", "+w") as file:
            json.dump(decks.decks, file, indent=4, ensure_ascii=False)

        aggregation = Aggregator(decks.decklists, ordre=3)
        aggregation.aggregate()
        aggregation.export(f"output/{player}_aggregation.txt")
