
from kps.fetchers import fetch_okt
from kiwipiepy import Kiwi


def main():
    sent = "저는 그 노래를 들어요"
    okt = fetch_okt()
    kiwi = Kiwi()
    print(okt.morphs(sent, stem=True))
    print([token.form for token in kiwi.tokenize(sent)])

    """
    # 듣다라는 어간이 나와야 하는데, okt는 맥락으로부터 듣다를 파악 못함.
    ['저', '는', '그', '노래', '를', '들다']
    # 하지만 kiwi는 맥락으로부터 어간이 듣-이라는 것을 파악할 수 있음.
    ['저', '는', '그', '노래', '를', '듣', '어요']
    """

    sent = "저는 그 상자를 들어요"
    okt = fetch_okt()
    kiwi = Kiwi()
    print(okt.morphs(sent, stem=True))
    print([token.form for token in kiwi.tokenize(sent)])

    """
    ['저', '는', '그', '상자', '를', '들다']
    # 노래를 -> 상자를로 바뀌면, 어간이 들-로 바뀌는 것을 알 수 있음. 이게 더 정확하다.
    ['저', '는', '그', '상자', '를', '들', '어요']
    """

    # 결론 = 그래서 konlpy보단 kiwi를 쓰는 편이 더 정확할 것이다.

if __name__ == '__main__':
    main()