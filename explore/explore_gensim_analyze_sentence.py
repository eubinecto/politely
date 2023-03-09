from gensim.test.utils import datapath
from gensim.models.word2vec import Text8Corpus
from gensim.models.phrases import Phrases

# Create training corpus. Must be a sequence of sentences (e.g. an iterable or a generator).
sentences = Text8Corpus(datapath('testcorpus.txt'))
# Each sentence must be a list of string tokens:
first_sentence = next(iter(sentences))
print(first_sentence[:10])

# Train a toy phrase model on our training corpus.
phrase_model = Phrases(sentences, min_count=1, threshold=1)

# Apply the trained phrases model to a new, unseen sentence.
new_sentence = "how are you".split()
for elem in phrase_model.analyze_sentence(new_sentence):
    print(elem)
