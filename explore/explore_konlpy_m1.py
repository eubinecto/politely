"""
다음의 링크에서 가져왔다:
https://github.com/konlpy/konlpy/issues/353#issuecomment-916166604
"""

from konlpy.tag import Okt
# zulu - macOS/arm64/version15 설치 이후.
# 해당 path를 지정.
JVM_PATH = '/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/bin/java'


def main():
    okt = Okt(jvmpath=JVM_PATH)
    tokens = okt.morphs("으아아아 M1 사용하기 피곤하네")
    print(tokens)


if __name__ == '__main__':
    main()
