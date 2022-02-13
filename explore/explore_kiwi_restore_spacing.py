"""
kiwi의 문제 = spacing이 사라져버린다... 음...s
이는 spacy와의 매우 큰 차이점이다. spacy는 띄어쓰기도 보존이 된다.
"""
import numpy as np
from kiwipiepy import Kiwi


def main():
    sent = "나는 달려요"
    sent = sent.replace(" ", " " * 2)  # just a quirk with kiwi - the spacings must be longer than 1.
    kiwi = Kiwi()
    tokens = kiwi.tokenize(sent)
    print(tokens)
    # --- the logic for restoring the spacings starts here --- #
    # 이게 내가할 수 있는 최선... 토큰에 진작에 whitespace가 추가 되어 있었다면, 큰 문제가 되지는 않았을텐데.
    # 물론 모델에다가 가장 노이즈가 없는 상태를 넣어야한다는 것은 공감이 가기는 하지만..
    starts = np.array([token.start for token in tokens] + [0])
    lens = np.array([token.len for token in tokens] + [0])
    sums = np.array(starts) + np.array(lens)
    spacings = (starts[1:] - sums[:-1]) > 0  # if it is greater than 1, than it should be spaced.
    texts = [
        token.form + " " if spacing else token.form
        for token, spacing in zip(tokens, spacings)
    ]
    sent = "".join(texts)
    # 이걸 뭐라고 부르나? 줄임말?
    # 이렇게 바뀌어가는 lineage를 계속 기록해나가는 것도 중요할듯!
    sent = sent.replace("하어", "해")
    sent = sent.replace("리어", "려")
    print(sent)


if __name__ == '__main__':
    main()
