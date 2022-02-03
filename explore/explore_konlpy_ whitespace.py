from konlpy.tag import Okt
# zulu - macOS/arm64/version15 설치 이후.
# 해당 path를 지정.
JVM_PATH = '/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/bin/java'


def main():
    okt = Okt(jvmpath=JVM_PATH)
    # how do I keep the whitespace? The only way possible is
    tokens = okt.morphs("나는 마셔", norm=True, stem=True)
    print(tokens)


if __name__ == '__main__':
    main()