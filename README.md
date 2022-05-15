# Politely

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://eubinecto-politely.herokuapp.com)

Politely is a rule-based politeness styler for Korean | 
--- | 
<img width="1010" alt="image" src="https://user-images.githubusercontent.com/56193069/168471756-084409db-5d72-48b7-820f-05e1de6b1f5a.png"> | 


## Quick Start 🚀
### setup `politely`
```
# install politely
!pip3 install git+https://github.com/eubinecto/politely.git@v2.6

# install khaiii (politely heavily relies on khaiii to anaylze endings)
!git clone https://github.com/kakao/khaiii.git
!mkdir khaiii/build
!cmake khaiii
!make package_python
!pip3 install package_python/.
```

### use the `Styler` to speak politely 👏

```python3
from politely.processors import Styler
styler = Styler()
print(styler("난 내 목표를 향해 달려.", 2))  # casual -> polite
print(styler("난 내 목표를 향해 달려.", 3))  # casual -> formal
print(styler("전 제 목표를 향해 달려요.", 1))  # polite -> casual
print(styler("전 제 목표를 향해 달려요.", 3))  # polite -> formal
```
```
# add the examples here
...
```

### Hosting the interactive demo locally

You can either host the interactive demo locally:
```shell
# get your api tokens for using papago API from: https://developers.naver.com/docs/papago/README.md
export NAVER_CLIENT_ID = ...
export NAVER_CLIENT_SECRET = ...
# host an interactive demo locally
streamlit run main_deploy.py
```
Or just visit [the demo that we have deployed on the web](https://eubinecto-politely.herokuapp.com) for you.


## What Politely cannot do 🙅




## By whom? 👏
- funded by: [Faculty of Oriental Studies](https://www.orinst.ox.ac.uk) at the University of Oxford 
- led & developed by: [Jieun Kiaer](https://www.orinst.ox.ac.uk/people/jieun-kiaer) (Associate Professor of Korean Language and Linguistics at the University of Oxford)
- co-developed by: Research assistant Eu-Bin KIM (Msc. in Applied Linguistics at the University of Oxford, Bsc. in AI at the University of Manchester )


