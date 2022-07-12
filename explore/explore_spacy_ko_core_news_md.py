"""
Korean models are now available.
https://spacy.io/models/ko#ko_core_news_md
It has been available since April 2022.
"""
import spacy

nlp = spacy.load("ko_core_news_md")

for token in nlp("아버지가 방에 들어가신다."):
    print(token.text, token.lemma_, token.pos_, token.tag_)

# but well, I think kiwi is far more accruate than that.
