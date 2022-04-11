from typing import List, Tuple
from kps.fetchers import fetch_komoran
from kiwipiepy import Kiwi
from kiwipiepy import Token


def lemmatize(sent: str) -> List[Tuple[str, str]]:
    kiwi = Kiwi()
    tokens = kiwi.tokenize(sent)
    # 어미를 전부 -다로 교체하면... 되긴하는데... 음..
    lemmas = [
        (token.form + "다", token.tag) if token.tag in ("XSV", "VV", "VA", "VX") else (token.form, token.tag)
        for token in tokens
        if not token.tag.startswith("E")
    ]
    return lemmas


def main():
    print(lemmatize("먹는다"))
    print(lemmatize("저기로 간다"))
    print(lemmatize("아버지는 밥을 먹는다"))
    print(lemmatize("우리는 그 길로 가고 있다"))
    print(lemmatize("오늘따라 목마르다"))
    # 종결 어미(EF)만을 높이면 된다 ->


if __name__ == '__main__':
    main()