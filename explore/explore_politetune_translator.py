
from politetune.processors import Translator


def main():
    t = Translator()
    print(t("hello world"))


if __name__ == '__main__':
    main()
