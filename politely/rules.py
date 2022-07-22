from typing import Set, Tuple, Dict

# --- symbols --- #
NULL = ""
TAG = "🔗"
SEP = "⊕"

# --- re-usable regex --- #
ALL = rf"[^\s{SEP}{TAG}{NULL}]"
EFS = rf"(?P<mask>{ALL}+?{TAG}EF)"
WITH_JS = rf"[{''.join({chr(i) for i in range(44032, 55204)} - {chr(44032 + 28 * i) for i in range(399)})}]"

# --- all EF's of different styles --- #
CASUAL = {
    f"어{TAG}EF",
    f"다{TAG}EF",
    f"자{TAG}EF",
    f"대{TAG}EF",
    f"는다{TAG}EF",
    f"마{TAG}EF",
    f"야{TAG}EF",
    f"군{TAG}EF",
    f"네{TAG}EF",
    f"냐{TAG}EF",
    f"ᆫ다{TAG}EF",
    f"ᆯ게{TAG}EF",
    f"ᆫ대{TAG}EF"
}

POLITE = {
    f"어요{TAG}EF",
    f"에요{TAG}EF",
    f"죠{TAG}EF",
    f"래요{TAG}EF",
    f"네요{TAG}EF",
    f"나요{TAG}EF",
    f"대요{TAG}EF",
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


# --- programmatically populated RULES --- #
RULES: Dict[str, Tuple[Set[str], Set[str], Set[str]]] = dict()

# --- the overarching rule --- #
RULES.update({
    EFS: (
        # remember, these are a set of things.
        CASUAL,
        POLITE,
        FORMAL
    )
})

# --- 시/EP (1): 시/으시로 끝나지 않는 VV의 경우, 뒤에 시/EP를 떼거나 붙인다 --- #
RULES.update({
    rf"(?P<mask>{ALL}+?{TAG}VV){SEP}(?!(시|으시){TAG}EP)": (
        {r"\g<mask>"},
        {rf"\g<mask>{SEP}시{TAG}EP", rf"\g<mask>{SEP}으시{TAG}EP"},  # we should be able to do back-referencing
        {rf"\g<mask>{SEP}시{TAG}EP", rf"\g<mask>{SEP}으시{TAG}EP"}
    )
})

# --- 시/EP (2): 이미 시/EP가 존재하는 경우, 반말을 쓸 때 제거한다 --- #
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