from kiwipiepy import Kiwi

sent = "시끄럽게 코 고는 소리에 놀라서 난 잠이 깼다."
# --- Kiwipiepy로 띄어쓰기 및 원형 복구 --- #
kiwi = Kiwi()
tokens = kiwi.tokenize(sent)
print(sent)
print(kiwi.join(tokens))
print(kiwi.join([('흙', "NNG"), ('이', 'JKS'), ('묻', 'VV'), ('어요', 'EF')]))
print(kiwi.join([('보', 'VX'), ('어', 'EF'), ('.', 'SF')]))
print(kiwi.join([('우', 'VV'), ('어요', 'EF'), ('.', 'SF')]))
print(kiwi.join([('이', 'VCP'), ('야', 'EF'), ('.', 'SF')]))
print(kiwi.join([('하', 'VV'), ('습니다', 'EF'), ('.', 'SF')]))
print(kiwi.join([('걸어가', 'VV'), ('읍시다', 'EF'), ('.', 'SF')]))
