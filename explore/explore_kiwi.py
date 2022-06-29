"""
You may want to replace konlpy with  kiwi, if it helps.
well, we will think about doing this later on. Just not now.

"""
from kiwipiepy import Kiwi


def main():
    kiwi = Kiwi()
    kiwi.add_user_word("해")
    print(kiwi.tokenize(text="나는 공부해"))
    print(kiwi.tokenize(text="나는 공부해요"))
    print(kiwi.tokenize(text="저기로 가요"))
    print(kiwi.tokenize(text="가요"))
    print(kiwi.tokenize(text="아버지는 진지를 드신다"))


if __name__ == "__main__":
    main()
