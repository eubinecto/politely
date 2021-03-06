# Politely

[![PyPI version](https://badge.fury.io/py/politely.svg)](https://badge.fury.io/py/politely)
![Workflow status](https://github.com/eubinecto/politely/actions/workflows/tests.yml/badge.svg)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://eubinecto-politely-main-streamlit-4vmces.streamlitapp.com)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1tpx_wrMmzD_pWeEibeenlU4q8TuKK1j7?usp=sharing)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Feubinecto%2Fpolitely&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
[![Downloads](https://pepy.tech/badge/politely)](https://pepy.tech/project/politely)
[![Downloads](https://pepy.tech/badge/politely/week)](https://pepy.tech/project/politely)

A rule-based politeness styler for the Korean language | 
--- | 
<img width="1010" alt="image" src="https://user-images.githubusercontent.com/56193069/168471756-084409db-5d72-48b7-820f-05e1de6b1f5a.png">  | 



## Quick Start π
### 1οΈβ£ Install `politely`

```python3
pip3 install politely
```

### 2οΈβ£ Split your text into sentences
Split your text into sentences with whatever tools you prefer. Here, we use [`kiwipiepy`](https://github.com/bab2min/kiwipiepy) for the sake of demonstration:
```python3
from kiwipiepy import Kiwi
# an excerpt from λλ°±κ½ (κΉμ μ )
text = """μμλ¦¬λ₯Ό λλ£¨ λμ΄λλ€κ° λ¨μ΄ λ€μκΉλ΄ μμΌλ‘ μμ νμ΄λ§κ³ λ κ·Έ μμμ κΉκΉλλ€. λ³λ‘ μ°μ€μΈ κ²λ μλλ° λ μ¨κ° νλ¦¬λλ μ΄ λμ κ³μ§μ κ° λ―Έμ³€λ νκ³  μμ¬νμλ€.
κ²λ€κ° μ‘°κΈ λ€μλ μ  μ§κ»λ₯Ό ν κΈν κΈ λμλ³΄λλ νμ£ΌμΉλ§μ μμΌλ‘ κΌλ λ°λ₯Έμμ λ½μμ λμ ν±λ°μΌλ‘ λΆμ₯ λ΄λ―Έλ κ²μ΄λ€. 
μΈμ  κ΅¬μ λμ§ λμ΄ κΉμ΄ ν± λΌμΉλ κ΅΅μ κ°μ μΈ κ°κ° μμ λΏλ―μ΄ μ₯μλ€. "λ μ§μ μ΄κ±° μμ§?" νκ³  μμμλ ν°μλ¦¬λ₯Ό νκ³ λ μ κ° μ€ κ²μ λ¨μ΄ μλ©΄μ ν°μΌλ νλ μ¬κΈ°μ μΌλ₯Έ λ¨Ήμ΄ λ²λ¦¬λλ€.
κ·Έλ¦¬κ³  λ νλ μλ¦¬κ°, "λ λ΄κ°μκ° λ§μλ¨λ€." "λ κ°μ μ λ¨Ήλλ€. λλ λ¨Ήμ΄λΌ." λλ κ³ κ°λ λλ¦¬μ§ μκ³  μΌνλ μμΌλ‘ κ·Έ κ°μλ₯Ό λλ‘ μ΄κΉ¨ λλ¨Έλ‘ μ₯ λ°μ΄ λ²λ Έλ€.
κ·Έλ¬λλ κ·Έλλ κ°λ κΈ°μμ΄ μκ³ , λΏλ§ μλλΌ μκ·Όμκ·Όνκ³  μ¬μμΉ μκ² μ¨μλ¦¬κ° μ μ  κ±°μΉ μ΄μ§λ€. μ΄κ±΄ λ λ­μΌ μΆμ΄μ κ·ΈλμμΌ λΉλ‘μ λμλ€λ³΄λ λλ μ°ΈμΌλ‘ λλλ€.
μ°λ¦¬κ° μ΄ λλ€μ λ€μ΄μ¨ κ²μ κ·Ό μΌλμ§Έ λμ΄μ€μ§λ§ μ¬νκ» κ°λ¬΄μ‘μ‘ν μ μμ΄μ μΌκ΅΄μ΄ μ΄λ κ²κΉμ§ νλΉλ¬΄μ²λΌ μλΉ¨κ°μ§ λ²μ΄ μμλ€.
κ²λ€κ° λμ λμ μ¬λ¦¬κ³  νμ°Έ λλ₯Ό μλ κ² μμλ³΄λλ λμ€μλ λλ¬ΌκΉμ§ μ΄λ¦¬λ κ²μ΄ μλλ.
κ·Έλ¦¬κ³  λ°κ΅¬λλ₯Ό λ€μ μ§μ΄λ€λλ μ΄λ₯Ό κΌ­ μλ¬Όκ³ λ μμ΄μ§ λ― μλΉ μ§ λ― λΌλμΌλ‘ ν‘νκ² λ¬μλλ κ²μ΄λ€."""
kiwi = Kiwi()
sents = [sent.text.strip() for sent in kiwi.split_into_sents(text)]
```

### 3οΈβ£ Speak `politely` with `Styler` 

Instantiate an object of `Styler`, and style your sentences in a polite or formal manner with it:

```python3
from politely import Styler
from pprint import pprint
styler = Styler()
pprint(" ".join(styler(sents, 2)))  # 2 = polite
```
```text
('μμλ¦¬λ₯Ό λλ£¨ λμ΄λλ€κ° λ¨μ΄ λ€μκΉ λ΄ μμΌλ‘ μμ νμ΄λ§κ³ λ κ·Έ μμμ κΉκΉλμ. λ³λ‘ μ°μ€μΈ κ²λ μλλ° λ μ¨κ° νλ¦¬λλ μ΄ λμ '
 'κ³μ§μ κ° λ―Έμ³€λ νκ³  μμ¬νμ΄μ. κ²λ€κ° μ‘°κΈ λ€μλ μ  μ§κ»λ₯Ό ν  κΈν  κΈ λμλ³΄λλ νμ£ΌμΉλ§μ μμΌλ‘ κΌλ λ°λ₯Έ μμ λ½μμ μ  ν± '
 'λ°μΌλ‘ λΆμ₯ λ΄λ―Έλ κ²μμ. μΈμ  κ΅¬μ λμ§ λμ΄ κΉμ΄ ν± λΌμΉλ κ΅΅μ κ°μ μΈ κ°κ° μμ λΏλ―μ΄ μ₯μμ΄μ. "λ μ§μλ μ΄ κ±° μμ£ ? '
 '"νκ³  μμ μλ ν° μλ¦¬λ₯Ό νκ³ λ μ κ° μ€ κ²μ λ¨μ΄ μλ©΄μ ν°μΌ λ  νλ μ¬κΈ°μ μΌλ₯Έ λ¨Ήμ΄ λ²λ¦¬λμ. κ·Έλ¦¬κ³  λ νλ μλ¦¬κ°,"λΉμ  '
 'λ΄ κ°μκ° λ§μμ΄μ. ""λ κ°μ μ λ¨Ήμ΄μ. λΉμ μ΄λ λ¨Ήμ΄μ. "μ λ κ³ κ°λ λλ¦¬μ§ μκ³  μΌνλ μμΌλ‘ κ·Έ κ°μλ₯Ό λλ‘ μ΄κΉ¨ λλ¨Έλ‘ μ₯ '
 'λ°μ΄ λ²λ Έμ΄μ. κ·Έλ¬λλ κ·Έλλ κ°λ κΈ°μμ΄ μκ³ , λΏλ§ μλλΌ μκ·Όμκ·Όνκ³  μ¬μνμ§ μκ² μ¨μλ¦¬κ° μ μ  κ±°μΉ μ΄μ Έμ. μ΄κ±°λ λ λ­μΌ '
 'μΆμ΄μ κ·Έ λμμΌ λΉλ‘μ λμλ€λ³΄λ μ λ μ°ΈμΌλ‘ λλμ΄μ. μ ν¬κ° μ΄ λλ€μ λ€μ΄μ¨ κ²μ κ·Ό μΌ λμ§Έ λΌ μ€μ§λ§ μ¬νκ» κ°λ¬΄μ‘μ‘ν μ μλ '
 'μ΄μ μΌκ΅΄μ΄ μ΄λ κ²κΉμ§ νλΉλ¬΄μ²λΌ μλΉ¨κ°μ§ λ²μ΄ μμμ΄μ. κ²λ€κ° λμ λμ μ¬λ¦¬κ³  νμ°Έ μ λ₯Ό μλ κ² μμλ³΄λλ λμ€μλ λλ¬ΌκΉμ§ μ΄λ¦¬λ '
 'κ² μλμ. κ·Έλ¦¬κ³  λ°κ΅¬λλ₯Ό λ€μ μ§μ΄ λ€λλ μ΄λ₯Ό κΌ­ μλ¬Όκ³ λ μμ΄μ§ λ― μλΉ μ§ λ― λΌλμΌλ‘ ν‘νκ² λ¬μλλ κ²μμ.')
 ```
 
 ```python3
 pprint(" ".join(styler(sents, 3)))  # 3 = formal
```
```text
('μμλ¦¬λ₯Ό λλ£¨ λμ΄λλ€κ° λ¨μ΄ λ€μκΉ λ΄ μμΌλ‘ μμ νμ΄λ§κ³ λ κ·Έ μμμ κΉκΉλλλ€. λ³λ‘ μ°μ€μΈ κ²λ μλλ° λ μ¨κ° νλ¦¬λλ μ΄ λμ '
 'κ³μ§μ κ° λ―Έμ³€λ νκ³  μμ¬νμ΅λλ€. κ²λ€κ° μ‘°κΈ λ€μλ μ  μ§κ»λ₯Ό ν  κΈν  κΈ λμλ³΄λλ νμ£ΌμΉλ§μ μμΌλ‘ κΌλ λ°λ₯Έ μμ λ½μμ μ  ν± '
 'λ°μΌλ‘ λΆμ₯ λ΄λ―Έλ κ²λλ€. μΈμ  κ΅¬μ λμ§ λμ΄ κΉμ΄ ν± λΌμΉλ κ΅΅μ κ°μ μΈ κ°κ° μμ λΏλ―μ΄ μ₯μμ΅λλ€. "λ μ§μλ μ΄ κ±° '
 'μμ΅λκΉ? "νκ³  μμ μλ ν° μλ¦¬λ₯Ό νκ³ λ μ κ° μ€ κ²μ λ¨μ΄ μλ©΄μ ν°μΌ λ  νλ μ¬κΈ°μ μΌλ₯Έ λ¨Ήμ΄ λ²λ¦¬λλλ€. κ·Έλ¦¬κ³  λ νλ '
 'μλ¦¬κ°,"λΉμ  λ΄ κ°μκ° λ§μμ΅λλ€. ""λ κ°μ μ λ¨Ήμ΅λλ€. λΉμ μ΄λ λ¨Ήμ­μμ€. "μ λ κ³ κ°λ λλ¦¬μ§ μκ³  μΌνλ μμΌλ‘ κ·Έ κ°μλ₯Ό '
 'λλ‘ μ΄κΉ¨ λλ¨Έλ‘ μ₯ λ°μ΄ λ²λ Έμ΅λλ€. κ·Έλ¬λλ κ·Έλλ κ°λ κΈ°μμ΄ μκ³ , λΏλ§ μλλΌ μκ·Όμκ·Όνκ³  μ¬μνμ§ μκ² μ¨μλ¦¬κ° μ μ  '
 'κ±°μΉ μ΄μ§λλ€. μ΄κ±°λ λ λ­μΌ μΆμ΄μ κ·Έ λμμΌ λΉλ‘μ λμλ€λ³΄λ μ λ μ°ΈμΌλ‘ λλμ΅λλ€. μ ν¬κ° μ΄ λλ€μ λ€μ΄μ¨ κ²μ κ·Ό μΌ λμ§Έ λΌ '
 'μ€μ§λ§ μ¬νκ» κ°λ¬΄μ‘μ‘ν μ μλ μ΄μ μΌκ΅΄μ΄ μ΄λ κ²κΉμ§ νλΉλ¬΄μ²λΌ μλΉ¨κ°μ§ λ²μ΄ μμμ΅λλ€. κ²λ€κ° λμ λμ μ¬λ¦¬κ³  νμ°Έ μ λ₯Ό μλ κ² '
 'μμλ³΄λλ λμ€μλ λλ¬ΌκΉμ§ μ΄λ¦¬λ κ² μλλλ€. κ·Έλ¦¬κ³  λ°κ΅¬λλ₯Ό λ€μ μ§μ΄ λ€λλ μ΄λ₯Ό κΌ­ μλ¬Όκ³ λ μμ΄μ§ λ― μλΉ μ§ λ― λΌλμΌλ‘ '
 'ν‘νκ² λ¬μλλ κ²λλ€.')
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


## What `politely` can't π

`politely`'s `Styler` cannnot take contexts into account because its conjugation algorithm is fundamentally rule-based. The algorithm is nothing but a chain of glorified if-else's. As a consequence of this, `Styler` can't disambiguate context-dependent conjugations, like so:  

```python3
# κΆμ  / μ²­μ μ μ°¨μ΄λ λ§₯λ½μ μμ‘΄
print(styler(["μ λ μ°λ κΈ°λ₯Ό μ£Όμμ."], 3))
print(styler(["μ, κ°μ΄ μ°λ κΈ°λ₯Ό μ£Όμμ."], 3))
```
```
[μ λ μ°λ κΈ°λ₯Ό μ€μ΅λλ€.]
[μ, κ°μ΄ μ°λ κΈ°λ₯Ό μ€μ΅λλ€.] (should be "μ, κ°μ΄ μ°λ κΈ°λ₯Ό μ£Όμμλ€")
```
```python3
# μ΄λ₯΄ + μ΄ -> μ΄λ₯΄λ¬/μΌλ¬ λν λ§₯λ½μ μμ‘΄
print(styler(["νμ§ λ§λΌκ³  μΌλ λ€."], 3))
print(styler(["μ μμ μ΄λ₯΄λ λ€."], 3))
```
```
[νμ§ λ§λΌκ³  μΌλ μ΅λλ€.]
[μ μμ μΌλ μ΅λλ€.] (should be "μ μμ μ΄λ₯΄λ μ΅λλ€")
```


## By whom? π
- funded by: [Faculty of Oriental Studies](https://www.orinst.ox.ac.uk) at the University of Oxford 
- led & developed by: [Jieun Kiaer](https://www.orinst.ox.ac.uk/people/jieun-kiaer) (Associate Professor of Korean Language and Linguistics at the University of Oxford)
- co-developed by: Research assistant Eu-Bin KIM (Msc. in Applied Linguistics at the University of Oxford, Bsc. in AI at the University of Manchester )


