from kiwipiepy import Kiwi
import numpy as np

# to be used for testing
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
]

# these are pretty much all you need?
HONORIFICS = {
    "어+EF": ("어", "어요"),
    "ᆯ래+EF": ("어", "어요"),
    "ᆫ다+EF": ("어", "어요"),
    "자+EF": ("어", "어요"),
    "어요+EF": ("어", "어요"),
    "나+NP": ("나", "저"),
    "저+NP": ("나", "저"),
}

# https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&qna_seq=38766
ABBREVIATIONS = {
    "하어": "해",
    "리어": "려",
    "시어": "셔",
    "지어": "져",
    "티어": "텨",
    "니어": "녀",
    "히어": "혀",
    "이어": "여",
    "보어": "봐",
    "나의": "내",
    "저의": "제",
}


kiwi = Kiwi()


def honorify(sent: str, honored: bool) -> str:
    # preprocess the sentence
    sent = sent + "." if not sent.endswith(".") else sent  # for accurate pos-tagging
    sent = sent.replace(" ", " " * 2)  # for accurate spacing
    # tokenize the sentence, and replace all the EFs with their honorifics
    tokens = kiwi.tokenize(sent)
    texts = [HONORIFICS.get(f"{token.form}+{token.tag}", (token.form,) * 2)[honored] for token in tokens]
    # restore spacings
    starts = np.array([token.start for token in tokens] + [0])
    lens = np.array([token.len for token in tokens] + [0])
    sums = np.array(starts) + np.array(lens)
    spacings = (starts[1:] - sums[:-1]) > 0
    sent = "".join([text + " " if spacing else text for text, spacing in zip(texts, spacings)])
    # abbreviate tokens
    for key, val in ABBREVIATIONS.items():
        sent = sent.replace(key, val)
    return sent


def main():
    for sent in SENTS:
        print(sent, "->", honorify(sent, False), "|", honorify(sent, True))

    """
    나는 공부하고 있어 -> 나는 공부하고 있어. | 저는 공부하고 있어요.
    저는 공부하고 있어요 -> 나는 공부하고 있어. | 저는 공부하고 있어요.
    나는 공부해 -> 나는 공부해. | 저는 공부해요.
    난 공부해 -> 난 공부해. | 전 공부해요.
    나는 공부할래 -> 나는 공부해. | 저는 공부해요.
    나는 공부한다 -> 나는 공부해. | 저는 공부해요.
    나는 물을 마신다 -> 나는 물을 마셔. | 저는 물을 마셔요.
    나는 마셔 -> 나는 마셔. | 저는 마셔요.
    자동차가 도로를 달려 -> 자동차가 도로를 달려. | 자동차가 도로를 달려요.
    자동차가 도로를 달린다 -> 자동차가 도로를 달려. | 자동차가 도로를 달려요.
    자동차가 도로를 달려요 -> 자동차가 도로를 달려. | 자동차가 도로를 달려요.
    도로가 많이 막힌다 -> 도로가 많이 막혀. | 도로가 많이 막혀요.
    나는 학원을 다닌다 -> 나는 학원을 다녀. | 저는 학원을 다녀요.
    나는 내 목표를 향해 달린다 -> 나는 내 목표를 향해 달려. | 저는 제 목표를 향해 달려요.
    한번 달려보자 -> 한번 달려봐. | 한번 달려봐요.
    좀만 더 버텨보자 -> 좀만 더 버텨봐. | 좀만 더 버텨봐요.
    좀만 더 버텨봐 -> 좀만 더 버텨봐. | 좀만 더 버텨봐요.
    """


if __name__ == "__main__":
    main()
