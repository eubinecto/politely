from politely import style
from politely.stylers import _preprocess  # noqa
import pytest


def test_preprocess():
    sent = "이것은 예시 문장이다"
    out = _preprocess(sent)
    assert "이것은 예시 문장이다.", out
    sent = "이것은 예시 문장이다."
    out = _preprocess(sent)
    assert "이것은 예시 문장이다.", out


def test_preprocess_trailing_spaces():
    sent = "이것은 예시 문장이다  "
    out = _preprocess(sent)
    assert "이것은 예시 문장이다.", out
    sent = "이것은 예시 문장이다. "
    out = _preprocess(sent)
    assert "이것은 예시 문장이다.", out


def test_honorify_ra():
    """
    종결어미 -라
    """
    sent = "최선을 다하라."
    assert "최선을 다하라.", style(sent, 1)
    assert "최선을 다하세요.", style(sent, 2)
    assert "최선을 다합시다.", style(sent, 3)


def test_honorify_ja():
    """
    종결어미 -자
    """
    sent = "자 이제 먹자."
    assert "자 이제 먹자.", style(sent, 1)
    assert "자 이제 먹어요.", style(sent, 2)
    assert "자 이제 먹읍시다.", style(sent, 3)


def test_honorify_nieun_dae():
    """
    종결어미 ㄴ대
    """
    sent = "밥먹고 누우면 안 된대."
    assert "밥먹고 누우면 안 된대.", style(sent, 1)
    assert "밥먹고 누우면 안 된대요.", style(sent, 2)
    assert "밥먹고 누우면 안 된답니다.", style(sent, 3)


def test_honorify_nieun_dae_yo():
    """
    종결어미 ㄴ대요
    """
    sent = "밥먹고 누우면 안 된대요."
    assert "밥먹고 누우면 안 된대.", style(sent, 1)
    assert "밥먹고 누우면 안 된대요.", style(sent, 2)
    assert "밥먹고 누우면 안 된답니다.", style(sent, 3)


def test_honorify_gae():
    sent = "회의를 시작할게."
    assert "회의를 시작할게.", style(sent, 1)
    assert "회의를 시작할게요.", style(sent, 2)
    assert "회의를 시작하겠습니다.", style(sent, 3)


def test_honorify_eo():
    """
    종결어미 -어
    """
    sent = "그 일은 내가 처리했어."
    assert "그 일은 내가 처리했어.", style(sent, 1)
    assert "그 일은 제가 처리했어요.", style(sent, 2)
    assert "그 일은 제가 처리했습니다.", style(sent, 3)


def test_honorify_yo():
    """
    종결어미 -요
    """
    sent = "제 패션을 함부로 비꼬지마요"
    assert "내 패션을 함부로 비꼬지마.", style(sent, 1)
    assert "제 패션을 함부로 비꼬지마요.", style(sent, 2)
    assert "제 패션을 함부로 비꼬지마십시오.", style(sent, 3)


def test_honorify_ge_yo():
    """
    게 + 종결어미 -요
    """
    sent = "회의를 시작할게요."
    assert "회의를 시작할게.", style(sent, 1)
    assert "회의를 시작할게요.", style(sent, 2)
    assert "회의를 시작하겠습니다.", style(sent, 3)


def test_honorify_yi_ya():
    """
    이+야
    """
    sent = "그 일은 내 담당이야."
    assert "그 일은 내 담당이야.", style(sent, 1)
    assert "그 일은 제 담당이에요.", style(sent, 2)
    assert "그 일은 제 담당입니다.", style(sent, 3)


def test_honorify_se_yo():
    """
    세+요
    """
    # 이미 규칙으로 존재하는 -세요 때문에 얘는 달라져야함
    sent = "최선을 다하세요."
    assert "최선을 다해.", style(sent, 1)
    assert "최선을 다하세요.", style(sent, 2)
    assert "최선을 다하십시오.", style(sent, 3)


def test_honorify_yi_eyo():
    """
    이 + 에요
    """
    sent = "그 일은 제 담당이에요."
    assert "그 일은 내 담당이야.", style(sent, 1)
    assert "그 일은 제 담당이에요.", style(sent, 2)
    assert "그 일은 제 담당입니다.", style(sent, 3)


def test_honorify_eu_yo_1():
    """
    종결어미 -어요 (1)
    """
    sent = "자 이제 먹어요."
    assert "자 이제 먹어.", style(sent, 1)
    assert "자 이제 먹어요.", style(sent, 2)
    assert "자 이제 먹습니다.", style(sent, 3)


def test_honorify_eu_yo_2():
    """
    종결어미 -어요 (2)
    """
    sent = "그 일은 제가 처리했어요."
    assert "그 일은 내가 처리했어.", style(sent, 1)
    assert "그 일은 제가 처리했어요.", style(sent, 2)
    assert "그 일은 제가 처리했습니다.", style(sent, 3)


def test_honorify_bo_ayo():
    """
    보 + 종결어미 -아요
    """
    sent = "좀만 더 버텨봐요"
    assert "좀만 더 버텨봐.", style(sent, 1)
    assert "좀만 더 버텨봐요.", style(sent, 2)
    assert "좀만 더 버텨봅시다.", style(sent, 3)


def test_honorify_ma():
    sent = "내 패션을 함부로 비꼬지마"
    assert "내 패션을 함부로 비꼬지마.", style(sent, 1)
    assert "제 패션을 함부로 비꼬지마요.", style(sent, 2)
    assert "제 패션을 함부로 비꼬지마십시오.", style(sent, 3)


def test_honorify_bo_a():
    sent = "좀만 더 버텨봐"
    assert "좀만 더 버텨봐.", style(sent, 1)
    assert "좀만 더 버텨봐요.", style(sent, 2)
    assert "좀만 더 버텨봅시다.", style(sent, 3)


def test_honorify_dae_q():
    sent = "걔 오늘 기분이 왜 이렇게 좋대?"
    assert "걔 오늘 기분이 왜 이렇게 좋대?", style(sent, 1)
    assert "걔 오늘 기분이 왜 이렇게 좋대요?", style(sent, 2)
    assert "걔 오늘 기분이 왜 이렇게 좋습니까?", style(sent, 3)


def test_honorify_dae_yo_q():
    sent = "걔 오늘 기분이 왜 이렇게 좋대요?"
    assert "걔 오늘 기분이 왜 이렇게 좋대?", style(sent, 1)
    assert "걔 오늘 기분이 왜 이렇게 좋대요?", style(sent, 2)
    assert "걔 오늘 기분이 왜 이렇게 좋습니까?", style(sent, 3)


def test_honorify_eo_q():
    """
    어?
    """
    # 했어?
    sent = "어제 공부는 마무리 했어?"
    assert "어제 공부는 마무리 했어?", style(sent, 1)
    assert "어제 공부는 마무리 했어요?", style(sent, 2)
    assert "어제 공부는 마무리 했습니까?", style(sent, 3)


def test_honorify_eo_yo_q_1():
    """
    의문형 종결어미 -어요? (1)
    """
    sent = "어제 공부는 마무리 했어요?"
    assert "어제 공부는 마무리 했어?", style(sent, 1)
    assert "어제 공부는 마무리 했어요?", style(sent, 2)
    assert "어제 공부는 마무리 했습니까?", style(sent, 3)


def test_honorify_eo_yo_q_2():
    """
    의문형 종결어미 -어요 (2)
    """
    sent = "어디 가세요?"
    assert "어디 가셔?", style(sent, 1)
    assert "어디 가세요?", style(sent, 2)
    assert "어디 가십니까?", style(sent, 3)


def test_honorify_si_eo_q():
    """
    시 + 의문형 종결어미 -어?
    """
    # 가셔? (가시어?)
    sent = "어디 가셔?"
    assert "어디 가셔?", style(sent, 1)
    assert "어디 가셔요?", style(sent, 2)
    assert "어디 가십니까?", style(sent, 3)


def test_honorify_ddae_q():
    sent = "순서를 바꾸는건 어때?"
    assert "순서를 바꾸는건 어때?", style(sent, 1)
    assert "순서를 바꾸는건 어때요?", style(sent, 2)
    assert "순서를 바꾸는건 어떻습니까?", style(sent, 3)
    sent = "순서를 바꾸는건 어때요?"
    assert "순서를 바꾸는건 어때?", style(sent, 1)
    assert "순서를 바꾸는건 어때요?", style(sent, 2)
    assert "순서를 바꾸는건 어떻습니까?", style(sent, 3)


# --- tests by irregular conjugations --- #
def test_conjugate_ah_1():
    """
    동모음 탈락
    걸어가어요 (x)
    걸어가요 (o)
    """
    sent = "가까우니까 걸어가자."
    assert "가까우니까 걸어가자.", style(sent, 1)
    assert "가까우니까 걸어가요.", style(sent, 2)
    assert "가까우니까 걸어갑시다.", style(sent, 3)


def test_conjugate_ah_2():
    """
    동모음 탈락
    떠나어요 (x)
    떠나요 (o)
    """
    sent = "자, 떠나자. 동해바다로."
    assert "자, 떠나자. 동해바다로.", style(sent, 1)
    assert "자, 떠나요. 동해바다로.", style(sent, 2)
    assert "자, 떠납시다. 동해바다로.", style(sent, 3)


def test_conjugate_ah_3():
    """
    동모음 탈락 (3)
    """
    sent = "자, 떠나요. 동해바다로."
    assert "자, 떠나. 동해바다로.", style(sent, 1)
    assert "자, 떠나요. 동해바다로.", style(sent, 2)
    assert "자, 떠납니다. 동해바다로.", style(sent, 3)


def test_conjugate_digud():
    """
    ㄷ 불규칙
    """
    sent = "나는 오늘 그 사실을 깨달았다."
    assert "나는 오늘 그 사실을 깨달았다.", style(sent, 1)
    assert "저는 오늘 그 사실을 깨달았어요.", style(sent, 2)
    assert "저는 오늘 그 사실을 깨달았습니다.", style(sent, 3)
    sent = "저는 오늘 그 사실을 깨달았어요."
    assert "나는 오늘 그 사실을 깨달았어.", style(sent, 1)
    assert "저는 오늘 그 사실을 깨달았어요.", style(sent, 2)
    assert "저는 오늘 그 사실을 깨달았습니다.", style(sent, 3)


def test_conjugate_ru():
    """
    르 불규칙
    e.g. 들르 + 어 -> 들러
    e.g. 이르 + 어  -> 일러
    """
    sent = "나는 그 상점을 들렀다."
    assert "나는 그 상점을 들렀다.", style(sent, 1)
    assert "저는 그 상점을 들렀어요.", style(sent, 2)
    assert "저는 그 상점을 들렀습니다.", style(sent, 3)
    sent = "저는 그 상점을 들렀어요."
    assert "나는 그 상점을 들렀어.", style(sent, 1)
    assert "저는 그 상점을 들렀어요.", style(sent, 2)
    assert "저는 그 상점을 들렀습니다.", style(sent, 3)
    sent = "지금은 좀 일러."
    assert "지금은 좀 일러.", style(sent, 1)
    assert "지금은 좀 일러요.", style(sent, 2)
    assert "지금은 좀 이릅니다.", style(sent, 3)


def test_conjugate_bieup_1():
    """
    ㅂ 불규칙 (모음 조화 o)
    """
    sent = "모래가 참 고와."
    assert "모래가 참 고와.", style(sent, 1)
    assert "모래가 참 고와요.", style(sent, 2)
    assert "모래가 참 곱습니다.", style(sent, 3)
    sent = "모래가 참 고와요."
    assert "모래가 참 고와.", style(sent, 1)
    assert "모래가 참 고와요.", style(sent, 2)
    assert "모래가 참 곱습니다.", style(sent, 3)


def test_conjugate_bieup_2():
    """
    ㅂ 불규칙 (모음 조화 x)
    """
    sent = "참 아름답다."
    assert "참 아름답다.", style(sent, 1)
    assert "참 아름다워요.", style(sent, 2)
    assert "참 아름답습니다.", style(sent, 3)
    sent = "참 아름다워요."
    assert "참 아름다워.", style(sent, 1)
    assert "참 아름다워요.", style(sent, 2)
    assert "참 아름답습니다.", style(sent, 3)


def test_conjugate_bieup_3():
    """
    더워의 경우.
    """
    sent = "오늘이 어제보다 더워."
    assert "오늘이 어제보다 더워.", style(sent, 1)
    assert "오늘이 어제보다 더워요.", style(sent, 2)
    assert "오늘이 어제보다 덥습니다.", style(sent, 3)
    sent = "오늘이 어제보다 더워요."
    assert "오늘이 어제보다 더워.", style(sent, 1)
    assert "오늘이 어제보다 더워요.", style(sent, 2)
    assert "오늘이 어제보다 덥습니다.", style(sent, 3)


def test_conjugate_bieup_4():
    """
    가려워의 경우.
    """
    sent = "너무 가려워."
    assert "너무 가려워.", style(sent, 1)
    assert "너무 가려워요.", style(sent, 2)
    assert "너무 가렵습니다.", style(sent, 3)
    sent = "너무 가려워요."
    assert "너무 가려워.", style(sent, 1)
    assert "너무 가려워요.", style(sent, 2)
    assert "너무 가렵습니다.", style(sent, 3)


def test_conjugate_r_cho_is_bieup():
    """
    ㅂ니다
    """
    sent = "이름은 김유빈이야."
    assert "이름은 김유빈입니다.", style(sent, 3)
    sent = "이름은 김유빈이에요."
    assert "이름은 김유빈입니다.", style(sent, 3)


def test_conjugate_siot():
    """
    ㅅ 불규칙
    """
    sent = "거기에 선을 그어."
    assert "거기에 선을 그어.", style(sent, 1)
    assert "거기에 선을 그어요.", style(sent, 2)
    assert "거기에 선을 긋습니다.", style(sent, 3)
    sent = "거기에 선을 그어요."
    assert "거기에 선을 그어.", style(sent, 1)
    assert "거기에 선을 그어요.", style(sent, 2)
    assert "거기에 선을 긋습니다.", style(sent, 3)


def test_conjugate_siot_exception():
    """
    ㅅ 불규칙 (벗어는 예외)
    """
    sent = "한국의 목욕탕에서는 옷을 벗어."
    assert "한국의 목욕탕에서는 옷을 벗어.", style(sent, 1)
    assert "한국의 목욕탕에서는 옷을 벗어요.", style(sent, 2)
    assert "한국의 목욕탕에서는 옷을 벗습니다.", style(sent, 3)
    sent = "한국의 목욕탕에서는 옷을 벗어요."
    assert "한국의 목욕탕에서는 옷을 벗어.", style(sent, 1)
    assert "한국의 목욕탕에서는 옷을 벗어요.", style(sent, 2)
    assert "한국의 목욕탕에서는 옷을 벗습니다.", style(sent, 3)


def test_conjugate_u():
    """
    우 불규칙
    """
    sent = "이 포스팅 퍼갈게."
    assert "이 포스팅 퍼갈게.", style(sent, 1)
    assert "이 포스팅 퍼갈게요.", style(sent, 2)
    assert "이 포스팅 퍼가겠습니다.", style(sent, 3)
    sent = "이 포스팅 퍼갈게요."
    assert "이 포스팅 퍼갈게.", style(sent, 1)
    assert "이 포스팅 퍼갈게요.", style(sent, 2)
    assert "이 포스팅 퍼가겠습니다.", style(sent, 3)


def test_conjugate_u_jup():
    """
    우 불규칙 - 줍은 예외
    """
    sent = "쓰레기를 줍자."
    assert "쓰레기를 줍자.", style(sent, 1)
    assert "쓰레기를 주워요.", style(sent, 2)
    assert "쓰레기를 주웁시다.", style(sent, 3)
    sent = "쓰레기를 주워요."
    assert "쓰레기를 주워.", style(sent, 1)
    assert "쓰레기를 주워요.", style(sent, 2)
    assert "쓰레기를 줍습니다.", style(sent, 3)


def test_conjugate_o():
    """
    오 불규칙
    """
    sent = "오늘 제주도로 여행왔어."
    assert "오늘 제주도로 여행왔어.", style(sent, 1)
    assert "오늘 제주도로 여행왔어요.", style(sent, 2)
    assert "오늘 제주도로 여행왔습니다.", style(sent, 3)
    sent = "오늘 제주도로 여행왔어요."
    assert "오늘 제주도로 여행왔어.", style(sent, 1)
    assert "오늘 제주도로 여행왔어요.", style(sent, 2)
    assert "오늘 제주도로 여행왔습니다.", style(sent, 3)


def test_conjugate_drop_ue():
    """
    으 탈락 불규칙
    """
    sent = "전등을 껐다."
    assert "전등을 껐다.", style(sent, 1)
    assert "전등을 껐어요.", style(sent, 2)
    assert "전등을 껐습니다.", style(sent, 3)
    sent = "전등을 껐어요."
    assert "전등을 껐어.", style(sent, 1)
    assert "전등을 껐어요.", style(sent, 2)
    assert "전등을 껐습니다.", style(sent, 3)


def test_conjugate_gara():
    """
    -가라 불규칙
    """
    sent = "저기로 가거라."
    assert "저기로 가거라.", style(sent, 1)
    assert "저기로 가세요.", style(sent, 2)
    assert "저기로 가십시오.", style(sent, 3)
    sent = "저기로 가세요."
    assert "저기로 가셔.", style(sent, 1)
    assert "저기로 가세요.", style(sent, 2)
    assert "저기로 가십시오.", style(sent, 3)


def test_conjugate_neura():
    """
    -너라 불규칙
    """
    sent = "이리 오너라."
    assert "이리 오너라.", style(sent, 1)
    assert "이리 오세요.", style(sent, 2)
    assert "이리 오십시오.", style(sent, 3)
    sent = "이리 오세요."
    assert "이리 오셔.", style(sent, 1)
    assert "이리 오세요.", style(sent, 2)
    assert "이리 오십시오.", style(sent, 3)


def test_conjugate_yue():
    """
    -여 불규칙
    """
    sent = "나는 그리하지 아니하였다."
    assert "나는 그리하지 아니하였다.", style(sent, 1)
    assert "저는 그리하지 아니했어요.", style(sent, 2)
    assert "저는 그리하지 아니했습니다.", style(sent, 3)
    sent = "저는 그리하지 아니하였어요."
    assert "나는 그리하지 아니했어.", style(sent, 1)
    assert "저는 그리하지 아니하였어요.", style(sent, 2)
    assert "저는 그리하지 아니했습니다.", style(sent, 3)


def test_conjugate_drop_hiut():
    """
    ㅎ 탈락
    """
    sent = "하늘이 파랗다."
    assert "하늘이 파랗다.", style(sent, 1)
    assert "하늘이 파래요.", style(sent, 2)
    assert "하늘이 파랗습니다.", style(sent, 3)
    sent = "하늘이 파래요."
    assert "하늘이 파래.", style(sent, 1)
    assert "하늘이 파래요.", style(sent, 2)
    assert "하늘이 파랗습니다.", style(sent, 3)


def test_conjugate_drop_yi():
    """
    ㅓ + 이.
    """
    sent = "이렇게 하는 거야?"
    assert "이렇게 하는 거야?", style(sent, 1)
    assert "이렇게 하는 거죠?", style(sent, 2)
    assert "이렇게 하는 겁니까?", style(sent, 3)
    sent = "이렇게 하는 거죠?"
    assert "이렇게 하는 거야?", style(sent, 1)
    assert "이렇게 하는 거죠?", style(sent, 2)
    assert "이렇게 하는 겁니까?", style(sent, 3)


# --- known issues --- #
@pytest.mark.skip("추가할만한 기능 (1): 밥 -> 진지")
def test_more_1():
    sent = "밥 먹어"
    assert "밥 먹어.", style(sent, 1)
    assert "밥 먹어요", style(sent, 2)
    assert "진지 잡수세요", style(sent, 3)


@pytest.mark.skip("추가할만한 기능 (2): 존대를 할 때는 주어를 생략할 때가 있다")
def test_more_2():
    sent = "자네만 믿고 있겠네"
    # 만약.. 들어오는 입력이 반말이라면, 굳이 반말인 경우를 수정할 필요가 없다.
    assert "자네만 믿고 있겠네.", style(sent, 1)
    assert "믿고 있겠어요.", style(sent, 2)
    assert "믿고 있겠습니다.", style(sent, 3)


@pytest.mark.skip()
def test_khaiii_error_1():
    """
    이건 khaiii에서의 문제다.
    "줍"만을 어간으로 추출해야하는데 알 수 없는 이유로 그렇게 되지 않는다.
    결과적으로,
    줍웠 + 어
    만을 고려하게된다. 그래서 ㅂ 블규칙이 적용되지 않음.
    """
    sent = "길가다가 동전을 주웠어."
    assert "길가다가 동전을 주웠어.", style(sent, 1)
    assert "길가다가 동전을 주웠어요.", style(sent, 2)
    assert "길가다가 동전을 주웠습니다.", style(sent, 3)
    sent = "길가다가 동전을 주웠어요."  # 아... 줍우... 줍이 아니라.. 줍우..
    assert "길가다가 동전을 주웠어.", style(sent, 1)
    assert "길가다가 동전을 주웠어요.", style(sent, 2)
    assert "길가다가 동전을 주웠습니다.", style(sent, 3)


@pytest.mark.skip()
def test_khaiii_error_2():
    """
    이것도 khaiii에서의 문제다.
    걷어를 맥락을 고려하지 않고 무조건적으로 걸어로 분석한다.
    """
    sent = "이참에 돈을 걷어가자."
    assert "이참에 돈을 걷어가자.", style(sent, 1)
    assert "이참에 돈을 걷어가요.", style(sent, 2)
    assert "이참에 돈을 걷어갑시다.", style(sent, 3)


@pytest.mark.skip()
def test_khaiii_error_3():
    sent = "가까우니까 걸어가요."
    assert "가까우니까 걸어가자.", style(sent, 1)
    assert "가까우니까 걸어가요.", style(sent, 2)
    assert "가까우니까 걸어갑시다.", style(sent, 3)


@pytest.mark.skip()
def test_contextual_1():
    # 이런 식으로 맥락이 필요한 경우도 대응이 어렵다. (존대 종결어미 선정에 맥락이 관여하는 경우)
    # 이제, 밥을 등, 단어 선택에 따라 formal의 형태가 달라지는데, 이것에 대응하는 것은 불가능하다.
    # 맥락이 필요하다. 오직 규칙만으로는 불가능하다.
    sent = "자 이제 먹어요."
    assert "자 이제 먹읍시다", style(sent, 3)
    sent = "전 밥을 먹어요."
    assert "전 밥을 먹습니다", style(sent, 3)


@pytest.mark.skip()
def test_contextual_2():
    """
    -르 불규칙 (conjugation 규칙에 맥락이 관여하는 경우)
    e.g. 이르 + 어 -> 이르러
    e.g.
    이건 -러 불규칙과 구분히 불가능하다. 나중에 맥락까지 고려할 수 있게된다면 그 때 해보자.
    여기 이슈참고: https://github.com/eubinecto/politely/issues/56#issue-1233231686
    """
    sent = "하지말라고 일렀다."
    assert "하지말라고 일렀다.", style(sent, 1)
    assert "하지말라고 일렀어요.", style(sent, 2)
    assert "하지말라고 일렀습니다.", style(sent, 3)
    sent = "드디어 정상에 이르렀다."
    assert "드디어 정상에 이르렀다.", style(sent, 1)
    assert "드디어 정상에 이르렀어요.", style(sent, 2)
    assert "드디어 정상에 이르렀습니다.", style(sent, 3)


@pytest.mark.skip()
def test_contextual_3():
    """
    쓰레기를 주워요 -> 쓰레기를 주웁시다 / 쓰레기를 줍습니다 (존대 종결어미 선정에 맥락이 관여하는 경우)
    둘다 가능하다. 이 경우는 맥락이 필요하다. 규칙만으로는 불가능하다.
    # 자세한 설명: https://github.com/eubinecto/politely/issues/60#issuecomment-1126839221
    """
    sent = "저는 쓰레기를 주워요."
    assert "나는 쓰레기를 주워.", style(sent, 1)
    assert "저는 쓰레기를 주워요.", style(sent, 2)
    assert "저는 쓰레기를 줍습니다.", style(sent, 3)
    sent = "같이 쓰레기를 주워요."
    assert "같이 쓰레기를 줍자.", style(sent, 1)
    assert "같이 쓰레기를 주워요.", style(sent, 2)
    assert "같이 쓰레기를 주웁시다.", style(sent, 3)


@pytest.mark.skip()
def test_contextual_4():
    """
    이것도 마찬가지로 맥락이 필요하다.
    떠나요 -> 떠나 / 떠나자, 둘 중 무엇이 정답인지는 맥락을 보아야만 알 수 있다.
    떠나요 -> 떠납니다 / 떠납시다 -> 둘 중 무엇이 맞는지도... 마찬가지
    """
    sent = "자, 떠나요. 동해바다로."
    assert "자, 떠나자. 동해바다로.", style(sent, 1)
    assert "자, 떠나요. 동해바다로.", style(sent, 2)
    assert "자, 떠납시다. 동해바다로.", style(sent, 3)
