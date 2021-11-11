import csv
import sys
import random

    # Ensure correct usage
if len(sys.argv) != 2:
    sys.exit("Usage: python tournament.py FILENAME")

teams = []
# TODO: Read teams into memory from file
f = sys.argv[1]
with open (f, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        team = row
        team["rating"] = int(team["rating"])
        teams.append(team)
print(teams[0]["rating"])
