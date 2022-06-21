import nltk

from nltk.corpus import brown
from nltk.util import ngrams

words = []
tagged_sentence = list(nltk.corpus.brown.tagged_sents())

tagged_words = [word for sentence in tagged_sentence for word in sentence]

tagSets = {word[1] for sentence in tagged_sentence for word in sentence}

biTags = []
biTaggedWords = []

for i in range(0,len(tagged_words)-1,1):
    biTags.append([tagged_words[i][1],tagged_words[i+1][1]])
    biTaggedWords.append([tagged_words[i][0],tagged_words[i+1][0]])

for w in brown.words():
    words.append(w.lower())

biWords= list(ngrams(words,2))
triWords = list(ngrams(words,3))

freqMat = nltk.FreqDist(words)
biFreq = nltk.FreqDist(biWords)
triFreq = nltk.FreqDist(triWords)

#Lets use words Corpus for spellCheck
alphabets = list("abcdefghijklmnopqrstuvwxyz")
wordArray ={}
biArray = {}
triArray = {}
taggedArray = {}
biTaggedArray = {}
biTagArray = {}

for tag in tagSets:
    taggedArray[tag] = set()
    biTagArray[tag] = []

for w in tagged_words:
    taggedArray[w[1]].add(w[0])
    biTaggedArray[w[0][0]] = []

for biTag in biTags:
    array = biTagArray[biTag[0]]
    array.append(biTag)
    biTagArray[biTag[0]] = array

for biTagWord in biTaggedWords:
    array = biTaggedArray[biTagWord[0][0]]
    array.append(biTagWord)
    biTaggedArray[biTagWord[0][0]] = array

for char in alphabets:
    wordArray[char] = set()
    biArray[char] = set()
    triArray[char] = set()

for w in words:
    if(w.isalpha()):
        wordArray[w[0]].add(w)

for w in biWords:
    if(w[0].isalpha()):
        biArray[w[0][0]].add(w)

for w in triWords:
    if(w[0].isalpha()):
        triArray[w[0][0]].add(w)