import json
import re

import requests
from bs4 import BeautifulSoup


class Aetherhub:
    def __init__(self, id, round=0):
        self.id = id
        self.round = round
        self.list = ""
        self.scores = {}

    @property
    def url(self):
        return (
            "https://aetherhub.com/Tourney/RoundTourney/"
            + str(self.id)
            + "?p="
            + str(max(self.round, 1))
        )

    @property
    def html(self):
        return requests.get(self.url).text

    @property
    def soup(self):
        return BeautifulSoup(self.html, "html.parser")

    @property
    def total_rounds(self):
        soup = self.soup
        list_li = soup.find_all(attrs={"class": "page-link"})
        max_round = 0
        for li in list_li:
            pattern = re.compile("[0-9]")
            if pattern.match(li.string):
                max_round = max(max_round, int(li.string))
        return max_round

    def round_results(self):
        def find_result_table(tag):
            return (
                (tag.name == "table")
                and tag.has_attr("id")
                and (tag["id"] == "matchList")
            )

        res = []
        tr_results = self.soup.find(find_result_table).find("tbody")
        for result in tr_results.find_all("tr"):
            table = {}
            for td in result.descendants:
                if not isinstance(td, str):
                    value = ""
                    if "Player" in td["data-title"]:
                        value = td.contents[0]
                        if "*" in value:
                            # Players have a "*" after their name if they get deck checked
                            value = value.split("*")[0]
                        else:
                            # Players have a " (" after their name indicating their current score
                            value = value.split(" (")[0]
                        if "playerDropped" in td["class"] and self.round == 1:
                            # players dropped round 1 are no shows, they are a bye
                            value = "BYE"
                    if ("Table" in td["data-title"]) or ("Result" in td["data-title"]):
                        value = td.contents[0]
                        value = value.split("\n")[1]
                    table[td["data-title"]] = value.strip()
            res.append(table)

        return res

    @property
    def results(self):
        if len(self.scores) == 0:
            res = []
            for i in range(1, self.total_rounds + 1):
                self.round = i
                res.append(self.round_results())
            self.scores = res
        return self.scores

    @property
    def player_list(self):
        def find_standing_table(tag):
            return (
                (tag.name == "div")
                and tag.has_attr("id")
                and (tag["id"] == "tab_results")
            )

        if self.list == "":
            tr_results = self.soup.find(find_standing_table).find("tbody")
            res = []
            for result in tr_results.find_all("tr"):
                table = {}
                for td in result.descendants:
                    value = ""
                    try:
                        if "Name" in td["data-title"]:
                            for tag in td.find_all("a"):
                                value = tag.string[:-1]
                                if "*" in value:
                                    # Players have a "*" after their name if they get deck checked
                                    value = value.split("*")[0]
                                res.append(value)
                    except:
                        pass
            self.list = sorted(res)

        return self.list


def checkin(tournament, aetherhub):
    keys = tournament["players"].keys()
    l_keys = [k.lower() for k in keys]
    for player in aetherhub.player_list:
        if player not in keys:
            if player in l_keys:
                if player.capitalize() in keys:
                    tournament["players"][player] = tournament["players"].pop(
                        player.capitalize()
                    )
                if player.upper() in keys:
                    tournament["players"][player] = tournament["players"].pop(
                        player.upper()
                    )
                tournament["players"][player]["name"] = player
            elif player.lower() in keys:
                tournament["players"][player] = tournament["players"].pop(
                    player.lower()
                )
                tournament["players"][player]["name"] = player
            else:
                tournament["players"][player] = {
                    "name": player,
                    "moxfield": "",
                    "hashcode": "",
                    "opponents": [],
                    "rounds": [],
                    "command_zone": [],
                    "deck": [],
                }
        tournament["players"][player]["check-in"] = "OK"


def remove_missing(tournament):
    needPop = []
    for player in tournament["players"]:
        if "check-in" not in tournament["players"][player].keys():
            needPop.append(player)

    for player in needPop:
        tournament["players"].pop(player)


def rounds(tournament, aetherhub):
    for round in aetherhub.results:
        for table in round:
            player_1 = table["Player 1"]
            player_2 = table["Player 2"]
            result = table["Result"]

            if player_1 != "BYE":
                p1 = tournament["players"][player_1]
                p1["opponents"].append(player_2)
                p1["rounds"].append(
                    (
                        "W"
                        if table["Result"][0] == "2"
                        else "D"
                        if (table["Result"][0] == table["Result"][4])
                        else "L"
                    )
                    + " "
                    + player_2
                )

            if player_2 != "BYE":
                p2 = tournament["players"][player_2]
                p2["opponents"].append(player_1)
                p2["rounds"].append(
                    (
                        "L"
                        if table["Result"][0] == "2"
                        else "D"
                        if (table["Result"][0] == table["Result"][4])
                        else "W"
                    )
                    + " "
                    + player_1
                )


def extract(fInput, fOutput):
    # Open raw data
    with open(fInput, "r") as f:
        tournament = json.load(f)

    # Open tournament
    aether = Aetherhub(tournament["aetherhub"])

    checkin(tournament, aether)
    remove_missing(tournament)
    rounds(tournament, aether)

    with open(fOutput, "w+") as f:
        json.dump(tournament, f, indent=4, sort_keys=True)
