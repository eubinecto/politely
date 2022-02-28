"""
다음의 링크에서 가져왔다:
https://github.com/konlpy/konlpy/issues/353#issuecomment-916166604
"""

from konlpy.tag import Okt, Komoran
# zulu - macOS/arm64/version15 설치 이후.
# 해당 path를 지정.
JVM_PATH = '/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/bin/java'


def main():
    komoran = Komoran(jvmpath=JVM_PATH)
    tokens = komoran.morphs("나는 마셔")
    print(tokens)
    tokens = komoran.morphs("저는 고마워요")
    print(tokens)
    tok2pos = komoran.pos("나는 공부하고 있어. 선생님은 물을 마셔.")
    print(tok2pos)


if __name__ == '__main__':
    main()
