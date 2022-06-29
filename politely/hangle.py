from soynlp.hangle import compose as soy_compose
from soynlp.hangle import decompose as soy_decompose
from soynlp.lemmatizer import conjugate as soy_conjugate
from typing import Tuple


def compose(cho: str, jung: str, jong: str) -> str:
    return soy_compose(cho, jung, jong)


def decompose(letter: str) -> Tuple[str, str, str]:
    return soy_decompose(letter)


def conjugate(left: str, right: str) -> Tuple[str, tuple]:
    r_first = right[0]
    l_last = left[-1]
    l_cho, l_jung, l_jong = decompose(l_last)  # decompose the last element
    r_cho, r_jung, r_jong = decompose(r_first)  # decompose the first element
    if l_jong == " " and right.startswith("ㅂ니"):
        # e.g. 전 이제 떠나ㅂ니다 -> 전 이제 떠납니다
        left = left[:-1] + compose(l_cho, l_jung, "ㅂ")
        left += right[1:]
        log = l_last, r_first, left, f"어간에 받침이 없고 어미가 읍인 경우, ㅂ은 어간의 받침으로 쓰임"
    elif l_jong != " " and right.startswith("ㅂ니"):
        # e.g. 갔ㅂ니다 -> 갔습니다
        left += f"습{right[1:]}"
        log = l_last, r_first, left, f"종성있음 + `ㅂ니` -> 습니"
    elif l_jong != " " and right.startswith("ㅂ시"):
        # 줍은 예외
        if left == "줍":
            left = left[:-1] + "주웁"
            left += right[1:]
            log = l_last, r_first, left, f"줍 예외"
        else:
            # e.g. 먹ㅂ시다
            left += f"읍{right[1:]}"
            log = l_last, r_first, left, f"종성있음 + `ㅂ시` -> 읍니"
    elif l_jong == "ㅎ" and r_first == "어":
        # e.g. 어떻 + 어요 -> 어때요, 좋어요 -> 좋아요
        left = left[:-1] + compose(l_cho, "ㅐ", " ")
        left += right[1:]
        log = l_last, r_first, left, f"`ㅎ` + `어` -> `ㅐ`"
    elif l_jung == "ㅣ" and l_jong == " " and r_first == "어":
        # e.g. 시어 -> 셔
        # 하지만 e.g. 있어 -> 있어
        # 히지만 e.g. 이어
        left = left[:-1] + compose(l_cho, "ㅕ", " ")
        left += right[1:]
        log = l_last, r_first, left, f"`ㅣ`+ `ㅓ` -> `ㅕ`"
    elif l_jung == "ㅏ" and l_jong in ("ㄷ", "ㅌ") and r_first == "어":
        # e.g. 같어요 -> 같아요
        # e.g  닫어요 -> 닫아요
        left += f"아{right[1:]}"
        log = l_last, r_first, left, f"`ㅏ (종성o)`+ `ㅓ` -> `ㅕ`"
    elif l_last == "하" and r_jung in ("ㅓ", "ㅕ"):
        # e.g. 하어요 -> 해요, 하여요 -> 해요, 하었어요 -> 했어요  -> 하였어요 -> 했어요
        left = left[:-1] + compose(l_cho, "ㅐ", r_jong)
        left += right[1:]
        log = l_last, r_first, left, f"`하`+ (`ㅓ` 또는 `ㅕ`) -> `해`"
    elif l_jung == "ㅏ" and r_first == "의":
        # e.g. 나의 -> 내 ("내"가 더 많이 쓰이므로)
        left = left[:-1] + compose(l_cho, "ㅐ", " ")
        log = l_last, r_first, left, f"`ㅏ`+ `의` -> `ㅐ`"
    elif l_jung == "ㅓ" and r_first == "의":
        # e.g. 저의 -> 제 ("제"가 더 많이 쓰이므로)
        left = left[:-1] + compose(l_cho, "ㅔ", " ")
        log = l_last, r_first, left, f"`ㅓ`+ `의` -> `ㅔ`"
    elif l_jung == "ㅓ" and l_jong == " " and r_first == "이":
        # e.g. 거이죠 -> 거죠?
        left += right[1:]
        log = l_last, r_first, left, f"ㅓ+ 이 -> ㅓ (이 탈락)"
    elif l_jong == "ㄷ" and r_cho == "ㅇ":
        # e.g. 깨닫아 -> 깨달아
        left = left[:-1] + compose(l_cho, l_jung, "ㄹ")
        left += right
        log = l_last, r_first, left, f"`ㄷ` 종성 + `ㅇ` 초성 -> `ㄹ` 종성"
    elif l_jung == "ㅏ" and l_jong == " " and r_first == "어":
        left += right[1:]
        log = l_last, r_first, left, f"동모음 탈락"
    else:
        # rely on soynlp for the remaining cases
        # always pop the shortest one (e.g. 마시어, 마셔, 둘 중 하나일 경우 마셔를 선택)
        # warning - popping an element from the set maybe non-deterministic
        left = min(soy_conjugate(left, right), key=lambda x: len(x))
        # TODO: logging with logging module
        log = l_last, r_first, left, f"conjugations done by soynlp"

    return left, log
