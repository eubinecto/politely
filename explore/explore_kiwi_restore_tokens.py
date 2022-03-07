"""
나는 지금 문법 교정기를 만드는게 아니라.. 존댓말 교정기를 만드는 중이다..
그런데 kiwi가 입력 단어를 훼손하기 때문에 (e.g. 시끄러운 -> 시끄럽운, 코고는 -> 코골는) 다시 원래대로 돌리려면
국문법을 내가 코딩해야한다.
물론 그런게 아주 쓸모없는 것은 아닌데, 원형이 아예 사라져버리는 건 문제가 있다.
굳이 이렇게 할필요 없다. spacy처럼 기존의 토큰을 훼손하지 않으면 된다.
내가 해야하는건.. 종결어미만 바꾸면 되는데.. 그냥 전체를 바꿔버리고 있다.
"""

from kiwipiepy import Kiwi

kiwi = Kiwi()


def main():
    sent = "시끄럽게 코고는 소리에 놀라서 난 잠이 깼다."
    tokens = kiwi.tokenize(sent)
    print(tokens)
    orths = [
        sent[token.start: token.start + token.len] if token.len > 0
        else ""
        for token in tokens
    ]
    # 존대
    tuned = [
    "어요" if f"{token.form}+{token.tag}" == "다+EF"
    else orth
    for token, orth in zip(tokens, orths)
    ]
    print("".join(tuned))
    # 반말
    tuned = [
    "습니다" if f"{token.form}+{token.tag}" == "다+EF"
    else orth
    for token, orth in zip(tokens, orths)
    ]
    print("".join(tuned))
    
        # orth -> lemmatized
    orth2lemma = [
        (token.form, orth)
        for token, orth in zip(tokens, orths)
    ]
    print(orth2lemma)

    # 왜 겹치는 구간이 나오는거지..
    # 그리고 spacing을 구하는 것까지 생각해보면...
    # 왜 이런 것까지 고려를 하지 못한 것일까? (어렵다는 건 알겠지만은...)
    # 이상적인 출력:
    # (text=시끄러, lemma=시끄럽), (text=운, lemma=은), (text=코, lemma=코),
    # (text=고, lemma=골), (text=는, lemma=는)


if __name__ == '__main__':
    main()

