from khaiii import KhaiiiApi


def main():
    api = KhaiiiApi()
    for token in api.analyze("아빠 진지드세요"):
        print(token)


if __name__ == '__main__':
    main()