from konlpy.tag import Komoran, Kkma, Hannanum

JVM_PATH = '/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/bin/java'


def main():
    sent = "나는 한다."
    # Komoran
    analyzer = Komoran(jvmpath=JVM_PATH)
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    sent = "저는 공부해요."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    sent = "나랑 공부하자."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    # so.. the way it should go is: you have to check both
    # the lemma and the pos..
    # if lemma == 나 && pos == Noun:
    #   나 -> 나, 저.
    sent = "나는 공부하고 선생님도 공부해요."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    sent = "시끄러운 코고는 소리에 난 잠이 깼다."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    print("-----")
    analyzer = Hannanum(jvmpath=JVM_PATH)
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    sent = "저는 공부해요."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    sent = "나랑 공부하자."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    # so.. the way it should go is: you have to check both
    # the lemma and the pos..
    # if lemma == 나 && pos == Noun:
    #   나 -> 나, 저.
    sent = "나는 공부하고 선생님도 공부해요."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    sent = "시끄러운 코고는 소리에 난 잠이 깼다."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    print("---")
    analyzer = Komoran(jvmpath=JVM_PATH)
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    sent = "저는 공부해요."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    sent = "나랑 공부하자."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    # so.. the way it should go is: you have to check both
    # the lemma and the pos..
    # if lemma == 나 && pos == Noun:
    #   나 -> 나, 저.
    sent = "나는 공부하고 선생님도 공부해요."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos
    sent = "시끄러운 코고는 소리에 난 잠이 깼다."
    tok2pos = analyzer.pos(sent)
    print(tok2pos)  # tok2pos


if __name__ == '__main__':
    main()
