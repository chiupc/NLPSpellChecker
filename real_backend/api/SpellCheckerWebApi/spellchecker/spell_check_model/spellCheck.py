#from viterbiAlgorithm import *
from models import *

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
        #Real word correction
        return response
