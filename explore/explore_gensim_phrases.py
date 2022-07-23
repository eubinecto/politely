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
new_sentence = ['trees', 'graph', 'minors']
print(phrase_model[new_sentence])
# The toy model considered "trees graph" a single phrase => joined the two
# tokens into a single "phrase" token, using our selected `_` delimiter.

# Update the model with two new sentences on the fly.
phrase_model.add_vocab([["hello", "world"], ["meow"]])
for entry in phrase_model.analyze_sentence(["hello", "how", "are", "you", "?"]):
    print(entry)