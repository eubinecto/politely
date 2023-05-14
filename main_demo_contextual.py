from politely import Styler

styler = Styler(lm_search=False)  # lm_search 기능 추가
print("##### lm을 쓰지 않는 경우 맥락 고려 X ######")
print(styler("난 밥을 먹어요.", 2))
print(styler("자, 이제 먹어요.", 2))

styler = Styler(lm_search=True)  # lm_search 기능 추가
print("##### lm을 쓰는 경우 맥락 고려 O ######")
print(styler("난 밥을 먹어요.", 2))
print(styler("자, 이제 먹어요.", 2))


"""
##### lm을 쓰지 않는 경우 맥락 고려 X ######
전 밥을 먹습니다.
자, 이제 먹습니다.
##### lm을 쓰는 경우 맥락 고려 O ######
전 밥을 먹습니다.
자, 이제 먹읍시다.
"""