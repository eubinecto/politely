from politely.fetchers import fetch_komoran


def lemmatize(word: str) -> str:
    komoran = fetch_komoran()
    morphtags = komoran.pos(
        word,
    )
    print(morphtags)
    if morphtags[0][1] == "VA" or morphtags[0][1] == "VV":
        return morphtags[0][0] + "다"


def main():
    print(lemmatize("먹어요"))
    print(lemmatize("저기로 가요"))  # this does not work


if __name__ == "__main__":
    main()
