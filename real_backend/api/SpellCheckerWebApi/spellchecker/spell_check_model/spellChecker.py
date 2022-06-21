from words import *
from nltk.tokenize import word_tokenize

from minDistance import *
def tokenizeSentence(inputSentence):
    return word_tokenize(inputSentence)

def spellCheck(inputString):
    porterStem = nltk.PorterStemmer()
    lancasterStem = nltk.LancasterStemmer()

    porterString = porterStem.stem(inputString)
    lancasterString = lancasterStem.stem(inputString)
    #Check using if the word stem by both Porter/Lancaster is valid
    for word in wordArray[inputString[0].lower()]:
        if ((word == porterString) | (word == lancasterString) | (word == inputString)):
            return 1
    return 0

def suggestCorrection(inputString):
    stringLength = len(inputString)
    correctionArray=[]
    for word in wordArray[inputString[0].lower()]:
        if (freqMat[word] != 0 and ((len(word) > (stringLength-2)) and (len(word) < (stringLength+2)))):
            (distMatrix,distance) = minDistance(word,inputString)
            correctionArray.append([word,distance,freqMat[word], distance*freqMat[word]])
    return correctionArray