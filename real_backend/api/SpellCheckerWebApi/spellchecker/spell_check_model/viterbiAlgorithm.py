from words import *
import numpy
from IPython.display import display
import pandas as pd

initiateMatrix = False

if(initiateMatrix):
    tagMatrix = numpy.zeros((len(tagSets),len(tagSets)))

    enum = enumerate(list(tagSets))

    for i,tag1 in enumerate(list(tagSets)):
        for j,tag2 in enumerate(list(tagSets)):
            totalTag1 = len(biTagArray[tag1])
            totalTag2 =0
            for t in biTagArray[tag1]:
                if(t[1] == tag2):
                    totalTag2 +=1
            tagMatrix[i,j] = totalTag2/totalTag1

    transMatrix = pd.DataFrame(tagMatrix,columns=list(tagSets),index=list(tagSets))
    transMatrix.to_pickle('transMatrix.pkl')
else:
    transMatrix = pd.read_pickle('transMatrix.pkl')

def emissionCount(word,tag):
    countWord = [w for w in taggedArray[tag] if w == word]
    return(len(countWord))

def viterbiProb(words):
    global transMatrix
    prevStateProb = {}
    errorWord = 0
    for i in range(0,len(words),1):
        currentStateProb = {}
        for tag1 in tagSets:
            prob = 0
            if i == 0:
                transitionProb = transMatrix.loc['.',tag1]
                emissionProb = emissionCount(words[i],tag1)/len(biTagArray[tag1])
                prob = transitionProb * emissionProb * 100000
            else:
                probMatrix = []
                prob = 0
                emissionProb = emissionCount(words[i],tag1)/len(biTagArray[tag1])
                if emissionProb != 0:
                    for tag2 in tagSets:
                        transitionProb = transMatrix.loc[tag2,tag1]
                        probMatrix.append(transitionProb * emissionProb * prevStateProb[tag2] * 100000 )
                    prob = max(probMatrix)
            currentStateProb[tag1] = prob

        #If somehow the probability drop to 0, check if remaining words form sentence
        if(max(currentStateProb.values())==0):
            errorWord = i
            return(0,errorWord)
        prevStateProb = currentStateProb
    print('Max:',max(prevStateProb.values()))
    return(max(prevStateProb.values()),errorWord)