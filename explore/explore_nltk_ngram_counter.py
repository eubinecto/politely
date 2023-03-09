from gensim.models.word2vec import Text8Corpus
from gensim.test.utils import datapath
from nltk.util import ngrams
from nltk.lm import NgramCounter
sentences = Text8Corpus(datapath('testcorpus.txt'))
# Each sentence must be a list of string tokens:
sentences = (
    ngrams(sent, n=2)
    for sent in sentences
)
counter = NgramCounter(sentences)

# NgramModel 클래스가 따로 있지는 않음. 이건 직접 구현해야하는 부분이다.
# 뭐.... 어쩌겠나! 하라면 해야지 허허.