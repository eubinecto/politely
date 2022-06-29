from politely import Styler
from pprint import pprint


def main():
    styler = Styler()
    print(styler.logs)
    print(styler.logs)
    print(styler("나한테 왜 그런거야?", 2))
    pprint(styler.logs)


if __name__ == "__main__":
    main()
