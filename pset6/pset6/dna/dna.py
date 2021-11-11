import sys
import csv

if len(sys.argv) != 3:
    print("Usage example: 'python dna.py databases/large.csv sequences/5.txt'")

with open(sys.argv[1], "r") as database:
    reader = csv.DictReader(database)
    dict_list = list(reader)
    STRs = reader.fieldnames[1:]

with open(sys.argv[2], "r") as sequence:
    text = csv.reader(sequence)
    for row in text:
        s = row
        s = str(s)

counts = []
for STR in STRs:
    count = 0
    pattern = STR
    while pattern in s:
        count += 1
        pattern += STR
    counts.append(count)

for i in range(len(dict_list)):
    matches = 0
    for j in range(1, len(reader.fieldnames)):
        if int(counts[j - 1]) == int(dict_list[i][reader.fieldnames[j]]):
            matches += 1
        if matches == (len(reader.fieldnames) - 1):
            print(dict_list[i]['name'])
            exit(0)
print("No match")