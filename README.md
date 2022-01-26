# Politetune (demo)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/eubinecto/politetune/main/main.py)


Project Politetune is a rule-based (well, for the time being) politeness tuner that is designed to help L2 learners of Korean in learning when to use Jondaemal(존댓말) and when to use Banmal(반말). 

## By Whom?
- funded by: [Faculty of Oriental Studies](https://www.orinst.ox.ac.uk) at the University of Oxford 
- led & developed by: [Jieun Kiaer](https://www.orinst.ox.ac.uk/people/jieun-kiaer) (Associate Professor of Korean Language and Linguistics at the University of Oxford)
- co-developed by: Research assistant Eu-Bin KIM (Msc. in Applied Linguistics at the University of Oxford, Bsc. in AI at the University of Manchester )


## The Plan

1. Get a cup of coffee and sit down
2. The results should be **explainable**, so start with a rule-based system.
3. Design a rule-based version of Politetune by the end of Feburary 2022, somthing akin to [wordtune](https://www.wordtune.com)
4. Think of how you could apply prediction-based Language Models to better politetune sentences.


## The Algorithm

### Who could be your listener?
- Teacher
- Boss at work 
- Older sister
- Older brother
- Older cousin
- Younger sister
- Younger brother 
- Younger cousin 
- Uncle
- Friend (same age)
- Grandpa
- Grandma
- Mum
- Dad
- Shop clerk 

### Where could you be speaking in?
- Private space like home 
- Public space where others are around  

### You are speaking to X in a private space
- Teacher  (POLITE)
- Boss at work (POLITE)
- Older sister (non-POLITE)
- Older brother (non-POLITE)
- Older cousin (non-POLITE)
- Younger sister (non-POLITE)
- Younger brother (non-POLITE)
- Younger cousin (non-POLITE)
- Uncle (POLITE)
- Friend (same age) (non-POLITE)
- Grandpa (POLITE)
- Grandma (POLITE)
- Mum (non-POLITE)
- Dad (POLITE)
- Shop clerk (POLITE)

### You are speaking to X in a public space
- Teacher  (POLITE)
- Boss at work (POLITE)
- Older sister (non-POLITE)
- Older brother (non-POLITE)
- Older cousin (non-POLITE)
- Younger sister(non-POLITE)
- Younger brother (non-POLITE)
- Younger cousin (non-POLITE)
- Uncle (POLITE)
- Friend (same age) (POLITE)
- Grandpa (POLITE)
- Grandma (POLITE)
- Mum (POLITE)
- Dad (POLITE)
- Shop clerk (POLITE)


### How do you politetune verbs?

Verbs	| Polite |	Non-polite
--- | --- | --- 
좋아하다	| 좋아해요 | 	좋아해
싫어하다	| 싫어해요 | 	싫어해
미안하다 | 	미안해요 | 	미안해
쇼핑하다	| 쇼핑해요 | 	쇼핑해
공부하다	| 공부해요 | 	공부해
마시다 	| 마셔요 | 	마셔
알다	| 알아요 | 	알아
모르다	| 몰라요 | 	몰라
듣다	| 들어요 | 	들어
사다	| 사요 | 	사
보다	| 봐요 | 	봐
가다	| 가요 | 	가
오다	| 와요 | 	와
아프다	| 아파요 | 	아파
목마르다	| 목말라요 | 	목말라
배고프다	| 배고파요 | 	배고파
고맙다	| 고마워요 | 	고마워

| row1 | row2 |



## Goals

```text
마시다 -> 나는 물을 마셔요 / 나는 물을 마셔
공부하다 -> 나는 공부해요 -> 나는 공부해
가다 -> 가요 -> 가
오다 ->  
```
