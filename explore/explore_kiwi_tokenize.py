"""
You may want to replace konlpy with  kiwi, if it helps.
well, we will think about doing this later on. Just not now.

"""
from kiwipiepy import Kiwi


kiwi = Kiwi()
kiwi.add_user_word("해")
print(kiwi.tokenize("한국의 목욕탕에서는 옷을 벗어"))
print(kiwi.tokenize("그래 좋아요"))
print(kiwi.tokenize("알겠습니다"))
print(kiwi.tokenize("했습니다"))
print(kiwi.tokenize("제가 합니다"))
print(kiwi.tokenize("이렇게 하십시오"))
print(kiwi.tokenize("그렇게 해"))
print(kiwi.tokenize("잘 지내셨습니까?"))
print(kiwi.tokenize("그렇게 하지마요."))
print(kiwi.tokenize("그렇게 하지마세요."))
print(kiwi.tokenize("그렇게 하래요."))
print(kiwi.tokenize("나는 쓰레기를 주워."))
print(kiwi.tokenize("배고파요."))
print(kiwi.tokenize("잘했죠."))
print(kiwi.tokenize("진지 잡수세요."))
