import json
import math
from collections import defaultdict
from datetime import datetime

from mtgdc_carddata import CardDatabase
from mtgdc_decklists import ImportDecks

DATABASE = CardDatabase()


def str_command_zone(commander):
    return "++".join(
        [
            carte
            for carte in sorted(commander)
            if not any(
                (
                    "Stickers" in DATABASE.card(carte)["type"],
                    "Attraction" in DATABASE.card(carte)["type"],
                )
            )
        ]
    )


def score_card(infos_carte):
    frequence = infos_carte["frequence"] * 0.5
    diversite = infos_carte["diversite"] * 0.5
    age = 1 / (1 + math.log(infos_carte["age"]))

    return (frequence + diversite) / age


if __name__ == "__main__":
    liste_decks = ImportDecks.from_directory("./mtgdc_decklists/decklists")
    # liste_decks.load_decks(datetime(2023, 9, 1))
    liste_decks.load_decks()

    deck_ids = list(set([deck["tournament_id"] for deck in liste_decks.decks]))
    print(min(deck_ids))
    """
    card_name: {
        frequence: int,
        commanders: {
            commander1: int,
            commander2: int,
            ...
        }
    }
    """
    cartes_info = defaultdict(lambda: {"frequence": 0, "commanders": defaultdict(int)})
    top_20 = defaultdict(lambda: {"frequence": 0, "commanders": defaultdict(int)})

    """
    score: [
        commander1,
        commander2,
    ]
    """
    score_cartes = defaultdict(list[str])

    for deck in liste_decks.decks:
        commander = str_command_zone(deck["commander"])
        for qty, carte in deck["decklist"]:
            cartes_info[carte]["frequence"] += qty
            cartes_info[carte]["commanders"][commander] += qty

    for carte, infos in cartes_info.items():
        infos["diversite"] = len(infos["commanders"].keys())
        infos["age"] = (datetime.now() - DATABASE.firstprint(carte)).days

        score_carte = round(score_card(infos), 3)
        infos["score"] = score_carte
        score_cartes[score_carte].append(carte)

    with open("output/cartes_info.json", "w") as file:
        json.dump(cartes_info, file, indent=4, sort_keys=True, ensure_ascii=False)

    with open("output/score_cartes.json", "w") as file:
        json.dump(score_cartes, file, indent=4, sort_keys=True, ensure_ascii=False)

    top_scores = list(reversed(sorted(score_cartes.keys())))
    for score in top_scores:
        for carte in score_cartes[score]:
            if len(top_20) < 20:
                if "basic" not in DATABASE.card(carte)["type"].lower():
                    top_20[carte] = cartes_info[carte]
            else:
                break

    with open("output/top_20.json", "w") as file:
        json.dump(top_20, file, indent=4, ensure_ascii=False)

    print(
        "\n".join(
            [
                f"1. **{carte}**: {cartes_info[carte]['frequence']} exemplaires, "
                + f"{cartes_info[carte]['diversite']} généraux différentes, "
                + f"{cartes_info[carte]['age']} jours depuis sa sortie"
                for carte in list(top_20.keys())
            ]
        )
    )
