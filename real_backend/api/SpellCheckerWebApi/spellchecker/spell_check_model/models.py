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
from IPython.display import display
from collections import Counter
import os

import pandas as pd
import nltk
import re
import codecs
import urllib
import string

nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('words')
nltk.download('wordnet')


def generate_pos_tags(tokens):
    return list(map(list, zip(*nltk.pos_tag(tokens))))


print("Initializing NLP required dataset...")
brown_lc_words = [wd.lower() for wd in brown.words()]
WORDS = set(brown_lc_words)
brown_pos = generate_pos_tags(brown_lc_words)
brown_bg = list(bigrams(brown_pos[0]))
brown_tg = list(trigrams(brown_pos[0]))
brown_bg_pos = list(bigrams(brown_pos[1]))
brown_tg_pos = list(trigrams(brown_pos[1]))
# Frequency distribution for Words
freq_dist = nltk.FreqDist(brown_lc_words)
freq_dist_bigrams = nltk.FreqDist(list(bigrams(brown_lc_words)))
freq_dist_trigrams = nltk.FreqDist(list(trigrams(brown_lc_words)))
# Frequency distribution for POS tags
freq_dist_pos = nltk.FreqDist(brown_pos[1])
freq_dist_bg_pos = nltk.FreqDist(brown_bg_pos)
freq_dist_tg_pos = nltk.FreqDist(brown_tg_pos)
correct_spellings = words.words()
total_len = len(brown_lc_words)

tagged_sentence = list(nltk.corpus.brown.tagged_sents())
tagged_words = [word for sentence in tagged_sentence for word in sentence]
tagSets = {word[1] for sentence in tagged_sentence for word in sentence}

print(os.listdir())
transMatrix = pd.read_pickle('transMatrix.pkl')
taggedArray = {}
biTaggedArray = {}
biTagArray = {}
biTags = []
biTaggedWords = []

for i in range(0,len(tagged_words)-1,1):
    biTags.append([tagged_words[i][1],tagged_words[i+1][1]])
    biTaggedWords.append([tagged_words[i][0],tagged_words[i+1][0]])

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


def open_file_or_url(path):
    if re.match(r'https?://', path):
        return urllib.request.urlopen(path)
    else:
        # Paralleling what urlopen does, we are going to open a bytestream (not a decoded string stream)
        # and read and decode it separately.
        return open(path, 'rb')


def process_line(line, error_cts, lct):
    line = line.strip()
    if line:
        (err, ct) = line.split('\t')
        (tgt, src) = err.split('|')
        if tgt and src:
            error_cts[tgt, src] = int(ct)
        elif tgt:
            error_cts[tgt, '#'] = int(ct)
        elif src:
            error_cts['#', src] = int(ct)
        else:
            print(f'***Warning*** Bad line {lct}: {line}')


def make_err_dict(path, encoding='latin1', errors='strict', linesep=r'\n'):
    """
    To get past some funky unicode characters, do errors = 'ignore'

    This will lose the troublesome characters; it  will not perform a reasonable
    approximation, such as "e"  for "e with an accent mark".
    """
    global error_cts
    error_cts = dict()
    with open_file_or_url(path) as handle:
        bytesdata = handle.read()
        data = codecs.decode(bytesdata, encoding=encoding, errors=errors)
    for (lct, line) in enumerate(re.split(linesep, data)):
        process_line(line, error_cts, lct)
    return error_cts


# Error data on Peter Norvig's website
url = 'https://norvig.com/ngrams/count_1edit.txt'
err_dict = make_err_dict(url)
print("Initialization complete...")


def get_letter_counts(path, encoding='latin1', linesep=r'\n', errors='strict'):
    """
    Build a single nltk.FreqDist instance with counts of both unigraphs
    and bigraphs for the words in `data_file`.
    """
    global line
    letters = []
    with open_file_or_url(path) as handle:
        bytesdata = handle.read()
        data = codecs.decode(bytesdata, encoding=encoding, errors=errors)
    for (lct, line) in enumerate(re.split(linesep, data)):
        line = line.strip()
        if line:
            # print(line)
            (right, wrong) = line.split(":")
            letters.append(right)
            letters.extend(ww.strip() for ww in wrong.split(","))
    # One big long string of letters with spaces separating words
    letters = ' '.join(letters)
    fd = nltk.FreqDist(letters)
    blts = list(nltk.bigrams(letters))
    fd.update(blts)
    return (fd, letters)

url = 'https://norvig.com/ngrams/spell-errors.txt'
letter_freqs, letters = get_letter_counts(url)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known(edits1(word)) or [word])


def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    keys = [w for w in words]
    for w in keys:
        if w not in WORDS:
            del words[w]
    return words


def edits1(word):
    operations = {}
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    #deletes = []
    for L, R in splits:
        if R:
            operations[L + R[1:]] = ((R[0], R[:2]), 'deletes')
            #deletes.append(L + R[1:])
    #transposes = []
    for L, R in splits:
        if len(R) > 1:
            operations[L + R[1] + R[0] + R[2:]] = ((R[1], R[0]), 'transposes')
            #transposes.append(L + R[1] + R[0] + R[2:])
    #replaces = []
    for L, R in splits:
        for c in letters:
            if R:
                # operations[L + c + R[1:]] = c + '|' + R[0]
                operations[L + c + R[1:]] = ((c, R[0]), 'replaces')
                #replaces.append(L + c + R[1:])
    #inserts = []
    for L, R in splits:
        for c in letters:
            operations[L + c + R] = ((c + R[0], R[0]), 'inserts') if R else ((L[-1] + c, L[-1]), 'inserts')
            #inserts.append(L + c + R)
    #inserts = [L + c + R for L, R in splits for c in letters]
    return operations


def get_candidates(w):
    #print(letter_freqs)
    candidate_set = {}
    for c, o in candidates(w).items():
        oper = o[1]
        oper_s = o[0]
        if oper_s[0] == oper_s[1]:
            candidate_set[c] = 0.95
        else:
            if oper_s in err_dict:
                if oper == 'deletes':
                    candidate_set[c] = err_dict[oper_s]/letter_freqs[oper_s[1][0], oper_s[1][1]]
                elif oper == 'inserts':
                    candidate_set[c] = err_dict[oper_s]/letter_freqs[oper_s[0][0]]
                elif oper == 'replaces':
                    candidate_set[c] = err_dict[oper_s]/letter_freqs[oper_s[0]]
                elif oper == 'transposes':
                    candidate_set[c] = err_dict[oper_s]/letter_freqs[oper_s]
    return candidate_set


def normalize(d, target=1.0):
    raw = sum(d.values())
    factor = target / raw
    return {key: value * factor for key, value in d.items()}


def normalize1(d, target=1.0):
    raw = sum([v[1] for v in d])
    factor = target/raw
    return [(kv[0], kv[1]*factor) for kv in d]


def is_contains_mispelled(input_text):
    entries = word_tokenize(input_text.lower().translate(str.maketrans('', '', string.punctuation)))
    print(entries)
    for entry in entries:
        print(entry)
        if entry not in brown_lc_words:
            return True
    return False


def non_word_spelling_check(input_text, max_dist=5, min_word=10):
    entries = word_tokenize(input_text)
    bigrams_ = list(bigrams(entries))
    suggestions = {}
    for position, entry in enumerate(entries):
        entry = entry.lower()
        if entry not in correct_spellings:
            temp_edit = [(edit_distance(entry, w), w) for w in correct_spellings if w[0] == entry[0]]
            i = 2
            edit_set = [x for x in temp_edit if x[0] <= i]
            while len(edit_set) < min_word & i < max_dist:
                i = i + 1
                edit_set = [x for x in temp_edit if x[0] <= i]
            freqs_1 = {}
            if(len(edit_set)==0):
                suggestions[position] = {}
            else:
                for word in edit_set:
                    if word[1] in freq_dist:
                        freqs_1[word[1]] = freq_dist[word[1]] / total_len
                entry_bigrams = [x for x in bigrams_ if (entry in x)]
                candidate_bigrams = {}
                # create bigrams candidate set
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
                            freqs_2[candidate] = freqs_2[candidate] + freq_dist_bigrams[cbigram] / freq_dist[cbigram[0]]
                if len(freqs_2) > 0:  # if exists bigrams then return the candidate with highest probability
                    suggestions[position] = [a[0] for a in sorted(freqs_2.items(), key=itemgetter(1), reverse=True)]
                elif len(freqs_1) > 0:
                    suggestions[position] = [a[0] for a in sorted(freqs_1.items(), key=itemgetter(1), reverse=True)]
    return suggestions


def real_word_spelling_check(input_text):
    print(input_text)
    upper_threshold = 0.9
    lower_threshold = 0.1
    lambda_ = 1.01
    #input_text = "the computer has
    # not been able to star up"
    entries = word_tokenize(input_text.lower())
    # entries = re.findall(r"[a-z]+", input_text.lower())
    trigrams_ = list(trigrams(entries))
    suggestions = {}
    # for position, entry in enumerate(entries):
    for tp, tg in enumerate(trigrams_):
        # if ',' in tg or '.' in tg or '!' in tg or '"' in tg:
        #    break
        for i, e in enumerate(tg):
            if e == ',' or e == '.' or e == '!' or e == '"':
                continue
            probs = {}
            candidate_set = get_candidates(e)
            x = list(tg)
            # print(candidate_set)
            for c, prob_channel in candidate_set.items():
                probc = prob_channel
                y = x
                y[i] = c
                # print(x)
                bgs = list(bigrams(x))
                for bg in bgs:
                    if freq_dist_bigrams[bg] > 0:
                        # print(bg)
                        # probs[c] = probs[c] * (freq_dist_bigrams[bg]/freq_dist[bg[0]])
                        probc = probc * (freq_dist_bigrams[bg] / freq_dist[bg[0]])
                    elif freq_dist_bigrams[bg] == 0:
                        if freq_dist[bg[0]] == 0:
                            bg0_freq = 0.000001
                        else:
                            bg0_freq = freq_dist[bg[0]]
                        if freq_dist[bg[1]] == 0:
                            bg1_freq = 0.000001
                        else:
                            bg1_freq = freq_dist[bg[1]]
                        # probs[c] = probs[c]  * bg0_freq/total_len * bg1_freq/total_len
                        probc = probc * bg0_freq / total_len * bg1_freq / total_len
                if c not in probs:
                    probs[c] = probc
                elif probc > probs[c]:
                    # print(c)
                    # print(probs)
                    probs[c] = probc
            # probs = sorted(normalize(probs).items(), key=itemgetter(1), reverse=True)
            # probs = normalize(probs)
            if tp + i not in suggestions:
                suggestions[tp + i] = probs
            else:
                for c, p in probs.items():
                    if c == e:  # if the word is the original
                        p = lambda_ * p
                    if c in suggestions[tp + i]:
                        if p > suggestions[tp + i][c]:
                            suggestions[tp + i][c] = p
                    else:
                        suggestions[tp + i][c] = p
    suggestions_final = {}
    #print(suggestions)
    for k, c in suggestions.items():
        c = sorted(normalize(c).items(), key=itemgetter(1), reverse=True)
        #print(c)
        for cc, p in c:
            if len(cc) == 1:
                if cc != 'a' and cc != 'i':
                    continue
            if p >= upper_threshold:
                if cc != entries[k]:  # if not the same as entry
                    suggestions_final[k] = [(cc, p)]
                    # suggestions_final[k] = [cc]
                break
            else:
                if k not in suggestions_final:
                    suggestions_final[k] = []
                if p > lower_threshold:
                    suggestions_final[k].append((cc, p))
                    # suggestions_final[k].append(cc)
    # print(suggestions_final)
    keys = [k for k, c in suggestions_final.items()]
    for k in keys:
        suggestions_final[k] = normalize1(suggestions_final[k])
        if suggestions_final[k][0][0] == entries[k] and suggestions_final[k][0][
            1] > 0.5:  # if the highest probability word is the same as the entry
            del suggestions_final[k]
        else:
            suggestions_final[k] = [kv[0] for kv in suggestions_final[k]]  # extract just the candidates
    return suggestions_final

def emissionCount(word,tag):
    #Scan through the Tag Array to find the occurrence of word
    countWord = [w for w in taggedArray[tag] if w == word] 
    return(len(countWord))

def viterbiProb(words):
    prevStateProb = {} #Set to store previous Probability States
    errorWord = 0
    for i in range(0,len(words),1):
        currentStateProb = {} #Set to store current Probability States
        for tag1 in tagSets:
            prob = 0
            if i == 0:
                transitionProb = transMatrix.loc['.',tag1] #The 1st word of sentence will be based on '.' transtition
                emissionProb = emissionCount(words[i],tag1)/len(biTagArray[tag1])
                #Multiplying constant to ensure probability is not too small to cause precision error
                prob = transitionProb * emissionProb * 100000 
            else:
                probMatrix = []
                prob = 0
                emissionProb = emissionCount(words[i],tag1)/len(biTagArray[tag1])
                if emissionProb != 0:
                    for tag2 in tagSets: #Loop through all available tags to find transition probability
                        transitionProb = transMatrix.loc[tag2,tag1]
                        #the probability for current state is also depends on the sequence probability of previous tag
                        probMatrix.append(transitionProb * emissionProb * prevStateProb[tag2] * 100000 )
                    #We will pick the maximum probability of Many Tag2 -> Single Tag1, as future sequence bear lower probability
                    prob = max(probMatrix)
            #Store the probability for next sequence computation
            currentStateProb[tag1] = prob
        #If somehow the probability drop to 0, return the errorWord
        if(max(currentStateProb.values())==0):
            errorWord = i
            return(0,errorWord)
        prevStateProb = currentStateProb
    #Pick the maximum probability of all tags combination, a Non-Zero indicate grammatically correct sentence
    return(max(prevStateProb.values()),errorWord)

def spellCheck(sentence):
    if is_contains_mispelled(sentence):
        response = non_word_spelling_check(sentence)
        if(len(response) == 1):
            for correctionIndex in response:
                updatedCandidates = []
                for candidates in response[correctionIndex]:
                    correctionSentence = word_tokenize(sentence)
                    correctionSentence[correctionIndex] = candidates
                    if(viterbiProb(correctionSentence) != 0):
                        updatedCandidates.append(candidates)
                response[correctionIndex] = updatedCandidates
            print('Return using Viterbi Non Word')
            return response
        else:
            print('Return using Non-Word Look Up')
            return response
    else:
        response = real_word_spelling_check(sentence)
        if(len(response) == 0):
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
                
                temp_cand = [(edit_distance(errorWord,w),w) for w in viterbiCandidate]
                i = 2
                min_word =10
                max_dist = 5
                cand_set = [x for x in temp_cand if x[0] <= i]
                while len(cand_set) < min_word & i < max_dist:
                    i = i + 1
                    cand_set = [x for x in temp_cand if x[0] <= i]
                finalCandidate[errorIndex] =cand_set
                print('Return using Viterbi Prob')
                return finalCandidate
            else:
                return None
        else:
            print('Return using Noisy Channel')
            return response