from politely import Styler
from politely.modeling_gpt2_scorer import GPT2Scorer
from politely.modeling_heuristic_scorer import HeuristicScorer

styler = Styler(scorer=HeuristicScorer())
print("##### lm을 쓰지 않는 경우 맥락 고려 X ######")
print(styler("내일 저랑 같이 점심 먹어요.", 0))

styler = Styler(scorer=GPT2Scorer())  # uses GPT2Scorer by default
print("##### lm을 쓰는 경우 맥락 고려 O ######")
print(styler("내일 저랑 같이 점심 먹어요.", 0))


"""
##### lm을 쓰지 않는 경우 맥락 고려 X ######
내일 나랑 같이 점심 먹어.
##### lm을 쓰는 경우 맥락 고려 O ######
내일 나랑 같이 점심 먹자.
"""