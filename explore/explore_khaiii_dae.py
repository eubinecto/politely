from khaiii import KhaiiiApi


def main():
    api = KhaiiiApi()
    for token in api.analyze("밥먹고 바로 누우면 안 된대."):
        print(token)


if __name__ == "__main__":
    main()
