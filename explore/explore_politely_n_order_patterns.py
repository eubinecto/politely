"""
Solving cloze-task with rules (regular expressions).
"""
import re
from typing import Tuple
import yaml
from kiwipiepy import Kiwi

DLM = "⊕"
ALL_MASK = rf"{DLM}(?P<mask>[^\s{DLM}]+/EF)"
ALL_UNMASK = ALL_MASK.replace("?P<mask>", "")

RULES_YML = f"""
# --- 1st-order rules (1-morpheme-pattern) --- #
{ALL_MASK}:
  - [어/EF, 다/EF, 자/EF, ᆫ다/EF, 는다/EF, 마/EF, ᆯ게/EF, ᆫ대/EF, 야/EF, 군/EF, 네/EF]
  - [어요/EF, 에요/EF, 죠/EF, 래요/EF, 네요/EF, 란다/EF, ᆯ게요/EF, ᆫ대요/EF, ᆫ가요/EF]
  - [ᆸ니다/EF, ᆸ시다/EF, 읍시다/EF, 습니까/EF, 십시오/EF, ᆸ시오/EF]  # "어"만 있을 땐, 의문형, 평서형 전부 가능 
{DLM}(?P<mask>자/EF):
  - [자/EF]
  - [어요/EF, 죠/EF]
  - [ᆸ니다/EF, ᆸ시다/EF]  # "어"만 있을 땐, 의문형, 평서형 전부 가능  
{DLM}(?P<mask>읍시다/EF):
  - [어/EF, 자/EF]
  - [어요/EF, 죠/EF]
  - [읍시다/EF]  # "어"만 있을 땐, 의문형, 평서형 전부 가능  
{DLM}(?P<mask>(다|ᆸ니다)/EF):
  - [다/EF]
  - [어요/EF, 네요/EF, 네요/EF, 에요/EF, 죠/EF]
  - [ᆸ니다/EF]  # -다로 끝나는 경우, 청유는 없음.
(^|.*{DLM})(?P<mask>(나|저)/NP)({DLM}.*|$):
  - [나/NP]
  - [저/NP]
  - [저/NP]
  
# --- 2nd-order rules (2-morpheme-pattern) --- #  
{ALL_MASK}{DLM}\?/SF: # use match & extract
  - {ALL_MASK}  # you can use other keys to use the same pattern
  - {ALL_MASK}
  - [습니까/EF]  # ?로 끝나는 경우, 의문형만 가능
{ALL_MASK}{DLM}[.!]/SF:
  - {ALL_MASK}
  - {ALL_MASK}
  - [ᆸ니다/EF, ᆸ시다/EF, 십시오/EF, ᆸ시오/EF]  # . 로 끝나는 경우, 평서형만 가능
# if you are not using any wildcards, be specific with your candidates
{DLM}이/VCP{DLM}(?P<mask>(어|다|야|군|에요|죠|ᆸ니다)/EF):
  - [어/EF, 다/EF, 야/EF, 군/EF]
  - [에요/EF, 죠/EF]
  - [ᆸ니다/EF]  #   "입시다" 따윈 없으므로 , 오직 ㅂ니다만 가능.
{DLM}말/VX{DLM}(?P<mask>(어|어요|십시오)/EF):
  - [어/EF]
  - [어요/EF]
  - [십시오/EF]
{DLM}시/EP{DLM}(?P<mask>(어|어요|ᆸ시오)/EF):
  - [어/EF]
  - [어요/EF]
  - [ᆸ시오/EF]
{DLM}(?P<mask>시/EP){ALL_UNMASK}:
  - []  # remove 시
  - [시/EP]
  - [시/EP]
# 3rd-order rules 
{DLM}배고프/VA{DLM}(?P<mask>(다|어|어요|네요|ᆸ니다)/EF){DLM}[.!]/SF:
  - [다/EF, 어/EF]
  - [어요/EF, 네요/EF]
  - [ᆸ니다/EF]
{DLM}배고프/VA{DLM}(?P<mask>(어|어요|죠|ᆫ가요|습니까)/EF){DLM}\?/SF:
  - [어/EF]
  - [어요/EF, 죠/EF, ᆫ가요/EF]
  - [습니까/EF]
"""


def fetch_rules() -> dict:
    honorifics = yaml.safe_load(RULES_YML.strip())
    for key, val in honorifics.items():
        for idx, candidates in enumerate(val):
            if isinstance(candidates, str):
                honorifics[key][idx] = honorifics[candidates][idx]
    return honorifics


RULES = fetch_rules()
BANS, JONS, FORMALS = RULES[ALL_MASK][0], RULES[ALL_MASK][1], RULES[ALL_MASK][2]
kiwi = Kiwi()


def style(sent: str, politeness: int) -> Tuple[str, list]:
    morphemes = [token.tagged_form for token in kiwi.tokenize(sent)]
    # check the formality of the sentence
    ef = [morph for morph in morphemes if morph.endswith("EF")][0]
    if ef in BANS:
        formality = 0
    elif ef in JONS:
        formality = 1
    elif ef in FORMALS:
        formality = 2
    else:
        raise ValueError(f"Unknown formality: {ef}")
    if formality == politeness:
        # just return it as-is.
        return sent, morphemes
    possibilities = {}
    joined = DLM.join(morphemes)
    for pattern in RULES.keys():
        regex = re.compile(pattern)
        if regex.search(joined):
            key = regex.search(joined).group('mask')
            honorifics = set(RULES[pattern][politeness])
            possibilities[key] = possibilities.get(key, honorifics) & honorifics
            # print(pattern, "->", possibilities)
    # should think of the combinations of multiple possibilities, though. (e.g. 나 -> 저 && 종결어미)
    # what you need is ... applying different keys at the same time -> but how? how do we do this?
    candidates = [
        possibilities.get(morpheme, morpheme)
        for morpheme in morphemes
    ]
    out = kiwi.join(
        [
            # for now, we use random pop.
            tuple(list(candidate)[0].split("/")) if isinstance(candidate, set)
            else tuple(candidate.split("/"))
            for candidate in candidates
            if candidate
        ]
    )
    return out, candidates


sent = "잘 했어."
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))
print("---")
sent = "잘 했어?"
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))
print("---")
sent = "아 배고프다."
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))
print("---")
sent = "아 배고픕니다."
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))
print("---")
sent = "자, 쓰레기를 줍자."
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))
print("---")
sent = "자, 쓰레기를 주웁시다."
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))
print("---")

# 어요 -> 자 or 다 is completely dependent on the context.
# 배고프 + 어요 -> 배고프다.
# 하 + 어요 -> 하자 / 해)
# this is why we need a language model, if we were to pull this off.
# okay. Let's do this after you finish your dissertation.
sent = "저는 배고파요."
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))
print("---")
sent = "지금 많이 배고파?"
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))
print("---")
sent = "그냥 지금 시작해요."
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))

print("---")
sent = "이건 흥미롭군."
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))


print("---")
sent = "그건 이 나라의 보물이다."
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))

print("---")
sent = "그렇게 하지마."
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))

print("---")
sent = "그렇게 하지마세요."  # removal of 시/EF is also possible
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))
print("---")
sent = "그렇게 하지마십시오."  # removal of 시/EF is also possible
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))
print("---")
sent = "지금 많이 배고프시죠?"  # removal of 시/EF is also possible
print(f"honorifying: {sent}")
print(style(sent, 0))
print(style(sent, 1))
print(style(sent, 2))