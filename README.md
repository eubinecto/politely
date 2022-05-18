# Politely

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://eubinecto-politely.herokuapp.com)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1W79NzS7xU4VS2HxAKjDB_QwsZp6e2jKu?usp=sharing)


Politely is an explainable politeness styler for the Korean language (work in progress) | 
--- | 
<img width="1010" alt="image" src="https://user-images.githubusercontent.com/56193069/168471756-084409db-5d72-48b7-820f-05e1de6b1f5a.png"> | 


## Quick Start 🚀
### 1️⃣ setup `politely`

Install `politely` directly from github
```
pip3 install git+https://github.com/eubinecto/politely.git@v2.6
```
`politely` heavily relies on `khaiii` for morpheme analysis. Install `khaiii`, as instructed in [the official document](https://github.com/kakao/khaiii/wiki/빌드-및-설치)
```
git clone https://github.com/kakao/khaiii.git
mkdir khaiii/build
cmake khaiii
make package_python
pip3 install package_python/.
```

### 2️⃣ Speak `politely` with `Styler`

```python3
from politely.styler import Styler

styler = Styler()
print(styler("난 내 목표를 향해 달려.", 2))  # casual -> polite
print(styler("난 내 목표를 향해 달려.", 3))  # casual -> formal
print(styler("전 제 목표를 향해 달려요.", 1))  # polite -> casual
print(styler("전 제 목표를 향해 달려요.", 3))  # polite -> formal
```
```
전 제 목표를 향해 달려요.
전 제 목표를 향해 달립니다.
난 내 목표를 향해 달려.
전 제 목표를 향해 달립니다.
```
```python3
print(styler("오늘이 어제보다 더워.", 2))  # casual -> polite
print(styler("오늘이 어제보다 더워.", 3))  # casual -> formal
print(styler("오늘이 어제보다 더워요.", 1))  # polite -> casual 
print(styler("오늘이 어제보다 더워요.", 3))  # polite -> formal
```
```
오늘이 어제보다 더워요.
오늘이 어제보다 덥습니다.
오늘이 어제보다 더워.
오늘이 어제보다 덥습니다.
```

## Coverage 📈

We have test-covered, and will test-cover, the following cases. Please feel free to contribute if you feel like you could cover more of these cases.

 - [X] -ㄴ대요
 - [X] -게
 - [X] -어
 - [X] -이야
 - [X] -마
 - [X] -봐
 - [X] -대?
 - [X] -어?
 - [X] -시어?
 - [X] -때?
 - [X] 동모음 탈락
 - [X] ㄷ 불규칙
 - [X] ㅅ 불규칙
 - [X] ㅎ 불규칙
 - [X] 오 불규칙
 - [X] 가라 불규칙
 - [X] 너라 불규칙
 - [ ] 으 불규칙
 - [ ] 르 불규칙
 - [ ] 우 불규칙
 - [ ] ㅂ 불규칙
 - [ ] ... (more to be added)
## Hosting the interactive demo 

You can either host the interactive demo locally ([you first have to sign up for papago API to get your secrets](https://developers.naver.com/docs/papago/README.md))
```shell
export NAVER_CLIENT_ID = ...
export NAVER_CLIENT_SECRET = ...
# host the demo via streamlit
streamlit run main_deploy.py
```

Or just visit [the demo we are hosting](https://eubinecto-politely.herokuapp.com) for you | 
--- |
<img width="749" alt="image" src="https://user-images.githubusercontent.com/56193069/168508652-687acb98-0bf6-4834-b56c-74d236bee031.png"> | 


## What Politely can't 🙅

`politely`'s `Styler` cannnot take contexts into account because its conjugation algorithm is fundamentally rule-based. The algorithm is nothing but a chain of glorified if-else's. As a consequence of this, `Styler` can't disambiguate context-dependent conjugations, like s:  

```python3
print(styler("저는 쓰레기를 주워요.", 3))
print(styler("자, 같이 쓰레기를 주워요.", 3))
```
```
저는 쓰레기를 줍습니다.
자, 같이 쓰레기를 줍습니다. (should be "자, 같이 쓰레기를 주웁시다")
```


## By whom? 👏
- funded by: [Faculty of Oriental Studies](https://www.orinst.ox.ac.uk) at the University of Oxford 
- led & developed by: [Jieun Kiaer](https://www.orinst.ox.ac.uk/people/jieun-kiaer) (Associate Professor of Korean Language and Linguistics at the University of Oxford)
- co-developed by: Research assistant Eu-Bin KIM (Msc. in Applied Linguistics at the University of Oxford, Bsc. in AI at the University of Manchester )


