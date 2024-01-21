from datetime import datetime

from mtgdc_aggregator import Aggregator
from mtgdc_decklists import ImportDecks

if __name__ == "__main__":
    players = ["spigushe", "zohoz", "domino", "mars"]

    for player in players:
        decks = ImportDecks.from_directory()
        decks.load_decks(date_from=datetime(2022, 9, 1), player=player)
        decks.palmares(f"output/{player}_palmares.txt", use_url=True)

        aggregation = Aggregator(decks.decklists, ordre=3, use_banlist=False)
        aggregation.aggregate()
        aggregation.export(f"output/{player}_aggregation.txt")
