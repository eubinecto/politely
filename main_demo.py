from pprint import pprint

from politely import Styler

SENTS = [
    # ㅂ 불규칙
    "영희가 철수를 도왔어",
    "저 집은 매일 고기를 구워",
    "미희는 옷을 잘 기워",
    "밥 먹고 누우면 안 된대",
    "오다 주웠어",
    "고운 손이 다 망가졌네",
    "오늘이 어제보다 더워",
    "이 라면은 너무 매워",
    "이 라면은 너무 맵다",
    "올해는 유난히 추워",
    "오늘은 꿈자리가 사나웠어",
    "난 뱀이 무서워",
    "겨울산은 아름다워",
    "키가 큰 사람은 부러워",
    # ㄷ 불규칙
    "가까우니까 걸어가자",
    "난 걸어 갈게",
    "그걸 이제야 깨달았어",
    "나는 그 문을 닫았어",
    "선생님 밥 먹어",
    "자 떠나자. 동해 바다로",
    "그는 전설이다",
    "그는 전설이에요",
    "나는 내 꿈을 향해 달려",
]

styler = Styler()


for sent in SENTS:
    ban = styler(sent, 1)
    jon = styler(sent, 2)
    formal = styler(sent, 3)
    print(sent, "->", ban, "|", jon, "|", formal)
