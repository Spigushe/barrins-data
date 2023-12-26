import json

from mtgdc_carddata import CardDatabase

database = CardDatabase()

if __name__ == "__main__":
    with open("mtgdc_carddata/sticker.json", "w", encoding="utf-8") as file:
        json.dump(
            database.card("Ancestral / Hot Dog / Minotaur"),
            file,
            ensure_ascii=False,
            indent=4,
        )

    with open("mtgdc_carddata/attraction.json", "w", encoding="utf-8") as file:
        json.dump(database.card("Balloon Stand"), file, ensure_ascii=False, indent=4)

    with open("mtgdc_carddata/background.json", "w", encoding="utf-8") as file:
        json.dump(
            database.card("Agent of the Iron Throne"),
            file,
            ensure_ascii=False,
            indent=4,
        )

    with open("mtgdc_carddata/companion.json", "w", encoding="utf-8") as file:
        json.dump(
            database.card("Lurrus of the Dream-Den"), file, ensure_ascii=False, indent=4
        )

    with open("mtgdc_carddata/card.json", "w", encoding="utf-8") as file:
        json.dump(database.card("Counterspell"), file, ensure_ascii=False, indent=4)
