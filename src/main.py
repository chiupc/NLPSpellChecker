from spellChecker import *
from viterbiAlgorithm import *
import time

start = time.time()
actualSentence = "The quick brown fox jump over the lazy dog"
# testSentence = "The quick brrwn fxo jumps over rin the laziness dog"
testSentence =["I am running to bus stop","I am run to bus stop"]

# tokenizedSentence = tokenizeSentence(testSentence)

for sentence in testSentence:
    print(sentence)
    viterbiProb(tokenizeSentence(sentence))

end = time.time()
difference = end - start
print('Time taken in seconds:',difference)

# viterbiProb(tokenizeSentence(actualSentence))

# spellCheckMatrix=[]

# for word in tokenizedSentence:
#     item = []
#     if(spellCheck(word)):
#         item=[word,1]
#     else:
#         item=[word,0]
#     spellCheckMatrix.append(item)

# for items in spellCheckMatrix:
#     if(items[1]==0):
#         suggestionArray = suggestCorrection(items[0])

#         for suggest in suggestionArray:
#             if(suggest[1]<3):
#                 print(suggest)