import khaiii
from soynlp.lemmatizer._conjugation import conjugate

api = khaiii.KhaiiiApi()


# you probably don't need to reinvent the wheel.... yeah, just don't reinvent the wheel.
# build on top of this already useful library, if you can.
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
    print(conjugate("떠나", "ㅂ시다"))  # -> 일컬어요
    print(conjugate("되", "ㄴ대요"))  # -> 일컬어요
    print(conjugate("떠나", "어요"))  # -> 일컬어요
    print(conjugate("가시", "ㅂ니다"))  # -> 일컬어요
    print(conjugate("먹", "ㅂ니다"))  # -> 일컬어요
    print(conjugate("사", "았어"))  # -> 일컬어요
    print(conjugate("어떻", "습니까"))  # -> 일컬어요
    print(conjugate("하였", "습니까"))  # -> 일컬어요
    print(conjugate("어떻", "어요"))  # -> 일컬어요
    print(conjugate("파랗", "아"))  # -> 일컬어요
    print(conjugate("하", "였어?"))  # -> 일컬어요 ddd
    print(conjugate("마시", "어"))  # -> 일컬어요 ddd
    print(conjugate("나", "어"))  # -> 일컬어요 ddd
    print(conjugate("것", "이야"))  # -> 일컬어요 ddd
    print(conjugate("되", "ㅂ니다"))  # -> 일컬어요 ddd


if __name__ == '__main__':
    main()
