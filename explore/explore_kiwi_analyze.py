"""
You may want to replace konlpy with  kiwi, if it helps.
well, we will think about doing this later on. Just not now.

"""
from kiwipiepy import Kiwi


kiwi = Kiwi()
kiwi.add_user_word("해")
print(kiwi.split_into_sents(text="아버지는 진지를 드신다. 하지만 난 방에서 공부하고 있다"))

