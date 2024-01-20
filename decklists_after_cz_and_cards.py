import os

from mtgdc_aggregator import Aggregator
from mtgdc_decklists import ImportDecks

COMMANDER = "Kroxa"
CARDS = ["Worldgorger Dragon"]

if __name__ == "__main__":
    str_joined = ("".join(filter(str.isalpha, COMMANDER + "".join(CARDS)))).lower()
    path = "output/" + str_joined

    if not os.path.isdir("output"):
        os.mkdir("output")
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        for root, dirs, files in os.walk(path):
            for file in files:
                os.remove(os.path.join(root, file))

    print(".", "Loading decks")
    liste_decks = ImportDecks.from_directory("./mtgdc_decklists/decklists")
    liste_decks.load_decks(commander=[COMMANDER], cards=CARDS)
    print("\t", f"{len(liste_decks.decklists)} decks loaded")

    print(".", "Aggregating loaded decklists")
    aggregate = Aggregator(liste_decks.decklists, order=3)
    aggregate.aggregate()
    aggregate.export(f"{path}/{str_joined}.txt")
