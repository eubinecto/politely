"""
How do I make the candidates back-referencible?

"""
import re
import random
from typing import Tuple
from kiwipiepy import Kiwi
from explore.explore_politely_hierarchical_rules_dict import EFS_WITH_CAP, CASUAL, POLITE, FORMAL

NULL = ""
TAG = "⌇"
# The symbol to use for separating taggd tokens from another tagged tokens
SEP = "⊕"
# The wild cards
ALL = rf"[^\s{SEP}]"
SELF = r"\g<mask>"
kiwi = Kiwi()

# --- the overarching rule --- #
RULES = {
    rf"(?P<mask>{ALL}+?{TAG}EF)": (
        # remember, these are a set of things.
        CASUAL,
        POLITE,
        FORMAL
    )
}

# --- 선어말어미 -시... 어간뒤에 붙이는 것은 항상 가능하다! --- #
RULES.update({
    rf"(?P<mask>{ALL}+?{TAG}VV){SEP}(?!(시|으시){TAG}EP)": (
        {f"{SELF}"},
        {f"{SELF}{SEP}시{TAG}EP", f"{SELF}{SEP}으시{TAG}EP"},  # we should be able to do back-referencing
        {f"{SELF}{SEP}시{TAG}EP", f"{SELF}{SEP}으시{TAG}EP"}
    )
})

# --- 시/EP --- #
RULES.update(
    {
        rf"(?P<mask>(시|으시){TAG}EP)": (
            {NULL},  # you don't use them
            {SELF},  # just repeat yourself
            {SELF},  # just repeat yourself
        )
    }
)


def style(sent: str, politeness: int) -> Tuple[str, list]:
    morphemes = [f"{token.form}{TAG}{token.tag}" for token in kiwi.tokenize(sent)]
    # --- get possible honorifics for each morpheme --- #
    joined = SEP.join(morphemes)
    morph2honorifics = {}
    for regex in RULES:
        match = re.search(regex, joined)
        if match:
            key = match.group("mask")
            honorifics = {honorific.replace(SELF, key) for honorific in RULES[regex][politeness]}
            morph2honorifics[key] = morph2honorifics.get(key, honorifics) & honorifics
    # --- update morphemes with candidate honorifics --- #
    morphemes = [
        morph2honorifics.get(morpheme, morpheme)
        for morpheme in morphemes
    ]
    # --- construct the besties --- #
    besties = list()
    for morpheme in morphemes:
        if isinstance(morpheme, set):
            best = random.choice(list(morpheme))
            if best != NULL:
                # You may want further splitting
                for morph2pos in best.split(SEP):
                    besties.append(tuple(morph2pos.split(TAG)))
        else:
            besties.append(tuple(morpheme.split(TAG)))
    # --- join the besties with kiwi's conjugation algorithm --- #
    styled = kiwi.join(besties)
    return styled, morphemes


print(style("안녕하세요", 0))
print(style("이거 했어?", 1))
print(style("밥 먹었어?", 1))
print(style("밥 먹으셨어요?", 1))
print(style("밥 먹으셨어요?", 0))