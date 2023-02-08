import csv
import json
import os
import re

from aetherhub import extract as aet_extract
from csv_loader import getCSV as csv_import
from moxfield import extract as mox_extract

fInput = "tournament-extractor/temp.json"

if __name__ == "__main__":
    name = csv_import(fInput)
    mox_extract(fInput, fInput)
    aet_extract(fInput, f"{fInput[:-9]}{name}.json")
    os.remove(fInput)
