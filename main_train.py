"""
Train a Word2Vec model from the StyleKQC dataset.
"""
import os

from gensim.models.callbacks import CallbackAny2Vec
from datasets import load_dataset
from gensim.models import Word2Vec
from tqdm import tqdm
from politely.fetchers import fetch_kiwi
import logging
logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)


class Callback(CallbackAny2Vec):
    """
    Callback to print loss after each epoch.
    This is just for... reporting the progress.
    """

    def __init__(self):
        self.epoch = 0
        self.loss_before = 0

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        print('Loss for the epoch {}: {}'.format(self.epoch, loss - self.loss_before))
        self.loss_before = loss
        self.epoch += 1


# prepare the tokenizer
kiwi = fetch_kiwi()
# prepare the dataset
dataset = load_dataset("wicho/stylekqc-style")
train = dataset['train']


# --- prepare the corpus (use streams) --- #
sents = [sent for sent in train['formal']] + [sent for sent in train['informal']]
corpus = [
    [token.form for token in kiwi.tokenize(sent)]
    for sent in tqdm(sents)
]


# --- start training --- #
# yeah, we could log this with wandb, most certainly.
w2v = Word2Vec(corpus, vector_size=300, sg=1, callbacks=[Callback()],
               alpha=0.025, min_alpha=0.0001, epochs=5000,
               compute_loss=True, window=5, min_count=1, workers=os.cpu_count())
w2v.save("stylekqc.w2v")