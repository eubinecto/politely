
from politetune.tuner import Tuner

SENTS = [
    "나는 공부하고 있어",
    "저는 공부하고 있어요",
    "나는 공부해",
    "난 공부해",
    "나는 공부할래",
    "나는 공부한다",
    "나는 물을 마신다",
    "나는 마셔",
    "자동차가 도로를 달려",
    "자동차가 도로를 달린다",
    "자동차가 도로를 달려요",
    "도로가 많이 막힌다",
    "나는 학원을 다닌다",
    "나는 내 목표를 향해 달린다",
    "한번 달려보자",
    "좀만 더 버텨보자",
    "좀만 더 버텨봐",
    "이것 좀 들어줘",
]

tuner = Tuner()


def main():
    for sent in SENTS:
        unhonored = tuner(sent, "friend", "private")['tuned']
        honored = tuner(sent, "friend", "public")['tuned']
        print(sent, "->", unhonored, "|", honored)


if __name__ == '__main__':
    main()