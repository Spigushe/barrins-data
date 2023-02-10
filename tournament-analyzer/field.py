import json
import re


def get_field(fInput, fOutput):
    with open(fInput, "r") as f:
        tournament = json.load(f)

    temp = {}
    for player in tournament["players"]:
        cz = tournament["players"][player]["command_zone"]
        if len(cz) > 1:
            cz.sort()
            cz1 = re.split(",", cz[0])[0] if "," in cz[0] else re.split(" ", cz[0])[0]
            cz2 = re.split(",", cz[1])[0] if "," in cz[1] else re.split(" ", cz[1])[0]
        cz = str(cz[0] if len(cz) == 1 else " - ".join([cz1, cz2]))

        # Updating data
        tournament["players"][player]["command_zone"] = cz

        # Add to field
        if cz not in temp.keys():
            temp[cz] = {"quantity": 0}
        temp[cz]["quantity"] += 1

    # Step 1.B : Get Metagame by Quantity
    tmpr = {}
    for cz in temp:
        if temp[cz]["quantity"] not in tmpr.keys():
            tmpr[temp[cz]["quantity"]] = []
        tmpr[temp[cz]["quantity"]].append(cz)

    tournament["field"] = dict(tmpr.items())

    with open(fOutput, "w+") as f:
        json.dump(tournament, f, indent=4, sort_keys=True)
