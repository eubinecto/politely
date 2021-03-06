from khaiii import KhaiiiApi
from politely import analyser

sents = [
    "좋아요.",
    "좋습니다.",
    "불합리합니다.",
    "했네요.",
    "합시다.",
    "할게요.",
    "하겠습니다.",
    "감사해요.",
    "고마워.",
    "고마워요.",
    "고맙습니다.",
    "드릴게요.",
    "전설이야.",
    "해내는구나.",
    "있겠네.",
    "버리네.",
    "있으마.",
    "있을게요.",
    "할걸요.",
    "있을걸요.",
    "기다릴걸요.",
    "난오늘도그녀에게전화를건다",
    "말안들을래요.",
    "안들을겁니까.",
    "오늘도 그녀에게 전화를걸어요.",
    "당신의 고향은 어디인가요?",
    "거기 설탕 좀 줄래요?",
    "했을겁니다.",
    "전설이에요.",
    "전설입니다.",
    "안녕.",
    "모든 것을 걸게요.",
    "안녕하세요.",
    "안녕하십니까.",
    "끝나겠네요.",
]


def main():
    api = KhaiiiApi()
    for sent in sents:
        for token in api.analyze(sent):
            print("=====")
            print(token)

    for sent in sents:
        for token in analyser.analyze(sent):
            print("=====")
            print(token)


"""
# 굉장히 빠르고 정확하다! 띄어쓰기를 훼손하지도 않고... 심플하고... 정확히 내가 바라던 것인 것 같다.
konlpy, kiwi에 걸쳐... 여기에 종착하게 되는 것인가?
이걸 사용하면 훨씬 쉬울 것! lemma와 구성성분이 따로 있으므로..!

시끄럽게	시끄럽/VA + 게/EC
코고는	코/NNG + 골/VV + 는/ETM
소리에	소리/NNG + 에/JKB
놀라서	놀라/VV + 아서/EC
난	나/NP + ㄴ/JX
잠이	잠/NNG + 이/JKS
깼다.	깨/VV + 었/EP + 다/EF + ./SF
"""

if __name__ == "__main__":
    main()
