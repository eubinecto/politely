import difflib


def main():
    cases = [
        ("afrykanerskojęzyczny", "afrykanerskojęzycznym"),
        ("afrykanerskojęzyczni", "nieafrykanerskojęzyczni"),
        ("afrykanerskojęzycznym", "afrykanerskojęzyczny"),
        ("nieafrykanerskojęzyczni", "afrykanerskojęzyczni"),
        ("nieafrynerskojęzyczni", "afrykanerskojzyczni"),
        ("abcdefg", "xac"),
    ]

    for a, b in cases:
        print("{} => {}".format(a, b))
        for i, s in enumerate(difflib.ndiff(a, b)):
            if s[0] == " ":
                continue
            elif s[0] == "-":
                print('Delete "{}" from position {}'.format(s[-1], i))
            elif s[0] == "+":
                print('Add "{}" to position {}'.format(s[-1], i))
        print()


if __name__ == "__main__":
    main()
