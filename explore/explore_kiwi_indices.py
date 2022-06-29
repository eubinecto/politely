from kiwipiepy import Kiwi

kiwi = Kiwi()

sent = "시끄럽게 코고는 소리에 놀라서 난 잠이 깼다."


def main():
    tokens = kiwi.tokenize(sent)
    for token in tokens:
        print(token, sent[token.start : token.end])


if __name__ == "__main__":
    main()
