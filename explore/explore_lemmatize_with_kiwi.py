from typing import List, Tuple
from politetune.fetchers import fetch_komoran
from kiwipiepy import Kiwi
from kiwipiepy import Token


def lemmatize(sent: str) -> List[Tuple[str, str]]:
    kiwi = Kiwi()
    tokens = kiwi.tokenize(sent)
    # 어미를 전부 -다로 교체하면... 되긴하는데... 음..
    lemmas = [
        (token.form + "다", token.tag) if token.tag in ("XSV", "VV") else (token.form, token.tag)
        for token in tokens
        if not token.tag.startswith("E")
    ]
    return lemmas


def main():
    print(lemmatize("먹어요"))
    print(lemmatize("저기로 가요"))  # this does not work
    print(lemmatize("아버지는 밥을 잡수신다"))



if __name__ == '__main__':
    main()