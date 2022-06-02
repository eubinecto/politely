from konlpy.tag import Okt, Kkma

JVM_PATH = "/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/bin/java"


examples = [
    "우리 같이 공부하자",  # 문제 -> 공부, 하다로 쪼개진다. 하지만 이 경우는.. 하다 -> 해요, 해로 바꾸는 것으로 구현 가능함.
    "우린 같이 물을 마신다",
    "우리 같이 가자",
    "나는 그게 뭔지 몰라요",
    "나는 그 노래를 들어요",  # 규칙 기반 표제어 추출기의 문제... 가 여기에 있네.
    "나는 그 상자를 들어요",
    "아 목마르다",
    "나는 공부할래",
    "그가 여기로 오네",
]

# 한국어 -> lemmatizer가.. 좀 문제가 많네.
# 어요 -> 어.


def main():
    okt = Okt(jvmpath=JVM_PATH)
    kkma = Kkma(jvmpath=JVM_PATH)

    for s in examples:
        tokens = okt.morphs(phrase=s, stem=True)
        print(tokens)

    # kkma does not support stemming, so this is not really useful.
    # for s in examples:
    #     tokens = kkma.morphs(phrase=s)
    #     print(tokens)


if __name__ == "__main__":
    main()
