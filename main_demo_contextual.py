from politely import Styler

styler = Styler(lm_search=True)  # lm_search 기능 추가
print("##### 맥락 고려 예시 1) - 쳥유 ######")
print(styler("자, 이제 먹어요.", 2))
print(styler("난 밥을 먹어요.", 2))
