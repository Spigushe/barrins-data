# mtgdc_decklists
A repository to store every tournament stored on MTGTOP8.

## What is MTGTOP8?
MTGTOP8 is a website that stores tournaments on every MTG format. This works through a declarative statement made by any user to have their tournament displayed. This is maintained outside of any `Barrin's Codex` projects.

## How is the data stored?
The `decklists` folder contains a set of data extracted from MTGTOP8 as `<tournament_id>?json`. To go to the original source, the `<tournament_id>` needs to be put in the following web adress: `https://mtgtop8.com/event?e=<id_tournoi>`.

Inside every `json` file is a set of data:
```json
{
    "format": "Duel Commander",
    "id": "2696",
    "name": "EDH (Saint-Nazaire)",
    "place": "",
    "players": "65 players",
    "date": "01/04/12",
    "decks": [
        {
            "deck_id": "217420",
            "rank": "1",
            "player": "player_name",
            "commander": [ /* commanders */ ],
            "decklist": [ /* cards */ ]
        }
    ]
}
```
The deck view is available here:`https://mtgtop8.com/event?e=<id_tournoi>&d=<id_deck>`
