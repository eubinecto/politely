import hgtk


def main():
    print(hgtk.letter.compose(chosung="ㄴ", joongsung="ㅏ"))  # 종성은 optional
    print(hgtk.letter.compose(chosung="ㄴ", joongsung="ㅏ", jongsung="ㄴ"))


if __name__ == "__main__":
    main()
