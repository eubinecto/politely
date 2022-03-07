from kiwipiepy import Kiwi

kiwi = Kiwi()


def main():
    sent = "시끄럽게 코고는 소리에 놀라서 난 잠이 깼다."
    tokens = kiwi.tokenize(sent)
    print(tokens)
    for token in tokens:
        print(token.form, sent[token.start:token.end])


if __name__ == '__main__':
    main()