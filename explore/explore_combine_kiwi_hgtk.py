from kiwipiepy import Kiwi
import hgtk


def main():
    sents = [
        "나는 공부하고 있어",
        "나는 공부해",
        "나는 공부할래",
    ]
    kiwi = Kiwi()
    # have a look at the tokens, first
    for sent in sents:
        texts = [
            token.form
            for token in kiwi.tokenize(sent)
        ]
        print(texts)

    # 단순히 EF -> 요로 바꾸면?
    # 나는 공부하고 있요
    # 나는 공부하요
    # 나는 공부하요
    print("-----")
    for sent in sents:
        texts = [
            "요" if token.tag == "EF" else token.form
            for token in kiwi.tokenize(sent)
        ]
        print(texts)

    # 여기에서....
    # 있요 -> 있어요
    # 하요 -> 해요
    # 로 바꾸는 로직이 필요하다. 여기에 hgtk를 쓸 수 있는걸까?
    # hgtk의 무엇을 쓸 수 있는 걸까?
    # 우선, 부족한게 무엇인지 파악해보자:
    print("---")
    print(kiwi.tokenize("저는 공부해요"))
    print(kiwi.tokenize("나는 물을 마셔"))

    # -어요. 가 필요한 것.
    # 그렇다면, EF 대신에 넣어야 할 것은 요가 아니라 -어요다:
    print("---")
    for sent in sents:
        texts = [
            "어요" if token.tag == "EF" else token.form
            for token in kiwi.tokenize(sent)
        ]
        print(texts)

    print("---")
    # 하어 -> 해로 바꾸면 얼추 될 것 같은데?
    for sent in sents:
        texts = "".join([
            "어요" if token.tag == "EF" else token.form
            for token in kiwi.tokenize(sent)
        ])
        texts = texts.replace("하어", "해")
        print(texts)


if __name__ == '__main__':
    main()
