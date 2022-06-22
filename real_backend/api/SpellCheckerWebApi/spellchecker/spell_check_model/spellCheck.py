from viterbiAlgorithm import *
import time
from models import *
import re
from collections import Counter
actualSentence = "I am ran to bus"

testSentence =["I am run to bus","I am ran to bus"]

splitSentence = re.split('[\.\?\!]\s*',actualSentence)


def spellCheck(sentence):
    response = non_word_spelling_check(sentence)
    if(len(response) != 0):
        if(len(response) == 1):
            for correctionIndex in response:
                updatedCandidates = []
                for candidates in response[correctionIndex]:
                    correctionSentence = word_tokenize(sentence)
                    correctionSentence[correctionIndex] = candidates
                    if(viterbiProb(correctionSentence) != 0):
                        updatedCandidates.append(candidates)
                response[correctionIndex] = updatedCandidates
            
            return response
        else:
            return response
    else:
        tokenSentence = word_tokenize(sentence)
        (vitProb,errorIndex) = viterbiProb(tokenSentence)
        if(vitProb == 0):
            viterbiCandidate = set()
            finalCandidate = {}
            prevWord = tokenSentence[errorIndex-1]
            errorWord = tokenSentence[errorIndex]
            nextWord = tokenSentence[errorIndex+1]
            finalCandidate[errorIndex] = []
            #Find the words in tagged library to find its POS, then proceed to find POS of subsequent words, and find suitable candidate
            prevPOS_index = []
            nextPOS_index = []
            for w in tagged_words:
                if w[0] == prevWord:
                    prevPOS_index.append(w[1])
                if w[0] == nextWord:
                    nextPOS_index.append(w[1])
            prevPOS_Counter = Counter(prevPOS_index)
            nextPOS_Counter = Counter(nextPOS_index)
            prevPOS = max(prevPOS_Counter,key=prevPOS_Counter.get)
            nextPOS = max(nextPOS_Counter,key=nextPOS_Counter.get)
            mat_Trans = {}
            for t in tagSets:
                transP1 = transMatrix.loc[prevPOS,t]
                transP2 = transMatrix.loc[t,nextPOS]
                mat_Trans[t] = transP1*transP2
                nextTrans = max(mat_Trans,key=mat_Trans.get)

                for t_words in taggedArray[nextTrans]:
                    if t_words[0] == errorWord[0]:
                        viterbiCandidate.add(t_words)
            
            for cand in viterbiCandidate:
                distance = edit_distance(errorWord,cand)
                if distance < 5:
                    array = finalCandidate[errorIndex]
                    array.append([cand,distance])
                    finalCandidate[errorIndex] = array
            print(finalCandidate)
            return finalCandidate
        else:
            return None