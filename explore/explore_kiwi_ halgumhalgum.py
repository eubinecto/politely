from pprint import pprint

from politely.fetchers import fetch_kiwi

kiwi = fetch_kiwi()


pprint(list(kiwi.tokenize("할금할금 쳐다보더니")))
pprint(list(kiwi.tokenize("뒤뚱뒤뚱 걸어가다")))
pprint(kiwi.join(kiwi.tokenize("별로 우스울 것도 없는데 웃더라"), lm_search=True))
