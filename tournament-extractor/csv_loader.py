import csv
import json
import re


def getCSV(fOutput):
    temp = {"date": "", "aetherhub": "", "name": "", "players": {}}
    file = input("Which tournament would you like to parse?\n")

    # Interpret data from filename
    data = re.split("/", file)[-1][:-4]
    temp["date"] = data[: data.find(" ")]
    temp["aetherhub"] = data[-5:]
    temp["name"] = data[
        len(temp["date"]) + 1 : len(data) - (len(temp["aetherhub"]) + 1)
    ]

    # Open CSV and compute
    with open(file, newline="") as f:
        raw_data = csv.reader(f, delimiter=",")
        for row in raw_data:
            temp["players"][row[0]] = {
                "name": row[0],
                "moxfield": row[1],
                "hashcode": row[2],
                "opponents": [],
                "rounds": [],
                "command_zone": [],
                "deck": [],
            }

    with open(fOutput, "w+") as f:
        json.dump(temp, f, indent=4)

    return data
