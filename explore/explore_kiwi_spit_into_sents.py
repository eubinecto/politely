"""
You may want to replace konlpy with  kiwi, if it helps.
well, we will think about doing this later on. Just not now.

"""
from kiwipiepy import Kiwi


kiwi = Kiwi()
kiwi.add_user_word("해")
print(kiwi.tokenize(text="나는 공부해"))
print(kiwi.tokenize(text="나는 공부해요"))
print(kiwi.tokenize(text="저기로 가요"))
print(kiwi.tokenize(text="가요"))
print(kiwi.tokenize(text="아버지는 진지를 드신다"))
print(kiwi.tokenize(text="그렇답니까?"))
print(kiwi.tokenize(text="하겠습니까?"))
print(kiwi.tokenize(text="그냥 해요"))
print(kiwi.tokenize(text="하지 마십시오"))
print(kiwi.tokenize(text="이제 시작한답니다"))
print(kiwi.tokenize(text="하겠습니다"))
print(kiwi.tokenize(text="이리 오십시오"))
print(kiwi.tokenize(text="여러분, 당신이 오셨습니다"))
print(kiwi.tokenize(text="가까우니 걸어갑시다"))
print(kiwi.tokenize(text="이리 오세요"))
print(kiwi.tokenize(text="한국의 목욕탕에서는 옷을 벗어"))
print(kiwi.tokenize(text="바로 누우면 안된대"))
print(kiwi.tokenize(text="버텨 봐요"))
print(kiwi.tokenize(text="좀만 더 버텨 봐"))
print(kiwi.tokenize(text="하지 마요"))
print(kiwi.tokenize(text="하지 마요"))

