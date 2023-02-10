import json
import math

"""
Loop will gather data:
    - (P) Presence
    - (M) Mirror Rounds
    - (N) Total Num of Rounds
    - (W) Total Wins (except from BYE)
    - (L) Total Losses
    - (D) Total Draws
"""


def basic_info(fInput, fOutput):
    with open(fInput, "r") as f:
        tournament = json.load(f)

    tournament["commanders"] = {}
    for player in tournament["players"]:
        cz = tournament["players"][player]["command_zone"]
        if (
            tournament["players"][player]["command_zone"]
            in tournament["commanders"].keys()
        ):
            # Adding to presence
            tournament["commanders"][cz]["presence"] += 1
        else:
            # Creating the fields
            tournament["commanders"][cz] = {
                "presence": 1,
                "mirror": 0,
                "total_rounds": 0,
                "total_wins": 0,
                "total_losses": 0,
                "total_draws": 0,
            }

        for round in tournament["players"][player]["rounds"]:
            # New round played
            tournament["commanders"][cz]["total_rounds"] += 1
            # Check if mirror
            opponent = str(round[2:])
            if cz == tournament["players"][opponent]["command_zone"]:
                tournament["commanders"][cz]["mirror"] += 1
            # Elseheck round result
            else:
                result = round[0]
                if opponent != "BYE":
                    if result == "W":
                        tournament["commanders"][cz]["total_wins"] += 1
                    elif result == "L":
                        tournament["commanders"][cz]["total_losses"] += 1
                    elif result == "D":
                        tournament["commanders"][cz]["total_draws"] += 1

    with open(fOutput, "w+") as f:
        json.dump(tournament, f, indent=4, sort_keys=True)


"""
Data to be computed:
    1st loop:
        - Winrate (W/(W+L))
        - Draw potential (D/(R-M))
    2nd loop:
        - (PS) Presence start at 0 (P-min(P))
        - (WS) Winrate start at 0 (W-min(W))
    3rd loop:
        - (PN) Presence normalized (PS/max(PS))
        - (WN) Winrate normalized (WS/max(WS))
        - (R) Rating ((PN+WN)*100)
    - (STDEV) Standard Deviation (R)
"""


def normalize(fInput, fOutput):
    with open(fInput, "r") as f:
        tournament = json.load(f)

    tmp = {}
    for commander in tournament["commanders"]:
        cz = tournament["commanders"][commander]
        # Presence
        # Min presence
        if "presence" not in tmp.keys():
            tmp["presence"] = cz["presence"]
        else:
            if cz["presence"] < tmp["presence"]:
                tmp["presence"] = cz["presence"]

        # Winrate
        cz["winrate"] = cz["total_wins"] / (cz["total_wins"] + cz["total_losses"])
        # Min winrate
        if "winrate" not in tmp.keys():
            tmp["winrate"] = cz["winrate"]
        else:
            if cz["winrate"] < tmp["winrate"]:
                tmp["winrate"] = cz["winrate"]

        # Draw potential
        cz["draw_potential"] = cz["total_draws"] / (cz["total_rounds"] - cz["mirror"])

    # Start at 0 computations
    for commander in tournament["commanders"]:
        cz = tournament["commanders"][commander]

        # Presence start at 0
        cz["presence_0"] = cz["presence"] - tmp["presence"]
        # Max presence start at 0
        if "presence_0" not in tmp.keys():
            tmp["presence_0"] = cz["presence_0"]
        else:
            if cz["presence_0"] > tmp["presence_0"]:
                tmp["presence_0"] = cz["presence_0"]

        # Winrate start at 0
        cz["winrate_0"] = cz["winrate"] - tmp["winrate"]
        # Max winrate start at 0
        if "winrate_0" not in tmp.keys():
            tmp["winrate_0"] = cz["winrate_0"]
        else:
            if cz["winrate_0"] > tmp["winrate_0"]:
                tmp["winrate_0"] = cz["winrate_0"]

    # Normalized computation
    for commander in tournament["commanders"]:
        cz = tournament["commanders"][commander]

        # Presence normalized
        cz["presence_n"] = cz["presence_0"] / tmp["presence_0"]

        # Winrate normalized
        cz["winrate_n"] = cz["winrate_0"] / tmp["winrate_0"]

        # Rating
        rating = (cz["presence_n"] + cz["winrate_n"]) * 100
        cz["rating"] = rating

    with open(fOutput, "w+") as f:
        json.dump(tournament, f, indent=4, sort_keys=True)


"""
Tiers calculus:
    - Tier 0   (avg(R)+3*STDEV)
    - Tier 0.5 (avg(R)+2*STDEV)
    - Tier 1   (avg(R)+1*STDEV)
    - Tier 1.5 (avg(R))
    - Tier 2   (avg(R)-1*STDEV)
    - Tier 2.5 (avg(R)-2*STDEV)
    - Tier 3   (avg(R)-3*STDEV)
"""


def tiers(fInput, fOutput):
    with open(fInput, "r") as f:
        tournament = json.load(f)

    # Variables
    (stdev, mean) = get_stdev(tournament)

    tournament["tiers"] = {
        "0": {"threshold": mean + 3 * stdev, "command_zone": []},
        "0.5": {"threshold": mean + 2 * stdev, "command_zone": []},
        "1": {"threshold": mean + 1 * stdev, "command_zone": []},
        "1.5": {"threshold": mean, "command_zone": []},
        "2": {"threshold": mean - 1 * stdev, "command_zone": []},
        "2.5": {"threshold": mean - 2 * stdev, "command_zone": []},
        "3": {"threshold": mean - 3 * stdev, "command_zone": []},
    }
    for commander in tournament["commanders"]:
        cz = tournament["commanders"][commander]
        rating = tournament["commanders"][commander]["rating"]
        tier_found = False
        for tier in tournament["tiers"]:
            if not tier_found:
                if rating > tournament["tiers"][tier]["threshold"]:
                    tournament["tiers"][tier]["command_zone"].append(commander)
                    cz["tier"] = tier
                    tier_found = True

    with open(fOutput, "w+") as f:
        json.dump(tournament, f, indent=4, sort_keys=True)


def get_stdev(tournament):
    tmp = {"rating": [], "sqdif": []}

    for commander in tournament["commanders"]:
        tmp["rating"].append(tournament["commanders"][commander]["rating"])
    tmp["mean"] = sum(tmp["rating"]) / len(tmp["rating"])
    for rate in tmp["rating"]:
        tmp["sqdif"].append((rate - tmp["mean"]) ** 2)
    tmp["avg_sqdif"] = sum(tmp["sqdif"]) / len(tmp["sqdif"])
    tmp["stdev"] = math.sqrt(tmp["avg_sqdif"])

    return (tmp["stdev"], tmp["mean"])
