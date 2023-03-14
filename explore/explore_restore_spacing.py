"""
어떻게 기존의 spacing을 유지할 수 있을까?
"""
from kiwipiepy import Kiwi
import numpy as np
kiwi = Kiwi()
sent = "나는 널 사 랑해"
tokens = kiwi.tokenize(sent)
# starts & lens를 ... 수정 후에도 ... 계속 바꿔줘야한다.
# 그게 문제다. 음...?
# 그렇다면, 사용자정의사전을 계속 추가하는 것이 필요할 것.
# 여기서 그리할 것이 아니라.... ㅇㅇ
# 이건 그냥 이렇게 남기겠다.
starts = np.array([token.start for token in tokens] + [0])
lens = np.array([token.len for token in tokens] + [0])
sums = np.array(starts) + np.array(lens)
spacings = (starts[1:] - sums[:-1]) > 0  # if it is greater than 1, than it should be spaced.
chunks = [f"{token.form}🏷{token.tag}" + "\n" if spacing else f"{token.form}🏷{token.tag}"
          for token, spacing in zip(tokens, spacings)]
sent = "🔗".join(chunks)
print(sent)
new_sent = ""
for chunk in sent.split("\n"):
    print(chunk)
    new_sent += kiwi.join([tuple(token.split("🏷")) for token in chunk.strip("🔗").split("🔗")]).replace(" ", "") + " "
