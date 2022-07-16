"""
Some philosophies to follow:
1. Rules account for 70% of the solution. Strive to hard-code the rules with intuitions and sweat. Keep the rules as general as possible.
2. The remaining 30% is based on the context. Don't use rules for that. It may be effective but it's inefficient (you won't get much from specific rules).
 Disambiguate contexts with masked language models (e.g. Word2Vec, BERT, etc).
3. Every new feature must be tested. If writing Unit tests are not viable, then try to write a small demo.

---
Research Proposal:
RegexBERT - Fine-tuning BERT with Regex-guided Masked Language Modelingd
---
너무나도 obvious한건 정규표현식으로 처리.
나머지 애매모호한 규칙은 BERT에게 맡긴다.
---
20번까지는 공식대로 푼다.
21번과 31번은 머리를 써서 푼다.
"""
# The symbol to use for separating tags from texts
from typing import Dict, Tuple, List
import re
from kiwipiepy import Kiwi

TAG = "⌇"
# The symbol to use for separating taggd tokens from another tagged tokens
SEP = "⊕"
# The wild cards
ALL = rf"([^\s{SEP}]+{TAG}EF)"
# https://www.pythontutorial.net/python-regex/python-regex-non-capturing-group/
ALL_NO_CAPTURE = rf"(?:[^\s{SEP}]+{TAG}EF)"
kiwi = Kiwi()

# --- all EF's for different styles of politeness --- #
CASUAL = {
    f"어{TAG}EF",
    f"다{TAG}EF",
    f"자{TAG}EF",
    f"ᆫ다{TAG}EF",
    f"는다{TAG}EF",
    f"마{TAG}EF",
    f"ᆯ게{TAG}EF",
    f"ᆫ대{TAG}EF",
    f"야{TAG}EF",
    f"군{TAG}EF",
    f"네{TAG}EF",
}
POLITE = {
    f"어요{TAG}EF",
    f"에요{TAG}EF",
    f"죠{TAG}EF",
    f"래요{TAG}EF",
    f"네요{TAG}EF",
    f"ᆯ게요{TAG}EF",
    f"ᆫ대요{TAG}EF",
    f"ᆫ가요{TAG}EF",
    f"나요{TAG}EF",
}
FORMAL = {
    f"ᆸ니다{TAG}EF",
    f"ᆸ시다{TAG}EF",
    f"습니까{TAG}EF",
    f"ᆸ니까{TAG}EF",
    f"십시오{TAG}EF",
    f"ᆸ시오{TAG}EF",
}

# --- any EF's --- #
RULES: Dict[str, Tuple[List[set], List[set], List[set]]] = {ALL: ([CASUAL], [POLITE], [FORMAL])}

# --- 자/EF --- #
RULES.update(
    {
        rf"(자{TAG}EF)": (
            [{f"자{TAG}EF"}],
            [{f"어요{TAG}EF", f"죠{TAG}EF"}],
            [RULES[ALL][2][0] - {f"ᆸ니다{TAG}EF", f"습니까{TAG}EF"}],
        )
    }
)

# --- 군/EF --- #
RULES.update(
    {
        rf"(군{TAG}EF)": (
            [{f"군{TAG}EF"}],
            [{f"어요{TAG}EF", f"네요{TAG}EF"}],
            [{f"ᆸ니다{TAG}EF"}],
        )
    }
)

# --- 나 or 저 --- #
RULES.update(
    {
        rf"((?:나|저){TAG}NP)": (
            [{f"나{TAG}NP"}],
            [{f"저{TAG}NP"}],
            [{f"저{TAG}NP"}],
        )
    }
)

# --- 너 or 당신 --- #
RULES.update(
    {
        rf"((?:너|당신){TAG}NP)": (
            [{f"너{TAG}NP"}],
            [{f"당신{TAG}NP"}],
            [{f"당신{TAG}NP"}],
        )
    }
)

# --- 너 or 당신 + ㄹ --- #
RULES.update(
    {
        rf"(?:너|당신){TAG}NP{SEP}(ᆯ{TAG}JKO)": (
            [{f"ᆯ{TAG}JKO"}],
            [{f"을{TAG}JKO"}],
            [{f"을{TAG}JKO"}],
        )
    }
)

# --- 시/EP + all/EF --- #
RULES.update(
    {
        rf"시{TAG}EP{SEP}{ALL}": (
            RULES[ALL][0],
            [RULES[ALL][1][0] - {f"에요{TAG}EF", f"네요{TAG}EF"}],
            # ㅅ is redundant
            [RULES[ALL][2][0]
             - {
                 f"습니까{TAG}EF",
                 f"십시오{TAG}EF",
                 f"ᆸ시다{TAG}EF",
             }],
        )
    }
)

# --- 시/EP --- #
RULES.update(
    {
        rf"(시{TAG}EP){SEP}{ALL_NO_CAPTURE}": (
            [set()],  # don't use 시/EP if politeness = 0. NOTE -you can delete a token this way, but you can't add one.
            [{f"시{TAG}EP"}],
            [{f"시{TAG}EP"}],
        )
    }
)

# --- ends with ?/SF --- #
RULES.update(
    {
        rf"{ALL}{SEP}\?{TAG}SF": (
            RULES[ALL][0],
            [RULES[ALL][1][0] - {f"네요{TAG}EF", f"ᆯ게요{TAG}EF"}],
            [{f"습니까{TAG}EF", f"ᆸ니까{TAG}EF"}],  # nothing but 습니까 is allowed
        )
    }
)

# --- ends with ./SF, !/SF --- #
RULES.update(
    {
        rf"{ALL}{SEP}[.!]{TAG}SF": (
            RULES[ALL][0],
            RULES[ALL][1],
            [RULES[ALL][2][0]
             - {f"습니까{TAG}EF", f"ᆸ니까{TAG}EF"}],  # anything but 습니까 is allowed
        )
    }
)

# ---- 이/VCP + EFs --- #
RULES.update(
    {
        rf"이{TAG}VCP{SEP}{ALL}": (
            [{f"어{TAG}EF", f"다{TAG}EF", f"야{TAG}EF", f"군{TAG}EF"}],
            [{f"에요{TAG}EF", f"죠{TAG}EF"}],
            [{f"ᆸ니다{TAG}EF"}],
        )
    }
)

# --- you can, define more than one group, if you wish  --- #
RULES.update(
    {
        rf"((?:밥|진지){TAG}NNG){SEP}((?:먹|들|잡수){TAG}VV)": (
            [{f"밥{TAG}NNG"}, {f"먹{TAG}VV"}],  # casual
            [{f"밥{TAG}NNG", f"진지{TAG}NNG"}, {f"먹{TAG}VV", f"들{TAG}VV", f"잡수{TAG}VV"}],  # polite
            [{f"진지{TAG}NNG"}, {f"들{TAG}VV", f"잡수{TAG}VV"}],  # formal
        )
    }
)


# TODO - right, now that should be alright. We need language models (e.g. maybe start with word2vec?)
# what pre-trained Korean word2vec do we have? -> You probably have to train one yourself.
# TODO - prioritize the tokens that are defined first in the rules.
# TODO - 받침이 있는지 확인? 이걸 정규표현식으로 하는게 가능? - 모든 받침을 하나의 리스트로 정의해두면 가능할 것.


# for validation
def style(sent: str, politeness: int) -> Tuple[str, list]:
    morphemes = [f"{token.form}{TAG}{token.tag}" for token in kiwi.tokenize(sent)]
    # check the formality of the sentence
    ef = [morph for morph in morphemes if morph.endswith("EF")][0]  # noqa
    if ef in CASUAL:
        formality = 0
    elif ef in POLITE:
        formality = 1
    elif ef in FORMAL:
        formality = 2
    else:
        raise ValueError(f"Unknown formality: {ef}")
    if formality == politeness:
        # just return it as-is.
        return sent, morphemes
    possibilities = {}
    joined = SEP.join(morphemes)
    for regex in RULES:
        match = re.search(regex, joined)
        if match:
            for key, honorifics in zip(match.groups(), RULES[regex][politeness]):  # we will have more than one groups
                honorifics = set(honorifics)
                possibilities[key] = possibilities.get(key, honorifics) & honorifics
    candidates = [possibilities.get(morpheme, morpheme) for morpheme in morphemes]
    out = kiwi.join(
        [
            tuple(list(candidate)[0].split(TAG))
            if isinstance(candidate, set)
            else tuple(candidate.split(TAG))
            for candidate in candidates
            if candidate
        ]
    )
    return out, candidates


def main():
    #  to avoid "shadows name out of scope" error
    sent = "저는 배고파요."
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "지금 많이 배고파?"
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "그냥 지금 시작해요."
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "이건 흥미롭군."
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "그건 이 나라의 보물이다."
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "그렇게 하지마."
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "그렇게 하지마세요."  # removal of 시/EF is also possible
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "그렇게 하지마십시오."  # removal of 시/EF is also possible
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "지금 많이 배고프시죠?"  # removal of 시/EF is also possible
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "난 널 사랑해!"  # removal of 시/EF is also possible
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "난 너가 좋아!"  # removal of 시/EF is also possible
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "넌 날 사랑해?"  # removal of 시/EF is also possible
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "진지 잡수세요."  # removal of 시/EF is also possible
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "맛있게 드세요."  # removal of 시/EF is also possible
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))

    sent = "밥 먹어."  # removal of 시/EF is also possible
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))


if __name__ == "__main__":
    main()
