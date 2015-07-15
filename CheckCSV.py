
import csv

with open("randomData/random.csv", 'r') as file:
    csvreader = csv.reader(file)
    c = 0
    for line in csvreader:
        print(len(line[0]))
        c += 1

    print(str(c) + " Samples")
