"""
You may want to replace konlpy with  kiwi, if it helps.
well, we will think about doing this later on. Just not now.

"""
from kiwipiepy import Kiwi


kiwi = Kiwi()
print(kiwi.split_into_sents("아버지는 진지를 드신다. 나는 밥을 먹는다."))

print("----")
for sent in kiwi.split_into_sents("한글(훈민정음)은 창제된 이후 약 500년 동안 많은 시련을 겪었다. 조선의 선비들은 한글을 무시하고 홀대했으며 연산군은 한글 사용을 탄압했다.[14][15][16] 일제는 조선어학회 사건(1942)을 조작하는 등 한국어와 한글 사용을 금지하는 민족정신 말살정책을 펼쳤다. 이런 어려움 속에서도 주시경, 최현배등 많은 선각자들이 한글을 체계적으로 연구하여 한글의 우수성을 알리고 널리 보급하려 노력하였다."):
    print(sent)

print("----")
for sent in kiwi.split_into_sents("한글(훈민정음)은 창제된 이후 약 500년 동안 많은 시련을 겪었다. 조선의 선비들은 한글을 무시하고 홀대했으며 연산군은 한글 사용을 탄압했다.[14][15][16] 일제는 조선어학회 사건(1942)을 조작하는 등 한국어와 한글 사용을 금지하는 민족정신 말살정책을 펼쳤다. 이런 어려움 속에서도 주시경, 최현배등 많은 선각자들이 한글을 체계적으로 연구하여 한글의 우수성을 알리고 널리 보급하려 노력하였다.", return_tokens=True):
    print(sent)

print("----")
for sent in kiwi.split_into_sents("한국의 목욕탕에서는 옷을 벗어 그러니까 놀라지마!", return_tokens=True):
    print(sent)
