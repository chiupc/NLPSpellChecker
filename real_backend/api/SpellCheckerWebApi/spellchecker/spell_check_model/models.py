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

ind = {}
letters = 'abcdefghijklmnopqrstuvwxyz'
for word in words.words():
    if word[0].lower() not in ind:
        ind[word[0].lower()] = set()
    ind[word[0].lower()].add(word)
for letter in letters:
    if letter not in ind:
        ind[letter] = set()


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