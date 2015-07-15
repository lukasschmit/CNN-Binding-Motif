# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:13:58 2015

@author: jod30
"""

import os, pickle, csv

# This folder has all the MAFK peaks separated into pickle files,
# one for each chromosome
peakFiles = os.listdir("../Datafiles/allMAFKpeaks")

MAFKpeaks30000_350bp = {}
countPeaks = 0
# Collect 30,000 MAFK peaks of length 350 bp 
for filename in peakFiles:
    if countPeaks < 30000:
        # Pickle unpacks into a list of lists;
        # Each of element of secondary list is [<start>, <length>] of a peak
        peaks = pickle.load(open("../Datafiles/allMAFKpeaks/"+filename, 'rb'))
        # Get chromosome number - FASTA file you need will be <chrNum>.fa
        chrNum = filename.lstrip("AllMAFKpeaks_").rstrip(".p")

        snippedPeakStart = []
        for peak in peaks:
            if peak[1] < 350:
                pass
            elif peak[1] == 350:
                snippedPeakStart.append(peak[0])
            else:
                # Get the start position of central 350 bp of the peak
                newStart = peak[0] + int(peak[1]/2) - int(350/2)
                snippedPeakStart.append(newStart)
        countPeaks += len(snippedPeakStart)
        if countPeaks > 30000:
            reduceSnips = countPeaks - 30000
            lenSnips = len(snippedPeakStart)
            keepPeaks = snippedPeakStart[0:(lenSnips - reduceSnips)]
        else:
            keepPeaks = snippedPeakStart        
    #print str(countPeaks)
    MAFKpeaks30000_350bp[chrNum] = keepPeaks

## count if got 30,000 peaks
#final = 0
#for item in MAFKpeaks30000_350bp:
#    final += len(MAFKpeaks30000_350bp[item])
#print str(final)
    

# This function reads in all the lines in the fasta file and joins into one 
# sequence for the entire chromosome
def readSequenceFile(p_file):
   L_rets = ''
   ff = open(p_file,'r')
   count = 0
   L_stringList = []
   for ln in ff:
      count += 1
      if count>1:
         ln2 = ln.split('\n')
         L_stringList.append(ln2[0])

   L_rets = ''.join(L_stringList)
   ff.close()
   #print 'The length of the sequence is',len(L_rets)
   return L_rets

#create csv file of 30,000 peak sequences of length 350 bp
with open("MAFKpeakSequences.csv",'wb') as csvfile:
    sequences =  iter(csvfile)
    for chrNum in MAFKpeaks30000_350bp:
        fasta_seq = readSequenceFile('../chromFa/'+chrNum+'.fa')
        for startPos in MAFKpeaks30000_350bp[chrNum]:
            peakSequence = fasta_seq[startPos:startPos+350]
            sequences.writerow([peakSequence])