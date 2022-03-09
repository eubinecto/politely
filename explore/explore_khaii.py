"""
깃허브:
https://github.com/kakao/khaiii
설치에 대한 더 간단한 설명:
https://miniolife.tistory.com/16
음... 그런데 이걸 streamlit에 배포를 하기 위해선...
"""
from khaiii import KhaiiiApi


def main():
    api = KhaiiiApi()
    for word in api.analyze("시끄럽게 코고는 소리에 놀라서 난 잠이 깼다."):
        print(word)


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

if __name__ == '__main__':
    main()
