"""
You may want to replace konlpy with  kiwi, if it helps.
well, we will think about doing this later on. Just not now.

"""
from kiwipiepy import Kiwi


kiwi = Kiwi()
kiwi.add_user_word("해")
print(kiwi.tokenize("한국의 목욕탕에서는 옷을 벗어"))
print(kiwi.tokenize("알겠읍니다"))
