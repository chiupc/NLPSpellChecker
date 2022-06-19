from spellChecker import *
actualSentence = "The quick brown fox jumps over the lazy dog"
testSentence = "The quick borwn fxo jumps over the laziness dog"

tokenizedSentence = tokenizeSentence(testSentence)
print(tokenizedSentence)
print([spellCheck(word) for word in tokenizedSentence])
