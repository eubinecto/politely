from khaiii import KhaiiiApi


def main():
    api = KhaiiiApi()

    for token in api.analyze("정상에 이르렀다."):
        print(token)

    for token in api.analyze("아직 끝내기에는 일러."):
        print(token)

    # 음... 둘의 pos에 별 차이가 없네..


if __name__ == "__main__":
    main()
