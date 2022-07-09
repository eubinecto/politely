from copy import copy
from pprint import pprint
import re
from typing import List, Tuple

import yaml
from kiwipiepy import Kiwi

HONORIFICS_YAML = """
# 1st-order rules (1-morpheme-pattern)
\+(?P<tgt>[^\s+]+/EF):
  - [어/EF, 다/EF, 자/EF]
  - [어요/EF, 죠/EF, 래요/EF, 네요/EF]
  - [ᆸ니다/EF, ᆸ시다/EF, 읍시다/EF, 습니까/EF, ᆸ시오]  # "어"만 있을 땐, 의문형, 평서형 전부 가능 
\+(?P<tgt>어/EF):
  - [어/EF]
  - [어요/EF, 죠/EF]  # 네요?는 포함 x
  - [ᆸ니다/EF, 습니까/EF]  # "어"만 있을 땐, 의문형, 평서형 전부 가능  
\+(?P<tgt>자/EF):
  - [자/EF]
  - [어요/EF, 죠/EF]
  - [ᆸ니다/EF, ᆸ시다/EF]  # "어"만 있을 땐, 의문형, 평서형 전부 가능  
\+(?P<tgt>읍시다/EF):
  - [어/EF, 자/EF]
  - [어요/EF, 죠/EF]
  - [읍시다/EF]  # "어"만 있을 땐, 의문형, 평서형 전부 가능  
\+(?P<tgt>다/EF):
  - [다/EF]
  - [어요/EF, 네요/EF]
  - [ᆸ니다/EF]  # -다로 끝나는 경우, 청유는 없음.
\+(?P<tgt>ᆸ니다/EF):
  - [다/EF]
  - [어요/EF, 네요/EF]
  - [ᆸ니다/EF]  # -ㅂ니다로 끝나는 경우에도, 청유는 없음.
(^|.*\+)(?P<tgt>(나|저)/NP)(\+.*|$):
  - [나/NP]
  - [저/NP]
  - [저/NP]
# 2nd-order rules (2-morpheme-pattern)  
\+(?P<tgt>[^\s+]+/EF)\+\?/SF:   # use match & extract
  - \+(?P<tgt>[^\s+]+/EF)  # you can use other keys to use the same pattern
  - \+(?P<tgt>[^\s+]+/EF)
  - [습니까/EF]  # ?로 끝나는 경우, 의문형만 가능
\+(?P<tgt>[^\s+]+/EF)\+[.!]/SF:
  - \+(?P<tgt>[^\s+]+/EF)
  - \+(?P<tgt>[^\s+]+/EF)
  - [ᆸ니다/EF, ᆸ시다/EF]  # . 로 끝나는 경우, 평서형만 가능
# if you are not using any wildcards, be specific with your candidates
\+이/VCP\+(?P<tgt>(어|다)/EF):
  - [어/EF, 다/EF]
  - [에요/EF, 죠/EF]
  - [ᆸ니다/EF]  #   "입시다" 따윈 없으므로 , 오직 ㅂ니다만 가능.
"""


def fetch_honorifics() -> dict:
    honorifics = yaml.safe_load(HONORIFICS_YAML.strip())
    for key, val in honorifics.items():
        for idx, candidates in enumerate(val):
            if isinstance(candidates, str):
                honorifics[key][idx] = honorifics[candidates][idx]
    return honorifics


HONORIFICS = fetch_honorifics()
BANS = {
    morpheme
    for val in HONORIFICS.values()
    for morpheme in val[0]
}
JONS = {
    morpheme
    for val in HONORIFICS.values()
    for morpheme in val[1]
}
FORMALS = {
    morpheme
    for val in HONORIFICS.values()
    for morpheme in val[2]
}
kiwi = Kiwi()


def honorify(sent: str, politeness: int) -> Tuple[str, list]:
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
    possible = {}
    joined = "+".join(morphemes)
    for pattern in HONORIFICS.keys():
        regex = re.compile(pattern)
        if regex.search(joined):
            key = regex.search(joined).group('tgt')
            honorifics = set(HONORIFICS[pattern][politeness])
            possible[key] = possible.get(key, honorifics) & honorifics
    # should think of the combinations of multiple possible, though. (e.g. 나 -> 저 && 종결어미)
    # what you need is ... applying different keys at the same time -> but how? how do we do this?
    candidates = [
        possible.get(morpheme, morpheme)
        for morpheme in morphemes
    ]
    out = kiwi.join(
        [
            # for now, we use random pop.
            tuple(list(candidate)[0].split("/"))if isinstance(candidate, set) else tuple(candidate.split("/"))
            for candidate in candidates
        ]
    )
    return out, candidates


sent = "잘 했어."
print(f"honorifying: {sent}")
print(honorify(sent, 0))
print(honorify(sent, 1))
print(honorify(sent, 2))
print("---")
sent = "잘 했어?"
print(f"honorifying: {sent}")
print(honorify(sent, 0))
print(honorify(sent, 1))
print(honorify(sent, 2))
print("---")
sent = "아 배고프다."
print(f"honorifying: {sent}")
print(honorify(sent, 0))
print(honorify(sent, 1))
print(honorify(sent, 2))
print("---")
sent = "아 배고픕니다."
print(f"honorifying: {sent}")
print(honorify(sent, 0))
print(honorify(sent, 1))
print(honorify(sent, 2))
print("---")
sent = "자, 쓰레기를 줍자."
print(f"honorifying: {sent}")
print(honorify(sent, 0))
print(honorify(sent, 1))
print(honorify(sent, 2))
print("---")
sent = "자, 쓰레기를 주웁시다."
print(f"honorifying: {sent}")
print(honorify(sent, 0))
print(honorify(sent, 1))
print(honorify(sent, 2))
print("---")

# 어요 -> 자 or 다 is completely dependent on the context.
# 배고프 + 어요 -> 배고프다.
# 하 + 어요 -> 하자 / 해)
# this is why we need a language model, if we were to pull this off.
# okay. Let's do this after you finish your dissertation.
sent = "저는 배고파요."
print(f"honorifying: {sent}")
print(honorify(sent, 0))
print(honorify(sent, 1))
print(honorify(sent, 2))
print("---")
sent = "그냥 지금 시작해요."
print(f"honorifying: {sent}")
print(honorify(sent, 0))
print(honorify(sent, 1))
print(honorify(sent, 2))