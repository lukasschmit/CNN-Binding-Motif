
import csv
import cPickle
import gzip
import numpy as np

trainSize = 40000
validSize = 10000
testSize = 10000

# 60000 high, 350x4 wide
features = np.zeros((60000, 350 * 4), dtype="float32")
labels = np.zeros(60000, dtype=int)
binDict = {'A': 0, 'T': 1, 'C': 2, 'G': 3}

index = 0

# Random cases
with open("./RandomData/random.csv", 'rb') as file:
    reader = csv.reader(file)
    for row in reader:
        seq = row[0].upper()
        for i in range(0, 350):
            # column major
            #
            # 0 1 0 0 0 0 1 0 0 0 1 0
            # 1 0 0 0 1 0 0 0 0 1 0 0
            # 0 0 0 1 0 1 0 0 1 0 0 0
            # 0 0 1 0 0 0 0 1 0 0 0 1

            features[index, i * 4 + binDict[seq[i]]] = 1.0
        labels[index] = 0
        index += 1

print("Finished " + str(index) + " random")

# Correct cases
with open("./PeakData/MAFKpeakSequences.csv", 'rb') as file:
    reader = csv.reader(file)
    for row in reader:
        seq = row[0].upper()
        for i in range(0, 350):
            features[index, i * 4 + binDict[seq[i]]] = 1.0
        labels[index] = 1
        index += 1

print("Converted " + str(index) + " peaks to binary.")

halfTrain = trainSize / 2
halfTest = testSize / 2

validStart1 = halfTrain
validStart2 = 30000 + halfTrain

testStart1 = 30000 - halfTest
testStart2 = 60000 - halfTest

# Write training set
with gzip.open("./training/BinaryData/training.pkl.gz", 'wb') as file:
    trainingFeat = np.concatenate((features[:validStart1], features[30000:validStart2]), axis=0)
    trainingLab = np.concatenate((labels[:validStart1], labels[30000:validStart2]), axis=0)
    cPickle.dump((trainingFeat, trainingLab), file)

print("Wrote training set")

# Write validation set
with gzip.open("./training/BinaryData/validation.pkl.gz", 'wb') as file:
    validFeat = np.concatenate((features[validStart1:testStart1], features[validStart2:testStart2]), axis=0)
    validLab = np.concatenate((labels[validStart1:testStart1], labels[validStart2:testStart2]), axis=0)
    cPickle.dump((validFeat, validLab), file)

print("Wrote validation set")

# Write test set
with gzip.open("./training/BinaryData/test.pkl.gz", 'wb') as file:
    testFeat = np.concatenate((features[testStart1:30000], features[testStart2:]), axis=0)
    testLab = np.concatenate((labels[testStart1:30000], labels[testStart2:]), axis=0)
    cPickle.dump((testFeat, testLab), file)

print("Wrote test set")
