import nltk
nltk.download('words')
nltk.download('punkt')
from nltk.corpus import words
from nltk.tokenize import word_tokenize

#Lets use words Corpus for spellCheck
spellCheckDictionary = words.words()

def tokenizeSentence(inputSentence):
    return word_tokenize(inputSentence)

def spellCheck(inputString):
    porterStem = nltk.PorterStemmer()
    lancasterStem = nltk.LancasterStemmer()

    porterString = porterStem.stem(inputString)
    lancasterString = lancasterStem.stem(inputString)
    #Check using if the word stem by both Porter/Lancaster is valid
    for word in spellCheckDictionary:
        if ((word == porterString) | (word == lancasterString)):
            return 1
    return 0

