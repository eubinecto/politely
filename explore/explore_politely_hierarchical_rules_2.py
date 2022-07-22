"""
This is going to be the d
"""
import re
from typing import Tuple
from kiwipiepy import Kiwi

NULL = ""
TAG = "⌇"
SEP = "⊕"
ALL = rf"[^\s{SEP}]"
EFS = rf"(?P<mask>{ALL}+?{TAG}EF)"
NO_JS = rf"[{''.join([chr(44032 + 28 * i) for i in range(399)])}]"
WITH_JS = rf"[{''.join({chr(i) for i in range(44032, 55204)} - {chr(44032 + 28 * i) for i in range(399)})}]"


# --- all EF's for different styles of politeness --- #
# style - transfer
CASUAL = {
    f"어{TAG}EF",
    f"다{TAG}EF",
    f"자{TAG}EF",
    f"는다{TAG}EF",
    f"마{TAG}EF",
    f"야{TAG}EF",
    f"군{TAG}EF",
    f"네{TAG}EF",
    f"ᆫ다{TAG}EF",
    f"ᆯ게{TAG}EF",
    f"ᆫ대{TAG}EF",
}

# 음.. 그냥... 시를 더해버리는 방법도 있다.
# 이건.. 나중에 고민하자.
POLITE = {
    f"어요{TAG}EF",
    f"에요{TAG}EF",
    f"죠{TAG}EF",
    f"래요{TAG}EF",
    f"네요{TAG}EF",
    f"나요{TAG}EF",
    f"ᆯ게요{TAG}EF",
    f"ᆫ대요{TAG}EF",
    f"ᆫ가요{TAG}EF"
}
FORMAL = {
    f"습니다{TAG}EF",
    f"습니까{TAG}EF",
    f"ᆸ니까{TAG}EF",
    f"ᆸ시오{TAG}EF",
    f"ᆸ니다{TAG}EF",
    f"ᆸ시다{TAG}EF"
}


# --- the overarching rule --- #
RULES = {
    EFS: (
        # remember, these are a set of things.
        CASUAL,
        POLITE,
        FORMAL
    )
}

# --- 시/EP (1) 시/으시로 끝나지 않는 VV의 경우, 뒤에 시/EP를 떼거나 붙인다 --- #
RULES.update({
    rf"(?P<mask>{ALL}+?{TAG}VV){SEP}(?!(시|으시){TAG}EP)": (
        {r"\g<mask>"},
        {rf"\g<mask>{SEP}시{TAG}EP", rf"\g<mask>{SEP}으시{TAG}EP"},  # we should be able to do back-referencing
        {rf"\g<mask>{SEP}시{TAG}EP", rf"\g<mask>{SEP}으시{TAG}EP"}
    )
})

# --- 시/EP (2) 이미 시/EP가 존재하는 경우, 반말을 쓸 때 제거한다 --- #
RULES.update(
    {
        rf"(?P<mask>(시|으시){TAG}EP)": (
            {NULL},  # you don't use them
            {r"\g<mask>"},  # just repeat yourself
            {r"\g<mask>"},  # just repeat yourself
        )
    }
)


# --- 종성이 있는 경우, 종성으로 시작하는 EF는 사용하지 않음 --- #
RULES.update(
    {
        rf"{WITH_JS}{TAG}[A-Z\-]+?{SEP}{EFS}": (
            CASUAL - {f"ᆫ다{TAG}EF", f"ᆯ게{TAG}EF", f"ᆫ대{TAG}EF"},
            POLITE - {f"ᆯ게요{TAG}EF", f"ᆫ대요{TAG}EF", f"ᆫ가요{TAG}EF"},
            FORMAL - {f"ᆸ니까{TAG}EF", f"ᆸ시오{TAG}EF", f"ᆸ니다{TAG}EF", f"ᆸ시다{TAG}EF"}
        )
    }
)


# --- 나/저 --- #
RULES.update(
    {
        rf"(?P<mask>(?:나|저){TAG}NP)": (
            {f"나{TAG}NP"},
            {f"저{TAG}NP"},
            {f"저{TAG}NP"}
        )
    }
)


# --- 너/당신 --- #
RULES.update(
    {
        rf"(?P<mask>(?:너|당신){TAG}NP)": (
            {f"너{TAG}NP"},
            {f"당신{TAG}NP"},
            {f"당신{TAG}NP"}
        )
    }
)


# --- 엄마/어머니 --- #
RULES.update(  # noqa
    {
        rf"(?P<mask>(?:엄마|어머니){TAG}NNG)": (
            {f"엄마{TAG}NNG"},
            {f"어머니{TAG}NNG"},
            {f"어머니{TAG}NNG"}
        )
    }
)


# --- 아빠/아버지 --- #
RULES.update(
    {
        rf"(?P<mask>(?:아빠|아버지){TAG}NNG)": (
            {f"아빠{TAG}NNG"},
            {f"아빠{TAG}NNG"},
            {f"아빠{TAG}NNG"}
        )
    }
)

# --- 가/께서 --- #
RULES.update(
    {
        rf"(?P<mask>(?:가|께서){TAG}JKS)": (
            {f"가{TAG}JKS"},
            {f"께서{TAG}JKS", f"이{TAG}JKS"},
            {f"께서{TAG}JKS", f"이{TAG}JKS"}
        )
    }
)


kiwi = Kiwi()


def score(morph: str) -> float:
    """
    Very rudimentary scoring function. Does not regard the context at all.
    Perhaps turn this into a Scorer class, in case you get to use a language model.
    """
    # 우선, 이것들이 우선시되어야 하는 건 맞음.
    if morph in (f"어{TAG}EF",
                 f"어요{TAG}EF",
                 f"어요{TAG}EF",
                 f"습니다{TAG}EF",
                 f"ᆸ니다{TAG}EF"):
        return 1
    else:
        return 0


def style(sent: str, politeness: int) -> Tuple[str, list]:
    """
    This is an experimental demo of the next version of Politely. This uses regular expressions
    effectively.
    """
    # --- analyze --- #
    """
    Use Kiwi to analyze the morphemes of the sentence.
    """
    morphs = [f"{token.form}{TAG}{token.tag}" for token in kiwi.tokenize(sent)]
    # --- honorify --- #
    """
    Using the chained conjunction algorithm, we can determine the candidates that would
    properly honorify the sentence.
    """
    joined = SEP.join(morphs)
    morph2honorifics = {}
    for regex in RULES:
        match = re.search(regex, joined)
        if match:
            key = match.group("mask")
            honorifics = {honorific.replace(r"\g<mask>", key) for honorific in RULES[regex][politeness]}
            morph2honorifics[key] = morph2honorifics.get(key, honorifics) & honorifics
    candidates = [
        morph2honorifics.get(morph, morph)
        for morph in morphs
    ]
    # --- guess --- #
    """
    Now that we have the candidates, we should guess which one
    is the correct one.
    """
    guess = list()
    for candidate in candidates:
        if isinstance(candidate, set):
            # can we do better than random choice?
            best = sorted(list(candidate), key=score, reverse=True)[0]
            if best != NULL:
                for morph2pos in best.split(SEP):
                    guess.append(tuple(morph2pos.split(TAG)))
        else:
            guess.append(tuple(candidate.split(TAG)))
    # --- conjugate --- #
    """
    Conjugate the guess to get the final result.
    """
    out = kiwi.join(guess)  # noqa
    return out, candidates


print(style("안녕하세요", 0))
print(style("이거 했어?", 1))
print(style("밥 먹었어?", 1))
print(style("밥 먹으셨어요?", 1))
print(style("밥 먹으셨어요?", 0))
print(style("난 널 사랑하는 것 같아", 0))
print(style("난 널 사랑하는 것 같아", 1))
print(style("난 널 사랑하는 것 같아", 2))