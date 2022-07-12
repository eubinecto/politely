# Politely
[![PyPI version](https://badge.fury.io/py/politely.svg)](https://badge.fury.io/py/politely)
![Workflow status](https://github.com/eubinecto/politely/actions/workflows/tests.yml/badge.svg)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://eubinecto-politely-main-streamlit-4vmces.streamlitapp.com)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1tpx_wrMmzD_pWeEibeenlU4q8TuKK1j7?usp=sharing)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Feubinecto%2Fpolitely&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
[![Downloads](https://pepy.tech/badge/politely)](https://pepy.tech/project/politely)
[![Downloads](https://pepy.tech/badge/politely/week)](https://pepy.tech/project/politely)

`Politely` is a rule-based politeness styler for the Korean language | 
--- | 
<img width="1010" alt="image" src="https://user-images.githubusercontent.com/56193069/168471756-084409db-5d72-48b7-820f-05e1de6b1f5a.png"> | 


## Quick Start 🚀
### 1️⃣ Install `politely`

```python3
pip3 install politely
```

### 2️⃣ Split your text into sentences
Split your text into sentences with whatever tools you prefer. Here, we use [`kiwipiepy`](https://github.com/bab2min/kiwipiepy) for the sake of demonstration:
```python3
from kiwipiepy import Kiwi
# an excerpt from 동백꽃 (김유정)
text = """잔소리를 두루 늘어놓다가 남이 들을까봐 손으로 입을 틀어막고는 그 속에서 깔깔댄다. 별로 우스울 것도 없는데 날씨가 풀리더니 이 놈의 계집애가 미쳤나 하고 의심하였다.
게다가 조금 뒤에는 제 집께를 할금할금 돌아보더니 행주치마의 속으로 꼈던 바른손을 뽑아서 나의 턱밑으로 불쑥 내미는 것이다. 
언제 구웠는지 더운 김이 홱 끼치는 굵은 감자 세 개가 손에 뿌듯이 쥐였다. "느 집엔 이거 없지?" 하고 생색있는 큰소리를 하고는 제가 준 것을 남이 알면은 큰일날테니 여기서 얼른 먹어 버리란다.
그리고 또 하는 소리가, "너 봄감자가 맛있단다." "난 감자 안 먹는다. 너나 먹어라." 나는 고개도 돌리지 않고 일하던 손으로 그 감자를 도로 어깨 너머로 쑥 밀어 버렸다.
그랬더니 그래도 가는 기색이 없고, 뿐만 아니라 쌔근쌔근하고 심상치 않게 숨소리가 점점 거칠어진다. 이건 또 뭐야 싶어서 그때에야 비로소 돌아다보니 나는 참으로 놀랐다.
우리가 이 동네에 들어온 것은 근 삼년째 되어오지만 여태껏 가무잡잡한 점순이의 얼굴이 이렇게까지 홍당무처럼 새빨개진 법이 없었다.
게다가 눈에 독을 올리고 한참 나를 요렇게 쏘아보더니 나중에는 눈물까지 어리는 것이 아니냐.
그리고 바구니를 다시 집어들더니 이를 꼭 악물고는 엎어질 듯 자빠질 듯 논둑으로 횡하게 달아나는 것이다."""
kiwi = Kiwi()
sents = [sent.text.strip() for sent in kiwi.split_into_sents(text)]
```

### 3️⃣ Speak `politely` with `Styler` 

Instantiate an object of `Styler`, and style your sentences in a polite or formal manner with `styler`:
```python3
from politely import Styler
from pprint import pprint
styler = Styler()
pprint(" ".join(styler(sents, 2)))  # 2 = polite
```
```text
('잔소리를 두루 늘어놓다가 남이 들을까 봐 손으로 입을 틀어막고는 그 속에서 깔깔대요. 별로 우스울 것도 없는데 날씨가 풀리더니 이 놈의 '
 '계집애가 미쳤나 하고 의심했어요. 게다가 조금 뒤에는 제 집께를 할 금할 금 돌아보더니 행주치마의 속으로 꼈던 바른 손을 뽑아서 제 턱 '
 '밑으로 불쑥 내미는 게에요. 언제 구웠는지 더운 김이 홱 끼치는 굵은 감자 세 개가 손에 뿌듯이 쥐였어요. "느 집에는 이 거 없죠? '
 '"하고 생색 있는 큰 소리를 하고는 제가 준 것을 남이 알면은 큰일 날 테니 여기서 얼른 먹어 버리래요. 그리고 또 하는 소리가,"당신 '
 '봄 감자가 맛있어요. ""난 감자 안 먹어요. 당신이나 먹어요. "저는 고개도 돌리지 않고 일하던 손으로 그 감자를 도로 어깨 너머로 쑥 '
 '밀어 버렸어요. 그랬더니 그래도 가는 기색이 없고, 뿐만 아니라 쌔근쌔근하고 심상하지 않게 숨소리가 점점 거칠어져요. 이거는 또 뭐야 '
 '싶어서 그 때에야 비로소 돌아다보니 저는 참으로 놀랐어요. 저희가 이 동네에 들어온 것은 근 삼 년째 돼 오지만 여태껏 가무잡잡한 점수는 '
 '이의 얼굴이 이렇게까지 홍당무처럼 새빨개진 법이 없었어요. 게다가 눈에 독을 올리고 한참 저를 요렇게 쏘아보더니 나중에는 눈물까지 어리는 '
 '게 아녀요. 그리고 바구니를 다시 집어 들더니 이를 꼭 악물고는 엎어질 듯 자빠질 듯 논둑으로 횡하게 달아나는 게에요.')
 ```
 
 ```python3
 pprint(" ".join(styler(sents, 3)))  # 3 = formal
```
```text
('잔소리를 두루 늘어놓다가 남이 들을까 봐 손으로 입을 틀어막고는 그 속에서 깔깔댑니다. 별로 우스울 것도 없는데 날씨가 풀리더니 이 놈의 '
 '계집애가 미쳤나 하고 의심했습니다. 게다가 조금 뒤에는 제 집께를 할 금할 금 돌아보더니 행주치마의 속으로 꼈던 바른 손을 뽑아서 제 턱 '
 '밑으로 불쑥 내미는 겝니다. 언제 구웠는지 더운 김이 홱 끼치는 굵은 감자 세 개가 손에 뿌듯이 쥐였습니다. "느 집에는 이 거 '
 '없습니까? "하고 생색 있는 큰 소리를 하고는 제가 준 것을 남이 알면은 큰일 날 테니 여기서 얼른 먹어 버리랍니다. 그리고 또 하는 '
 '소리가,"당신 봄 감자가 맛있습니다. ""난 감자 안 먹습니다. 당신이나 먹십시오. "저는 고개도 돌리지 않고 일하던 손으로 그 감자를 '
 '도로 어깨 너머로 쑥 밀어 버렸습니다. 그랬더니 그래도 가는 기색이 없고, 뿐만 아니라 쌔근쌔근하고 심상하지 않게 숨소리가 점점 '
 '거칠어집니다. 이거는 또 뭐야 싶어서 그 때에야 비로소 돌아다보니 저는 참으로 놀랐습니다. 저희가 이 동네에 들어온 것은 근 삼 년째 돼 '
 '오지만 여태껏 가무잡잡한 점수는 이의 얼굴이 이렇게까지 홍당무처럼 새빨개진 법이 없었습니다. 게다가 눈에 독을 올리고 한참 저를 요렇게 '
 '쏘아보더니 나중에는 눈물까지 어리는 게 아닙디다. 그리고 바구니를 다시 집어 들더니 이를 꼭 악물고는 엎어질 듯 자빠질 듯 논둑으로 '
 '횡하게 달아나는 겝니다.')
```

## Hosting the interactive demo 

You can either host the interactive demo locally ([you first have to sign up for papago API to get your secrets](https://developers.naver.com/docs/papago/README.md))
```shell
export NAVER_CLIENT_ID = ...
export NAVER_CLIENT_SECRET = ...
# host the demo via streamlit
streamlit run main_deploy.py
```

Or just visit [the demo we are hosting](https://eubinecto-politely-main-streamlit-4vmces.streamlitapp.com) for you | 
--- |
<img width="743" alt="image" src="https://user-images.githubusercontent.com/56193069/177812857-afa40454-1afd-4b09-873f-aa9db3495d9e.png"> | 


## What Politely can't 🙅

`politely`'s `Styler` cannnot take contexts into account because its conjugation algorithm is fundamentally rule-based. The algorithm is nothing but a chain of glorified if-else's. As a consequence of this, `Styler` can't disambiguate context-dependent conjugations, like so:  

```python3
# 권유 / 청유의 차이는 맥락에 의존
print(styler(["저는 쓰레기를 주워요."], 3))
print(styler(["자, 같이 쓰레기를 주워요."], 3))
```
```
[저는 쓰레기를 줍습니다.]
[자, 같이 쓰레기를 줍습니다.] (should be "자, 같이 쓰레기를 주웁시다")
```
```python3
# 이르 + 어 -> 이르러/일러 또한 맥락에 의존
print(styler(["하지 말라고 일렀다."], 3))
print(styler(["정상에 이르렀다."], 3))
```
```
[하지 말라고 일렀습니다.]
[정상에 일렀습니다.] (should be "정상에 이르렀습니다")
```


## By whom? 👏
- funded by: [Faculty of Oriental Studies](https://www.orinst.ox.ac.uk) at the University of Oxford 
- led & developed by: [Jieun Kiaer](https://www.orinst.ox.ac.uk/people/jieun-kiaer) (Associate Professor of Korean Language and Linguistics at the University of Oxford)
- co-developed by: Research assistant Eu-Bin KIM (Msc. in Applied Linguistics at the University of Oxford, Bsc. in AI at the University of Manchester )


