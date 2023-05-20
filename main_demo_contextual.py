from politely import Styler

styler = Styler(lm_search=False)  # lm_search 기능 추가
print("##### lm을 쓰지 않는 경우 맥락 고려 X ######")
print(styler("내일 같이 점심 먹어요.", 0))

styler = Styler(lm_search=True)  # lm_search 기능 추가
print("##### lm을 쓰는 경우 맥락 고려 O ######")
print(styler("내일 같이 점심 먹어요.", 0))


"""
styler = Styler(lm_search=False)  # lm_search 기능 추가
print("##### lm을 쓰지 않는 경우 맥락 고려 X ######")
print(styler("내일 같이 점심 먹어요.", 0))

styler = Styler(lm_search=True)  # lm_search 기능 추가
print("##### lm을 쓰는 경우 맥락 고려 O ######")
print(styler("내일 같이 점심 먹어요.", 0))
"""