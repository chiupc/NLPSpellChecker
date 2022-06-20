from nltk.metrics.distance import edit_distance
from nltk.corpus import words
from nltk.util import ngrams
from nltk.util import trigrams
from nltk.util import bigrams
from operator import itemgetter
from nltk.corpus import brown
from nltk.util import trigrams
from nltk.util import bigrams
from nltk.tokenize import word_tokenize
from nltk.collocations import *
import nltk
import re

nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('words')
nltk.download('wordnet')


def generate_pos_tags(tokens):
    return list(map(list, zip(*nltk.pos_tag(tokens))))

print("Initializing NLP required dataset...")
brown_pos = generate_pos_tags(brown.words())
brown_bg = list(bigrams(brown_pos[0]))
brown_tg = list(trigrams(brown_pos[0]))
brown_bg_pos = list(bigrams(brown_pos[1]))
brown_tg_pos = list(trigrams(brown_pos[1]))
#Frequency distribution for Words
freq_dist = nltk.FreqDist(brown.words())
freq_dist_bigrams = nltk.FreqDist(list(bigrams(brown.words())))
freq_dist_trigrams = nltk.FreqDist(list(trigrams(brown.words())))
#Frequency distribution for POS tags
freq_dist_pos = nltk.FreqDist(brown_pos[1])
freq_dist_bg_pos = nltk.FreqDist(brown_bg_pos)
freq_dist_tg_pos = nltk.FreqDist(brown_tg_pos)
correct_spellings = words.words()
total_len = len(brown.words())
print("Initialization complete...")

ind = {}
letters = 'abcdefghijklmnopqrstuvwxyz'
for word in words.words():
    if word[0].lower() not in ind:
        ind[word[0].lower()] = set()
    ind[word[0].lower()].add(word)
for letter in letters:
    if letter not in ind:
        ind[letter] = set()


def non_word_spelling_check(input_text, max_dist=5, min_word=10):
    entries = word_tokenize(input_text)
    bigrams_ = list(bigrams(entries))
    suggestions = {}
    for position, entry in enumerate(entries):
        entry = entry.lower()
        if entry not in correct_spellings:
            temp_edit = [(edit_distance(entry, w),w) for w in correct_spellings if w[0]==entry[0]]
            i = 2
            edit_set = [x for x in temp_edit if x[0] <= i]
            while len(edit_set) < min_word & i < max_dist:
                i = i + 1
                edit_set = [x for x in temp_edit if x[0] <= i]
            freqs_1 = {}
            for word in edit_set:
                if word[1] in freq_dist:
                    freqs_1[word[1]] = freq_dist[word[1]]/total_len
            entry_bigrams = [x for x in bigrams_ if (entry in x)]
            candidate_bigrams = {}
            #create bigrams candidate set
            for correction in edit_set:
                for pos_, x in enumerate(entry_bigrams):
                    if ',' in x or '.' in x or '!' in x or '"' in x:
                        break
                    for j in range(len(x)):
                        if x[j] == entry:
                            y = list(x)
                            y[j] = correction[1]
                            x = tuple(y)
                    if correction[1] not in candidate_bigrams:
                        candidate_bigrams[correction[1]] = list()
                    candidate_bigrams[correction[1]].append(x)
            freqs_2 = {}
            for candidate, cbigrams in candidate_bigrams.items():
                for cbigram in cbigrams:
                    if cbigram in freq_dist_bigrams:
                        if candidate not in freqs_2:
                            freqs_2[candidate] = 0
                        freqs_2[candidate] = freqs_2[candidate] + freq_dist_bigrams[cbigram]/freq_dist[cbigram[0]]
            if len(freqs_2) > 0: #if exists bigrams then return the candidate with highest probability
                suggestions[position] = [a[0] for a in sorted(freqs_2.items(), key=itemgetter(1), reverse=True)]
            elif len(freqs_1) > 0:
                suggestions[position] = [a[0] for a in sorted(freqs_1.items(), key=itemgetter(1), reverse=True)]
    return suggestions


