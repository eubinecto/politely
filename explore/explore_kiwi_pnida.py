from kiwipiepy import Kiwi

kiwi = Kiwi()


def main():
    sent = "이만 가보겠습니다"
    print(kiwi.tokenize(sent))


if __name__ == "__main__":
    main()
