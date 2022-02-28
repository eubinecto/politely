"""
ㄹ 받침을 어떻게 처리하는지?
"""
from kiwipiepy import Kiwi


kiwi = Kiwi()


def main():
    sent = "느는 건 빛뿐이야"
    tokens = kiwi.tokenize(sent)
    for token in tokens:
        print(token)


if __name__ == '__main__':
    main()
