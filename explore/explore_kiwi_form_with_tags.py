"""
kiwi의 문제 = spacing이 사라져버린다... 음...s
이는 spacy와의 매우 큰 차이점이다. spacy는 띄어쓰기도 보존이 된다.
"""
import numpy as np
from kiwipiepy import Kiwi
from khaiii import KhaiiiApi


sent = "시끄럽게 코 고는 소리에 놀라서 난 잠이 깼다."
# --- Kiwipiepy로 띄어쓰기 및 원형 복구 --- #
kiwi = Kiwi()
tokens = kiwi.tokenize(sent)
for token in tokens:
    print(token.tagged_form)