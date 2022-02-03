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
    tokens = kiwi.tokenize(text="나는 공부해")


if __name__ == '__main__':
    main()

