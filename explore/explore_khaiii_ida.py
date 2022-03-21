from khaiii import KhaiiiApi


def main():
    api = KhaiiiApi()
    for token in api.analyze("내가 원하는 것은 그것이다."):
        print(token)


if __name__ == '__main__':
    main()
