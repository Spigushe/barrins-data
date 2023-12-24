"""
Module pour l'extraction de MTGTOP8 en vue de stocker
et d'analyser les données dans l'objectif de définir
une vue plus précise des archétypes joués avec
`mtgdc-parser` et d'autres outils à venir comme
`mtgdc-aggregator` ou `mtgdc-database`.
"""
import glob
import json
import os
from threading import Thread

from mtgdc_scrapper import Soupe, Tournoi


def get_first_id(path: str) -> str:
    """Fonction qui retour le premier id à exporter."""
    files = glob.glob(os.path.join(path, "*.json"))
    id_tournoi = 2694  # Premier tournoi DC sur mtgtop8 : 2695
    if len(files) > 0:
        id_tournoi = max(
            int(os.path.splitext(os.path.basename(file))[0]) for file in files
        )
    return id_tournoi


def extraction() -> None:
    """Fonctionn principale."""

    path = "mtgdc_decklists/decklists"
    first_id = get_first_id(path)

    def extract_tournoi(event_id: str) -> None:
        print("Tournoi", event_id)
        tournoi = Tournoi(Soupe(f"https://mtgtop8.com/event?e={event_id}"))

        if tournoi.is_commander:
            tournoi_data = tournoi.to_dict()
            with open(
                os.path.join(path, f"{event_id}.json"), "+w", encoding="utf-8"
            ) as json_file:
                json.dump(tournoi_data, json_file, ensure_ascii=False, indent=4)

    # A chaque fois, 1000 extractions par groupe de 10
    threads = []
    for i in range(100):
        threads = [
            Thread(
                target=extract_tournoi,
                args=(first_id + 10 * i + j + 1,),
            )
            for j in range(10)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    extraction()
