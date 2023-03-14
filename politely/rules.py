from typing import Set, Tuple, Dict

# --- symbols --- #
NULL = "❌"
TAG = "🏷"
SEP = "🔗"


# --- all EF's of different styles --- #
CASUAL = {
    f"어{TAG}EF",
    f"다{TAG}EF",
    f"라{TAG}EF",
    f"어라{TAG}EF",
    f"자{TAG}EF",
    f"대{TAG}EF",
    f"는다{TAG}EF",
    f"마{TAG}EF",
    f"야{TAG}EF",
    f"군{TAG}EF",
    f"네{TAG}EF",
    f"냐{TAG}EF",
    f"ᆫ다{TAG}EF",
    f"란다{TAG}EF",
    f"ᆯ게{TAG}EF",
    f"ᆫ대{TAG}EF",
    f"ᆫ가{TAG}EF",
    f"지{TAG}EF"
}

POLITE = {
    f"어요{TAG}EF",
    f"시{TAG}EP{SEP}어요{TAG}EF",
    f"에요{TAG}EF",
    f"지요{TAG}EF",
    f"래요{TAG}EF",
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
    f"시{TAG}EP{SEP}습니다{TAG}EF",
    f"습니까{TAG}EF",
    f"랍니다{TAG}EF",
    f"ᆸ니까{TAG}EF",
    f"ᆸ시오{TAG}EF",
    f"ᆸ니다{TAG}EF",
    f"ᆸ시다{TAG}EF"
}


# --- regex --- #
EFS = rf"(?P<MASK>({'|'.join([pair for pair in (CASUAL | POLITE | FORMAL)])}))"
SELF = rf"\g<MASK>"
WITH_JONG_SUNG = rf"[{''.join({chr(i) for i in range(44032, 55204)} - {chr(44032 + 28 * i) for i in range(399)})}]"


# --- programmatically populated RULES --- #
RULES: Dict[str, Tuple[Set[str], Set[str], Set[str]]] = dict()

# --- the overarching rule --- #
RULES.update({
    EFS: (
        CASUAL,
        POLITE,
        FORMAL
    )
})

# --- 시/EP: 이미 시/EP가 존재하는 경우, 반말을 쓸 때 제거한다 --- #
RULES.update(
    {
        rf"(?P<MASK>(시|으시){TAG}EP)": (
            {NULL},  # you don't use them
            {SELF},  # just repeat yourself
            {SELF},  # just repeat yourself
        )
    }
)


# --- 종성이 있는 경우, 종성으로 시작하는 EF는 사용하지 않음 --- #
RULES.update(
    {
        rf"{WITH_JONG_SUNG}{TAG}[A-Z\-]+?{SEP}{EFS}": (
            CASUAL - {f"ᆫ다{TAG}EF", f"ᆯ게{TAG}EF", f"ᆫ대{TAG}EF"},
            POLITE - {f"ᆯ게요{TAG}EF", f"ᆫ대요{TAG}EF", f"ᆫ가요{TAG}EF"},
            FORMAL - {f"ᆸ니까{TAG}EF", f"ᆸ시오{TAG}EF", f"ᆸ니다{TAG}EF", f"ᆸ시다{TAG}EF"}
        )
    }
)


# --- 의문형인 경우, formal은 -니까만 가능 --- #
RULES.update(
    {
        rf"{EFS}{SEP}\?{TAG}SF": (
            CASUAL,
            POLITE,
            {f"습니까{TAG}EF", f"ᆸ니까{TAG}EF"}
        )
    }
)

# --- 나/저 --- #
RULES.update(
    {
        rf"(?P<MASK>(나|저){TAG}NP)": (
            {f"나{TAG}NP"},
            {f"저{TAG}NP"},
            {f"저{TAG}NP"}
        )
    }
)


# --- 너/당신 --- #
RULES.update(
    {
        rf"(?P<MASK>(너|당신){TAG}NP)": (
            {f"너{TAG}NP"},
            {f"당신{TAG}NP"},
            {f"당신{TAG}NP"}
        )
    }
)


# --- 엄마/어머니 --- #
RULES.update(  # noqa
    {
        rf"(?P<MASK>(엄마|어머니|어머님){TAG}NNG)": (
            {f"엄마{TAG}NNG"},
            {f"어머니{TAG}NNG", f"어머님{TAG}NNG"},
            {f"어머니{TAG}NNG", f"어머님{TAG}NNG"}
        )
    }
)


# --- 아빠/아버지 --- #
RULES.update(
    {
        rf"(?P<MASK>(아빠|아버지|아버님){TAG}NNG)": (
            {f"아빠{TAG}NNG"},
            {f"아버지{TAG}NNG", f"아버님{TAG}NNG"},
            {f"아버지{TAG}NNG", f"아버님{TAG}NNG"}
        )
    }
)

# --- 께서 --- #
RULES.update(
    {
        rf"(어머니|어머님|아버지|아버님|선생님|할머니|할아버지){TAG}NNG{SEP}(?P<MASK>\S+?{TAG}JKS)": (
            {SELF},
            {f"께서{TAG}JKS"},
            {f"께서{TAG}JKS"}
        )
    }
)

# --- 란다 -> 래요 / 랍니다 --- #
RULES.update(
    {
        rf"(?P<MASK>(란다|래요|랍니다){TAG}EF)": (
            {f"란다{TAG}EF"},
            {f"래요{TAG}EF"},
            {f"랍니다{TAG}EF"}
        )
    }
)


# --- 지 -> 지요 --- #
RULES.update(
    {
        rf"(?P<MASK>(지|지요|ᆸ니다){TAG}EF)": (
            {f"지{TAG}EF"},
            {f"지요{TAG}EF"},
            #  전부 가능함
            FORMAL
        )
    }
)


# ---- to be used for scoring -- #
PREFERENCES = {f"어{TAG}EF",
               f"어요{TAG}EF",
               f"어요{TAG}EF",
               f"습니다{TAG}EF",
               f"ᆸ니다{TAG}EF"}
