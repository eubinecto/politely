from politely import Styler
from kiwipiepy import Kiwi
from pprint import pprint
# an excerpt from 동백꽃 (김유정)
text = """잔소리를 두루 늘어놓다가 남이 들을까봐 손으로 입을 틀어막고는 그 속에서 깔깔댄다. 별로 우스울 것도 없는데 날씨가 풀리더니 이 놈의 계집애가 미쳤나 하고 의심하였다.
게다가 조금 뒤에는 제 집께를 할금할금 돌아보더니 행주치마의 속으로 꼈던 바른손을 뽑아서 나의 턱밑으로 불쑥 내미는 것이다. 
언제 구웠는지 더운 김이 홱 끼치는 굵은 감자 세 개가 손에 뿌듯이 쥐였다. "느 집엔 이거 없지?" 하고 생색있는 큰소리를 하고는 제가 준 것을 남이 알면은 큰일날테니 여기서 얼른 먹어 버리란다.
그리고 또 하는 소리가, "너 봄감자가 맛있단다." "난 감자 안 먹는다. 너나 먹어라." 나는 고개도 돌리지 않고 일하던 손으로 그 감자를 도로 어깨 너머로 쑥 밀어 버렸다.
그랬더니 그래도 가는 기색이 없고, 뿐만 아니라 쌔근쌔근하고 심상치 않게 숨소리가 점점 거칠어진다. 이건 또 뭐야 싶어서 그때에야 비로소 돌아다보니 나는 참으로 놀랐다.
우리가 이 동네에 들어온 것은 근 삼년째 되어오지만 여태껏 가무잡잡한 점순이의 얼굴이 이렇게까지 홍당무처럼 새빨개진 법이 없었다.
게다가 눈에 독을 올리고 한참 나를 요렇게 쏘아보더니 나중에는 눈물까지 어리는 것이 아니냐.
그리고 바구니를 다시 집어들더니 이를 꼭 악물고는 엎어질 듯 자빠질 듯 논둑으로 횡하게 달아나는 것이다."""
# split the text into sentences using whatever tools you prefer.
kiwi = Kiwi()
sents = [sent.text.strip() for sent in kiwi.split_into_sents(text)]
# instantiate a Styler object.
styler = Styler()
# to a polite style
pprint(" ".join([styler(sent, 1) for sent in sents]))
print("###")
# to a formal style
pprint(" ".join([styler(sent, 2) for sent in sents]))