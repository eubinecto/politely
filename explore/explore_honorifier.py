from main import Honorifier, load_okt
from annotated_text import annotated_text

def main():
    listener = "teacher"
    visibility = "private"
    sent = "나는 공부하고 선생님도 공부해"
    okt = load_okt()
    honorifier = Honorifier(okt)
    honorified = honorifier(sent, listener, visibility)
    print(annotated_text(*honorified))


if __name__ == '__main__':
    main()