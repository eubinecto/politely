
from kiwipiepy import Kiwi
kiwi = Kiwi()


def main():
    # This is much better!
    sent = "시끄럽게 코고는 소리에 놀라서 난 잠이 깼다."
    tokens = kiwi.tokenize(sent)
    for token in tokens:
        if f"{token.form}+{token.tag}" == "다+EF":
            sent = sent[:token.start] + "어요" + sent[token.end:]

        if f"{token.form}+{token.tag}" == "난+NP":
            sent = sent[:token.start] + "전" + sent[token.end:]
    print(sent)


if __name__ == '__main__':
    main()
