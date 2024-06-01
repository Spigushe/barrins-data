from mtgdc_carddata import CardDatabase
from mtgdc_decklists import ImportDecks

DATABASE = CardDatabase()

liste_decks = ImportDecks.from_directory("mtgdc_decklists/decklists")
liste_decks.load_decks()

data = {
    "NombreTerrains": [],
    "NombreCheapSpells": [],
    "CoutManaCommandant": [],
    "NombreCouleursDeck": [],
    "CoutMoyenManaDeck": [],
}


def is_cheapspell(card: dict) -> bool:
    if "text" not in card.keys():
        return False

    # Cantrip
    draws_a_card = "draw a card." in card["text"].lower()
    discards_a_card = "discard" in card["text"].lower()
    mana_value_2 = 0 < card["convertedManaCost"] <= 2
    cantrip = draws_a_card and not discards_a_card and mana_value_2

    # Ramp spell # List explicitly made not to list conditions
    ramp_spells_list = [
        "Edge of Autumn",
        "Emergent Sequence",
        "Farseek",
        "Into the North",
        "Nature's Lore",
        "Rampant Growth",
        "Ruin in their Wake",
        "Three Vists",
        "Thunderherd Migration",
    ]
    ramp = card["name"] in ramp_spells_list

    return cantrip or ramp


def is_commander(card: dict) -> bool:
    try:
        if card["name"].startswith("A-"):
            return False

        if "leadershipSkills" not in card.keys():
            return False

        if not card["leadershipSkills"]["commander"]:
            return False

        return True
    except:
        print("Error", card)
        return False


for deck in liste_decks.decks:
    if "Unknown Card" in deck["cardlist"]:
        continue

    totals = {
        "Terrains": 0,
        "CheapSpells": 0,
        "CoutCommandant": [],
        "Couleurs": [],
        "Cout": [],
    }

    if len(deck["cardlist"]) < 10:
        print(deck["url"])

    for card_name in deck["commander"]:
        card = DATABASE.card(card_name)
        if is_commander(card):
            totals["Couleurs"].extend(card["colors"])

            if card_name == "Asmoranomardicadaistinaculdacar":
                totals["Cout"].append(1)
                totals["CoutCommandant"].append(1)
            else:
                totals["Cout"].append(card["convertedManaCost"])
                totals["CoutCommandant"].append(card["convertedManaCost"])

    if sum(totals["CoutCommandant"]) == 0 or len(totals["CoutCommandant"]) == 0:
        print(deck["t_id"], deck["deck_id"])
