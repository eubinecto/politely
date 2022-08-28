"""
Train a Word2Vec model from the StyleKQC dataset.
"""
import os
import yaml
from gensim.models.callbacks import CallbackAny2Vec
from datasets import load_dataset
from gensim.models import Word2Vec
from tqdm import tqdm
from politely.fetchers import fetch_kiwi
import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s -  %(message)s", level=logging.INFO)


class LossCallback(CallbackAny2Vec):
    """
    Just for reporting the progress.
    """
    def __init__(self):
        self.epoch = 0
        self.before = 0

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        print('Loss for the epoch {}: {}'.format(self.epoch, loss - self.before))
        self.before = loss
        self.epoch += 1


# --- load the config --- #
with open("config.yaml", 'r') as fh:
    config = yaml.safe_load(fh)

# prepare the tokenizer and the dataset --- #
kiwi = fetch_kiwi()
dataset = load_dataset("wicho/stylekqc-style")
train = dataset['train']

# --- prepare the corpus --- #
sents = [sent for sent in train['formal']] + [sent for sent in train['informal']]
corpus = [
    [token.form for token in kiwi.tokenize(sent)]
    for sent in tqdm(sents)
]

# --- start training --- #
# yeah, we could log this with wandb, most certainly.
w2v = Word2Vec(corpus, callbacks=[LossCallback()], workers=os.cpu_count(), **config)
w2v.save("stylekqc.w2v")
