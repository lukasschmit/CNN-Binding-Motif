
from random import randint
import csv

caseLength = 350
caseCount = 30000 # divisible by 24
chromosomeCount = 24

chromosomeChar = range(1, 23)
chromosomeChar.append('X')
chromosomeChar.append('Y')

allRandom = []

for c in chromosomeChar:
    c = str(c)
    chromFile = open("humanGenome/chr" + c + ".fa", "r")

    sequence = ""

    for line in chromFile:
        # skip headers
        if '>' is line[0]:
            continue

        # Add nucleotides
        line = line.upper()
        for n in line:
            if n in ['A', 'T', 'C', 'G']:
                sequence += n

    for i in range(0, caseCount / chromosomeCount):
        start = randint(0, len(sequence) - caseLength)
        piece = sequence[start:start + caseLength]
        allRandom.append(piece)

    print("Finished chromosome " + c)

print("done parsing")

with open("./RandomData/random.csv",'wb') as file:
    csvwriter = csv.writer(file)
    for sequence in allRandom:
        csvwriter.writerow([sequence])
