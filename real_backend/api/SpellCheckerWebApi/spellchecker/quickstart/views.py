# Create your views here.
from nltk.corpus import brown
from rest_framework import status
# initialize nltk corpus download
from rest_framework.decorators import api_view
from rest_framework.response import Response
from spell_check_model.models import *
from spell_check_model.spellCheck import *
import re

#corpus = brown.words()
brown_words_non_punc = []
for word in brown.words():
    for w in re.findall(r"[a-z]+",word.lower()):
        brown_words_non_punc.append(w)

@api_view(['GET'])
def get_corpus_tokens(request):
    print(request.method)
    res = {"result" : list(set(brown_words_non_punc))}
    return Response(data=res, status=status.HTTP_200_OK)


@api_view(['POST'])
def spelling_check(request):
    input_text = request.data
    return Response(data=spellCheck(request.data["input_text"]), status=status.HTTP_200_OK)
