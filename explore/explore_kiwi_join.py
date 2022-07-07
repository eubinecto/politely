from kiwipiepy import Kiwi

sent = "시끄럽게 코 고는 소리에 놀라서 난 잠이 깼다."
# --- Kiwipiepy로 띄어쓰기 및 원형 복구 --- #
kiwi = Kiwi()
tokens = kiwi.tokenize(sent)
print(sent)
print(kiwi.join(tokens))
print(kiwi.join([("흙", "NNG"), ("이", "JKS"), ("묻", "VV"), ("어요", "EF")]))
print(kiwi.join([("보", "VX"), ("어", "EF"), (".", "SF")]))
print(kiwi.join([("우", "VV"), ("어요", "EF"), (".", "SF")]))
print(kiwi.join([("이", "VCP"), ("야", "EF"), (".", "SF")]))
print(kiwi.join([("하", "VV"), ("습니다", "EF"), (".", "SF")]))
print(kiwi.join([("걸어가", "VV"), ("읍시다", "EF"), (".", "SF")]))

#  `join`시 ㄹ 법칙 오류
sent = "북한에서는 한글을 '조선글'이라 부른다."
print(kiwi.join(kiwi.tokenize(sent)))
sent = "북한에서는 한글을 조선글?이라 부른다."
print(kiwi.join(kiwi.tokenize(sent)))
sent = "북한에서는 한글을 조선글!이라 부른다."
print(kiwi.join(kiwi.tokenize(sent)))
sent = "북한에서는 한글을 조선글,이라 부른다."
print(kiwi.join(kiwi.tokenize(sent)))
sent = "북한에서는 한글을 조선글🔥이라 부른다."
print(kiwi.join(kiwi.tokenize(sent)))
sent = "북한에서는 한글을 조선글🔥으로 부른다."
print(kiwi.join(kiwi.tokenize(sent)))
# 특수기호가 없는 경우에는 정상적으로 출력 - 일단 이 이슈는 나중에!
sent = "북한에서는 한글을 조선글이라 부른다."  # 모음 탈락이 일어나면 안된다.
print(kiwi.join(kiwi.tokenize(sent)))
sent = "북한에서는 한글을 조선글으로 부른다."  #  모음 탈락.
print(kiwi.join(kiwi.tokenize(sent)))


# Another error?
sent = "비하적 의미가 없었다는 것이 정설이다. 더 자세한 내용은 한글/역사 문서로."
print(kiwi.join(kiwi.tokenize(sent)))
