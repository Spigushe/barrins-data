import json
import math
import os
import re

from data_loop import basic_info, normalize, tiers
from field import get_field

fInput = "tournament-analyzer/temp.json"

if __name__ == "__main__":
    file = input("Which tournament would you like to parse?\n")
    get_field(file, fInput)
    basic_info(fInput, fInput)
    normalize(fInput, fInput)
    tiers(fInput, f"{fInput[:-9]}{re.split('/',file)[-1][:-11]}.json")
    os.remove(fInput)
