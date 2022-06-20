# Create your views here.
from nltk.corpus import brown
from rest_framework import status
# initialize nltk corpus download
from rest_framework.decorators import api_view
from rest_framework.response import Response
from spell_check_model.models import *

corpus = brown.words()


@api_view(['GET'])
def get_corpus_tokens(request):
    print(request.method)
    res = {"result" : list(corpus)}
    return Response(data=res, status=status.HTTP_200_OK)


@api_view(['POST'])
def spelling_check(request):
    input_text = request.data
    return Response(data=non_word_spelling_check(request.data["input_text"]), status=status.HTTP_200_OK)
