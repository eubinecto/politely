import khaiii
from soynlp.lemmatizer._conjugation import conjugate

api = khaiii.KhaiiiApi()


# you probably don't need to reinvent the wheel/
def main():
    # we need to get this conjugations working
    print(conjugate("줍", "어", debug=True))
    print(conjugate("걷", "어", debug=True))
    # 하지만..
    print(conjugate("줍우", "어", debug=True))
    # 이건.. 어떻게?
    print(conjugate("줍", "워"))
    # 이렇게 해야한다.
    # 그렇다면.... R -> L 알고리즘을 쓰면 되지 않을까?
    sent = "그런 현상을 일컬어요."
    for token in api.analyze(sent):
        print(token)
    print(conjugate("일컫", "어요"))  # -> 일컬어요
    # basic alogorithm; work on it chunk-by-chunk


if __name__ == '__main__':
    main()
