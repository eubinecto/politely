"""
Some philosophies to follow:
1. Rules account for 70% of the solution. Strive to hard-code the rules with intuitions and sweat. Keep the rules as general as possible.
2. The remaining 30% is based on the context. Don't use rules for that. It may be effective but it's inefficient (you won't get much from specific rules).
 Disambiguate contexts with masked language models (e.g. Word2Vec, BERT, etc).
3. Every new feature must be tested. If writing Unit tests are not viable, then try to write a small demo.

---
Research Proposal:
RegexBERT - Fine-tuning BERT with Regex-guided Masked Language Modeling
or....
It might be better to generalize this approach over auto-regressive inference.
---
너무나도 obvious한건 정규표현식으로 처리.
나머지 애매모호한 규칙은 BERT에게 맡긴다.
---
20번까지는 공식대로 푼다.
21번과 31번은 머리를 써서 푼다.
"""
# The symbol to use for separating tags from texts
import random
from typing import Dict, Tuple, List
import re
from kiwipiepy import Kiwi
NULL = ""
TAG = "⌇"
# The symbol to use for separating taggd tokens from another tagged tokens
SEP = "⊕"
# The wild cards
# https://www.pythontutorial.net/python-regex/python-regex-non-capturing-group/
EFS_NO_CAP = rf"(?:[^\s{SEP}]+?{TAG}EF)"  # 여기에 시/EP 를 추가할수가 없다.
EFS_WITH_CAP = rf"([^\s{SEP}]+?{TAG}EF)"
# all characters with or without jong sung
ALL_NO_JS = rf"[{''.join([chr(44032 + 28 * i) for i in range(399)])}]"
ALL_WITH_JS = rf"[{''.join({chr(i) for i in range(44032, 55204)} - {chr(44032 + 28 * i) for i in range(399)})}]"

kiwi = Kiwi()

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


# --- The big rule; applied to every cases --- #
RULES: Dict[str, Tuple[List[set], List[set], List[set]]] = {
    EFS_WITH_CAP: ([CASUAL], [POLITE], [FORMAL])
}

# --- 종성이 있는 경우 + any EF's -> 받침으로 시작하는 EF는 해당 X --- #
RULES.update(
    {
        rf"{ALL_WITH_JS}{TAG}[A-Z\-]+?{SEP}{EFS_WITH_CAP}": (
            [CASUAL - {f"ᆫ다{TAG}EF", f"ᆯ게{TAG}EF", f"ᆫ대{TAG}EF"}],
            [POLITE - {f"ᆯ게요{TAG}EF", f"ᆫ대요{TAG}EF", f"ᆫ가요{TAG}EF"}],
            [FORMAL - {f"ᆸ니까{TAG}EF", f"ᆸ시오{TAG}EF", f"ᆸ니다{TAG}EF", f"ᆸ시다{TAG}EF"}],
        )
    }
)


# --- 자/EF --- #
RULES.update(
    {
        rf"(자{TAG}EF)": (
            [{f"자{TAG}EF"}],
            [{f"어요{TAG}EF", f"죠{TAG}EF"}],
            [FORMAL - {f"ᆸ니다{TAG}EF", f"습니까{TAG}EF"}],
        )
    }
)

# --- 군/EF --- #
RULES.update(
    {
        rf"(군{TAG}EF)": (
            [{f"군{TAG}EF"}],
            [{f"어요{TAG}EF", f"네요{TAG}EF"}],
            [{f"ᆸ니다{TAG}EF", f"습니다{TAG}EF"}],
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


# --- 엄마/어머니 --- #
RULES.update(  # noqa
    {
        rf"((?:엄마|어머니){TAG}NNG)": (
            [{f"엄마{TAG}NNG"}],
            [{f"어머니{TAG}NNG"}],
            [{f"어머니{TAG}NNG"}],
        )
    }
)


# --- 아빠/아버지 --- #
RULES.update(
    {
        rf"((?:아빠|아버지){TAG}NNG)": (
            [{f"아빠{TAG}NNG"}],
            [{f"아빠{TAG}NNG"}],
            [{f"아빠{TAG}NNG"}],
        )
    }
)

# --- 가/께서 --- #
RULES.update(
    {
        # 맥락이 필요한 경우... ㅎ 하지만 규칙을 때려박으면 해결은 가능함.
        # 정규표현식 짱짱맨.
        rf"((?:가|께서){TAG}JKS)": (
            [{f"가{TAG}JKS"}],
            #  이..는 왜? -> e.g. 전 당신이 좋아요.
            [{f"께서{TAG}JKS", f"이{TAG}JKS"}],
            [{f"께서{TAG}JKS", f"이{TAG}JKS"}]
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

# --- 시/EP --- #
RULES.update(
    {
        rf"(시{TAG}EP)": (
            [{NULL}],
            [{f"시{TAG}EP"}],
            [{f"시{TAG}EP"}],
        )
    }
)


# --- 시/EP + all/EF --- #
RULES.update(
    {
        rf"(시{TAG}EP){SEP}{EFS_WITH_CAP}": (
            [{NULL}, CASUAL],
            [{f"시{TAG}EP"}, POLITE - {f"에요{TAG}EF", f"네요{TAG}EF"}],
            # ㅅ is redundant
            [{f"시{TAG}EP"}, FORMAL - {f"습니까{TAG}EF", f"ᆸ시다{TAG}EF"}],
        )
    }
)

# --- ends with ?/SF --- #
RULES.update(
    {
        rf"{EFS_WITH_CAP}{SEP}\?{TAG}SF": (
            [CASUAL],
            [POLITE - {f"네요{TAG}EF", f"ᆯ게요{TAG}EF"}],
            [{f"습니까{TAG}EF", f"ᆸ니까{TAG}EF"}],  # nothing but 습니까 is allowed
        )
    }
)

# --- ends with ./SF, !/SF --- #
RULES.update(
    {
        rf"{EFS_WITH_CAP}{SEP}[.!]{TAG}SF": (
            [CASUAL],
            [POLITE],
            [FORMAL - {f"습니까{TAG}EF", f"ᆸ니까{TAG}EF"}],  # anything but 습니까 is allowed
        )
    }
)

# ---- 이/VCP + EFs --- #
RULES.update(
    {
        rf"이{TAG}VCP{SEP}{EFS_WITH_CAP}": (
            [{f"어{TAG}EF", f"다{TAG}EF", f"야{TAG}EF", f"군{TAG}EF"}],
            [{f"에요{TAG}EF", f"죠{TAG}EF"}],
            [{f"ᆸ니다{TAG}EF", f"습니다{TAG}EF"}],
        )
    }
)

# --- 밥 or 진지 --- #
RULES.update(
    {
        rf"((?:밥|진지){TAG}NNG)": (
            [{f"밥{TAG}NNG"}],  # casual
            [{f"밥{TAG}NNG", f"진지{TAG}NNG"}],  # polite
            [{f"진지{TAG}NNG"}]  # formal
        )
    }
)


# --- 먹/들/잡수 (위와 합치면 안된다. e.g. "맛있게 드세요") --- #
RULES.update(
    {
        rf"((?:먹|들|잡수){TAG}VV)": (
            [{f"먹{TAG}VV"}],  # casual
            [{f"먹{TAG}VV", f"들{TAG}VV", f"잡수{TAG}VV"}],  # polite
            [{f"들{TAG}VV", f"잡수{TAG}VV"}]  # formal
        )
    }
)


# what pre-trained Korean word2vec do we have? -> You probably have to train one yourself.
# TODO - prioritize the tokens that are defined first in the rules. (how do you preserve the order?)
# TODO - we need scores as well. for the time being, prioritize  어, 어요, 습니다, 습니까. (You won't need this once you apply
# TODO -  language models. This is just to replicate the previous behaviour).
# TODO - multi-token candidates? How should we deal with this?  (e.g. 하+라 -> 하+어요 도 가능하지만, 하+시+어요도 가능하다.).
# TODO - formality check 대신, 그냥 입력으로 들어온 EF는 가산점을 주는 편으로 변경하는게 낫다.
# TODO - 언어모델을 적용할 때 - 모든 permutation의 점수를 계산하고, 가장 점수가 높은 것을 선택하는 것이 낫다. (음... 그런데.. 만약에 sentence 임베딩을 구해야하는 것이라면...?)
# 일단.. . 현재까지는 그렇게 적용한다.

# 골치 아플듯 ㅠ
# 어쩔 수 없다. 규칙은 규칙이다. 하나의 토큰만을 혀용할 수 밖에 없다.
# 그렇다면... 십시오, 십니다, 시네요, 시나요, 등..을, 그냥 추가해버리고, 토큰나이저도 그렇게 토크나이즈 하도록 하는 편이. 나을수도 있다.
# 여러개의 토큰을 허용하는 순간, generation에 더 적합해진다.
# 이건 좀 더 고민해볼 문제인듯. 일단 이정도로도 괜찮은 성과이니, 이걸 그대로 가져가서 한번 배포를 해보자.
# 그건 역시.. 그냥 노가다다. 최소한의 규칙을 유지해야하는데. 음.

# for validation
def style(sent: str, politeness: int) -> Tuple[str, list]:
    morphemes = [f"{token.form}{TAG}{token.tag}" for token in kiwi.tokenize(sent)]
    # --- get possible honorifics for each morpheme --- #
    morph2honorifics = {}
    joined = SEP.join(morphemes)
    for regex in RULES:
        match = re.search(regex, joined)
        if match:
            for key, honorifics in zip(match.groups(), RULES[regex][politeness]):
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
                besties.append(tuple(best.split(TAG)))
        else:
            besties.append(tuple(morpheme.split(TAG)))
    # --- join the besties with kiwi's conjugation algorithm --- #
    styled = kiwi.join(besties)
    return styled, morphemes


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

    sent = "어머니께서 진지를 잡수시기로 하셨다."  # removal of 시/EF is also possible
    print(f"honorifying: {sent}")
    print(style(sent, 0))
    print(style(sent, 1))
    print(style(sent, 2))


if __name__ == "__main__":
    main()

"""
honorifying: 저는 배고파요.
('나는 배고플게.', [{'나⌇NP'}, '는⌇JX', '배고프⌇VA', {'ᆯ게⌇EF', 'ᆫ다⌇EF', '군⌇EF', '마⌇EF', '는다⌇EF', '자⌇EF', '다⌇EF', '네⌇EF', 'ᆫ대⌇EF', '어⌇EF', '야⌇EF'}, '.⌇SF'])
('저는 배고파요.', ['저⌇NP', '는⌇JX', '배고프⌇VA', '어요⌇EF', '.⌇SF'])
('저는 배고픕니다.', [{'저⌇NP'}, '는⌇JX', '배고프⌇VA', {'습니다⌇EF', 'ᆸ시오⌇EF', 'ᆸ니다⌇EF', 'ᆸ시다⌇EF'}, '.⌇SF'])
honorifying: 지금 많이 배고파?
('지금 많이 배고파?', ['지금⌇MAG', '많이⌇MAG', '배고프⌇VA', '어⌇EF', '?⌇SF'])
('지금 많이 배고픈가요?', ['지금⌇MAG', '많이⌇MAG', '배고프⌇VA', {'ᆫ가요⌇EF', '래요⌇EF', '어요⌇EF', '죠⌇EF', 'ᆫ대요⌇EF', '나요⌇EF', '에요⌇EF'}, '?⌇SF'])
('지금 많이 배고픕니까?', ['지금⌇MAG', '많이⌇MAG', '배고프⌇VA', {'ᆸ니까⌇EF', '습니까⌇EF'}, '?⌇SF'])
honorifying: 그냥 지금 시작해요.
('그냥 지금 시작할게.', ['그냥⌇MAG', '지금⌇MAG', '시작⌇NNG', '하⌇XSV', {'ᆯ게⌇EF', 'ᆫ다⌇EF', '군⌇EF', '마⌇EF', '는다⌇EF', '자⌇EF', '다⌇EF', '네⌇EF', 'ᆫ대⌇EF', '어⌇EF', '야⌇EF'}, '.⌇SF'])
('그냥 지금 시작해요.', ['그냥⌇MAG', '지금⌇MAG', '시작⌇NNG', '하⌇XSV', '어요⌇EF', '.⌇SF'])
('그냥 지금 시작합니다.', ['그냥⌇MAG', '지금⌇MAG', '시작⌇NNG', '하⌇XSV', {'습니다⌇EF', 'ᆸ시오⌇EF', 'ᆸ니다⌇EF', 'ᆸ시다⌇EF'}, '.⌇SF'])
honorifying: 이건 흥미롭군.
('이건 흥미롭군.', ['이⌇NP', '이⌇VCP', '건⌇EC', '흥미⌇NNG', '롭⌇XSA-I', '군⌇EF', '.⌇SF'])
('이건 흥미롭네요.', ['이⌇NP', '이⌇VCP', '건⌇EC', '흥미⌇NNG', '롭⌇XSA-I', {'네요⌇EF', '어요⌇EF'}, '.⌇SF'])
('이건 흥미롭습니다.', ['이⌇NP', '이⌇VCP', '건⌇EC', '흥미⌇NNG', '롭⌇XSA-I', {'습니다⌇EF'}, '.⌇SF'])
honorifying: 그건 이 나라의 보물이다.
('그건 이 나라의 보물이다.', ['그거⌇NP', 'ᆫ⌇JX', '이⌇MM', '나라⌇NNG', '의⌇JKG', '보물⌇NNG', '이⌇VCP', '다⌇EF', '.⌇SF'])
('그거는 이 나라의 보물이죠.', ['그거⌇NP', 'ᆫ⌇JX', '이⌇MM', '나라⌇NNG', '의⌇JKG', '보물⌇NNG', '이⌇VCP', {'죠⌇EF', '에요⌇EF'}, '.⌇SF'])
('그거는 이 나라의 보물입니다.', ['그거⌇NP', 'ᆫ⌇JX', '이⌇MM', '나라⌇NNG', '의⌇JKG', '보물⌇NNG', '이⌇VCP', {'습니다⌇EF', 'ᆸ니다⌇EF'}, '.⌇SF'])
honorifying: 그렇게 하지마.
('그렇게 하지마.', ['그렇⌇VA', '게⌇EC', '하⌇VV', '지⌇EC', '말⌇VX', '어⌇EF', '.⌇SF'])
('그렇게 하지 말래요.', ['그렇⌇VA', '게⌇EC', '하⌇VV', '지⌇EC', '말⌇VX', {'래요⌇EF', '어요⌇EF', '죠⌇EF', '나요⌇EF', '네요⌇EF', '에요⌇EF'}, '.⌇SF'])
('그렇게 하지 맙니다.', ['그렇⌇VA', '게⌇EC', '하⌇VV', '지⌇EC', '말⌇VX', {'습니다⌇EF'}, '.⌇SF'])
honorifying: 그렇게 하지마세요.
('그렇게 하지 말게.', ['그렇⌇VA', '게⌇EC', '하⌇VV', '지⌇EC', '말⌇VX', {'ᆯ게⌇EF', 'ᆫ다⌇EF', '군⌇EF', '마⌇EF', '는다⌇EF', '자⌇EF', '다⌇EF', '네⌇EF', 'ᆫ대⌇EF', '어⌇EF', '야⌇EF'}, '.⌇SF'])
('그렇게 하지마세요.', ['그렇⌇VA', '게⌇EC', '하⌇VV', '지⌇EC', '말⌇VX', '시⌇EP', '어요⌇EF', '.⌇SF'])
('그렇게 하지 마십니다.', ['그렇⌇VA', '게⌇EC', '하⌇VV', '지⌇EC', '말⌇VX', {'시⌇EP'}, {'습니다⌇EF', 'ᆸ시오⌇EF', 'ᆸ니다⌇EF'}, '.⌇SF'])
honorifying: 그렇게 하지마십시오.
('그렇게 하지 말게.', ['그렇⌇VA', '게⌇EC', '하⌇VV', '지⌇EC', '말⌇VX', {'ᆯ게⌇EF', 'ᆫ다⌇EF', '군⌇EF', '마⌇EF', '는다⌇EF', '자⌇EF', '다⌇EF', '네⌇EF', 'ᆫ대⌇EF', '어⌇EF', '야⌇EF'}, '.⌇SF'])
('그렇게 하지 마실게요.', ['그렇⌇VA', '게⌇EC', '하⌇VV', '지⌇EC', '말⌇VX', {'시⌇EP'}, {'ᆯ게요⌇EF', 'ᆫ가요⌇EF', '래요⌇EF', '어요⌇EF', '죠⌇EF', 'ᆫ대요⌇EF', '나요⌇EF'}, '.⌇SF'])
('그렇게 하지마십시오.', ['그렇⌇VA', '게⌇EC', '하⌇VV', '지⌇EC', '말⌇VX', '시⌇EP', 'ᆸ시오⌇EF', '.⌇SF'])
honorifying: 지금 많이 배고프시죠?
('지금 많이 배고플게?', ['지금⌇MAG', '많이⌇MAG', '배고프⌇VA', {'ᆯ게⌇EF', 'ᆫ다⌇EF', '군⌇EF', '마⌇EF', '는다⌇EF', '자⌇EF', '다⌇EF', '네⌇EF', 'ᆫ대⌇EF', '어⌇EF', '야⌇EF'}, '?⌇SF'])
('지금 많이 배고프시죠?', ['지금⌇MAG', '많이⌇MAG', '배고프⌇VA', '시⌇EP', '죠⌇EF', '?⌇SF'])
('지금 많이 배고프십니까?', ['지금⌇MAG', '많이⌇MAG', '배고프⌇VA', {'시⌇EP'}, {'ᆸ니까⌇EF'}, '?⌇SF'])
honorifying: 난 널 사랑해!
('난 널 사랑해!', ['나⌇NP', 'ᆫ⌇JX', '너⌇NP', 'ᆯ⌇JKO', '사랑⌇NNG', '하⌇XSV', '어⌇EF', '!⌇SF'])
('저는 당신을 사랑할게요!', [{'저⌇NP'}, 'ᆫ⌇JX', {'당신⌇NP'}, {'을⌇JKO'}, '사랑⌇NNG', '하⌇XSV', {'ᆯ게요⌇EF', 'ᆫ가요⌇EF', '래요⌇EF', '어요⌇EF', '죠⌇EF', 'ᆫ대요⌇EF', '나요⌇EF', '네요⌇EF', '에요⌇EF'}, '!⌇SF'])
('저는 당신을 사랑합니다!', [{'저⌇NP'}, 'ᆫ⌇JX', {'당신⌇NP'}, {'을⌇JKO'}, '사랑⌇NNG', '하⌇XSV', {'습니다⌇EF', 'ᆸ시오⌇EF', 'ᆸ니다⌇EF', 'ᆸ시다⌇EF'}, '!⌇SF'])
honorifying: 난 너가 좋아!
('난 너가 좋아!', ['나⌇NP', 'ᆫ⌇JX', '너⌇NP', '가⌇JKS', '좋⌇VA', '어⌇EF', '!⌇SF'])
('저는 당신이 조래요!', [{'저⌇NP'}, 'ᆫ⌇JX', {'당신⌇NP'}, '가⌇JKS', '좋⌇VA', {'래요⌇EF', '어요⌇EF', '죠⌇EF', '나요⌇EF', '네요⌇EF', '에요⌇EF'}, '!⌇SF'])
('저는 당신이 좋습니다!', [{'저⌇NP'}, 'ᆫ⌇JX', {'당신⌇NP'}, '가⌇JKS', '좋⌇VA', {'습니다⌇EF'}, '!⌇SF'])
honorifying: 넌 날 사랑해?
('넌 날 사랑해?', ['너⌇NP', 'ᆫ⌇JX', '나⌇NP', 'ᆯ⌇JKO', '사랑⌇NNG', '하⌇XSV', '어⌇EF', '?⌇SF'])
('당신은 절 사랑한가요?', [{'당신⌇NP'}, 'ᆫ⌇JX', {'저⌇NP'}, 'ᆯ⌇JKO', '사랑⌇NNG', '하⌇XSV', {'ᆫ가요⌇EF', '래요⌇EF', '어요⌇EF', '죠⌇EF', 'ᆫ대요⌇EF', '나요⌇EF', '에요⌇EF'}, '?⌇SF'])
('당신은 절 사랑합니까?', [{'당신⌇NP'}, 'ᆫ⌇JX', {'저⌇NP'}, 'ᆯ⌇JKO', '사랑⌇NNG', '하⌇XSV', {'ᆸ니까⌇EF', '습니까⌇EF'}, '?⌇SF'])
honorifying: 진지 잡수세요.
('밥 먹을게.', [{'밥⌇NNG'}, {'먹⌇VV'}, {'ᆯ게⌇EF', 'ᆫ다⌇EF', '군⌇EF', '마⌇EF', '는다⌇EF', '자⌇EF', '다⌇EF', '네⌇EF', 'ᆫ대⌇EF', '어⌇EF', '야⌇EF'}, '.⌇SF'])
('진지 잡수세요.', ['진지⌇NNG', '잡수⌇VV', '시⌇EP', '어요⌇EF', '.⌇SF'])
('진지 드십니다.', [{'진지⌇NNG'}, {'들⌇VV', '잡수⌇VV'}, {'시⌇EP'}, {'습니다⌇EF', 'ᆸ시오⌇EF', 'ᆸ니다⌇EF'}, '.⌇SF'])
honorifying: 맛있게 드세요.
('맛있게 먹을게.', ['맛있⌇VA', '게⌇EC', {'먹⌇VV'}, {'ᆯ게⌇EF', 'ᆫ다⌇EF', '군⌇EF', '마⌇EF', '는다⌇EF', '자⌇EF', '다⌇EF', '네⌇EF', 'ᆫ대⌇EF', '어⌇EF', '야⌇EF'}, '.⌇SF'])
('맛있게 드세요.', ['맛있⌇VA', '게⌇EC', '들⌇VV', '시⌇EP', '어요⌇EF', '.⌇SF'])
('맛있게 드십니다.', ['맛있⌇VA', '게⌇EC', {'들⌇VV', '잡수⌇VV'}, {'시⌇EP'}, {'습니다⌇EF', 'ᆸ시오⌇EF', 'ᆸ니다⌇EF'}, '.⌇SF'])
honorifying: 밥 먹어.
('밥 먹어.', ['밥⌇NNG', '먹⌇VV', '어⌇EF', '.⌇SF'])
('진지 들래요.', [{'진지⌇NNG', '밥⌇NNG'}, {'들⌇VV', '먹⌇VV', '잡수⌇VV'}, {'래요⌇EF', '어요⌇EF', '죠⌇EF', '나요⌇EF', '네요⌇EF', '에요⌇EF'}, '.⌇SF'])
('진지 듭니다.', [{'진지⌇NNG'}, {'들⌇VV', '잡수⌇VV'}, {'습니다⌇EF'}, '.⌇SF'])
"""