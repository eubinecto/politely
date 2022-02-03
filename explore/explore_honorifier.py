from politetune.honorifier import Honorifier


def main():
    listener = "teacher"
    visibility = "private"
    sent = "나는 공부하고 선생님도 공부해"
    honorifier = Honorifier()
    honorified = honorifier(sent, listener, visibility)
    print(honorified)
    print(honorifier.honored)


if __name__ == '__main__':
    main()