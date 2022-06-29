from politely import Styler
import pytest  # noqa
from politely.errors import EFNotIncludedError, EFNotSupportedError


@pytest.fixture(scope="session")
def styler():
    return Styler()


def test_preprocess(styler):
    sent = "이것은 예시 문장이다"
    styler.preprocess(sent)
    assert "이것은 예시 문장이다." == styler.out
    sent = "이것은 예시 문장이다."
    styler.preprocess(sent)
    assert "이것은 예시 문장이다." == styler.out


def test_preprocess_trailing_spaces(styler):
    sent = "이것은 예시 문장이다  "
    styler.preprocess(sent)
    assert "이것은 예시 문장이다." == styler.out
    sent = "이것은 예시 문장이다. "
    styler.preprocess(sent)
    assert "이것은 예시 문장이다." == styler.out


def test_check_ef_not_included_error(styler):
    sent = "가나다라마바사"
    with pytest.raises(EFNotIncludedError):
        styler.setup().preprocess(sent).analyze().check()


def test_check_ef_not_supported_error(styler):
    sent = "용서해주소서"
    with pytest.raises(EFNotSupportedError):
        styler.setup().preprocess(sent).analyze().check()


def test_honorify_ra(styler):
    """
    종결어미 -라
    """
    sent = "최선을 다하라."
    assert "최선을 다하라." == styler(sent, 1)
    assert "최선을 다하세요." == styler(sent, 2)
    assert "최선을 다합시다." == styler(sent, 3)


def test_honorify_ja(styler):
    """
    종결어미 -자
    """
    sent = "자 이제 먹자."
    assert "자 이제 먹자." == styler(sent, 1)
    assert "자 이제 먹어요." == styler(sent, 2)
    assert "자 이제 먹읍시다." == styler(sent, 3)


def test_honorify_nieun_dae(styler):
    """
    종결어미 ㄴ대
    """
    sent = "밥 먹고 누우면 안 된대."
    assert "밥 먹고 누우면 안 된대." == styler(sent, 1)
    assert "밥 먹고 누우면 안 된대요." == styler(sent, 2)
    assert "밥 먹고 누우면 안 된답니다." == styler(sent, 3)


def test_honorify_nieun_dae_yo(styler):
    """
    종결어미 ㄴ대요
    """
    sent = "밥 먹고 누우면 안 된대요."
    assert "밥 먹고 누우면 안 된대." == styler(sent, 1)
    assert "밥 먹고 누우면 안 된대요." == styler(sent, 2)
    assert "밥 먹고 누우면 안 된답니다." == styler(sent, 3)


def test_honorify_gae(styler):
    sent = "회의를 시작할게."
    assert "회의를 시작할게." == styler(sent, 1)
    assert "회의를 시작할게요." == styler(sent, 2)
    assert "회의를 시작하겠습니다." == styler(sent, 3)


def test_honorify_eo(styler):
    """
    종결어미 -어
    """
    sent = "그 일은 내가 처리했어."
    assert "그 일은 내가 처리했어." == styler(sent, 1)
    assert "그 일은 제가 처리했어요." == styler(sent, 2)
    assert "그 일은 제가 처리했습니다." == styler(sent, 3)


def test_honorify_yo(styler):
    """
    종결어미 -요
    """
    sent = "제 패션을 함부로 비꼬지 마요."
    assert "내 패션을 함부로 비꼬지 마." == styler(sent, 1)
    assert "제 패션을 함부로 비꼬지 마요." == styler(sent, 2)
    assert "제 패션을 함부로 비꼬지 마십시오." == styler(sent, 3)


def test_honorify_ge_yo(styler):
    """
    게 + 종결어미 -요
    """
    sent = "회의를 시작할게요."
    assert "회의를 시작할게." == styler(sent, 1)
    assert "회의를 시작할게요." == styler(sent, 2)
    assert "회의를 시작하겠습니다." == styler(sent, 3)


def test_honorify_yi_ya(styler):
    """
    이+야
    """
    sent = "그 일은 내 담당이야."
    assert "그 일은 내 담당이야." == styler(sent, 1)
    assert "그 일은 제 담당예요." == styler(sent, 2)
    assert "그 일은 제 담당입니다." == styler(sent, 3)


def test_honorify_se_yo(styler):
    """
    세+요
    """
    # 이미 규칙으로 존재하는 -세요 때문에 얘는 달라져야함
    sent = "최선을 다 하세요."
    assert "최선을 다 해." == styler(sent, 1)
    assert "최선을 다 하세요." == styler(sent, 2)
    assert "최선을 다 하십시오." == styler(sent, 3)


def test_honorify_yi_eyo(styler):
    """
    이 + 에요
    """
    sent = "그 일은 제 담당예요."
    assert "그 일은 내 담당이야." == styler(sent, 1)
    assert "그 일은 제 담당예요." == styler(sent, 2)
    assert "그 일은 제 담당입니다." == styler(sent, 3)


def test_honorify_eu_yo_1(styler):
    """
    종결어미 -어요 (1)
    """
    sent = "자 이제 먹어요."
    assert "자 이제 먹어." == styler(sent, 1)
    assert "자 이제 먹어요." == styler(sent, 2)
    assert "자 이제 먹습니다." == styler(sent, 3)


def test_honorify_eu_yo_2(styler):
    """
    종결어미 -어요 (2)
    """
    sent = "그 일은 제가 처리했어요."
    assert "그 일은 내가 처리했어." == styler(sent, 1)
    assert "그 일은 제가 처리했어요." == styler(sent, 2)
    assert "그 일은 제가 처리했습니다." == styler(sent, 3)


def test_honorify_bo_ayo(styler):
    """
    보 + 종결어미 -아요
    """
    sent = "좀만 더 버텨 봐요"
    assert "좀만 더 버텨 봐." == styler(sent, 1)
    assert "좀만 더 버텨 봐요." == styler(sent, 2)
    assert "좀만 더 버텨 봅시다." == styler(sent, 3)


def test_honorify_ma(styler):
    sent = "내 패션을 함부로 비꼬지 마"
    assert "내 패션을 함부로 비꼬지 마." == styler(sent, 1)
    assert "제 패션을 함부로 비꼬지 마요." == styler(sent, 2)
    assert "제 패션을 함부로 비꼬지 마십시오." == styler(sent, 3)


def test_honorify_bo_a(styler):
    sent = "좀만 더 버텨 봐"
    assert "좀만 더 버텨 봐." == styler(sent, 1)
    assert "좀만 더 버텨 봐요." == styler(sent, 2)
    assert "좀만 더 버텨 봅시다." == styler(sent, 3)


def test_honorify_dae_q(styler):
    sent = "걔 오늘 기분이 왜 이렇게 좋대?"
    assert "걔 오늘 기분이 왜 이렇게 좋대?" == styler(sent, 1)
    assert "걔 오늘 기분이 왜 이렇게 좋대요?" == styler(sent, 2)
    assert "걔 오늘 기분이 왜 이렇게 좋답니까?" == styler(sent, 3)


def test_honorify_dae_yo_q(styler):
    sent = "걔 오늘 기분이 왜 이렇게 좋대요?"
    assert "걔 오늘 기분이 왜 이렇게 좋대?" == styler(sent, 1)
    assert "걔 오늘 기분이 왜 이렇게 좋대요?" == styler(sent, 2)
    assert "걔 오늘 기분이 왜 이렇게 좋답니까?" == styler(sent, 3)


def test_honorify_eo_q(styler):
    """
    어?
    """
    # 했어?
    sent = "어제 공부는 마무리했어?"
    assert "어제 공부는 마무리했어?" == styler(sent, 1)
    assert "어제 공부는 마무리했어요?" == styler(sent, 2)
    assert "어제 공부는 마무리했습니까?" == styler(sent, 3)


def test_honorify_eo_yo_q_1(styler):
    """
    의문형 종결어미 -어요? (1)
    """
    sent = "어제 공부는 마무리했어요?"
    assert "어제 공부는 마무리했어?" == styler(sent, 1)
    assert "어제 공부는 마무리했어요?" == styler(sent, 2)
    assert "어제 공부는 마무리했습니까?" == styler(sent, 3)


def test_honorify_eo_yo_q_2(styler):
    """
    의문형 종결어미 -어요 (2)
    """
    sent = "어디 가세요?"
    assert "어디 가?" == styler(sent, 1)
    assert "어디 가세요?" == styler(sent, 2)
    assert "어디 가십니까?" == styler(sent, 3)


def test_honorify_ga(styler):
    """
    시 + 의문형 종결어미 -어?
    """
    # 가셔? (가시어?)
    sent = "어디 가?"
    assert "어디 가?" == styler(sent, 1)
    assert "어디 가요?" == styler(sent, 2)
    assert "어디 갑니까?" == styler(sent, 3)


def test_honorify_ddae_q(styler):
    sent = "순서를 바꾸는 거는 어때?"
    assert "순서를 바꾸는 거는 어때?" == styler(sent, 1)
    assert "순서를 바꾸는 거는 어때요?" == styler(sent, 2)
    assert "순서를 바꾸는 거는 어떻습니까?" == styler(sent, 3)
    sent = "순서를 바꾸는 거는 어때요?"
    assert "순서를 바꾸는 거는 어때?" == styler(sent, 1)
    assert "순서를 바꾸는 거는 어때요?" == styler(sent, 2)
    assert "순서를 바꾸는 거는 어떻습니까?" == styler(sent, 3)


# --- tests by irregular conjugations --- #
def test_conjugate_ah_1(styler):
    """
    동모음 탈락
    걸어가어요 (x)
    걸어가요 (o)
    """
    sent = "가까우니까 걸어가자."
    assert "가까우니까 걸어가자." == styler(sent, 1)
    assert "가까우니까 걸어가요." == styler(sent, 2)
    assert "가까우니까 걸어갑시다." == styler(sent, 3)


def test_conjugate_ah_2(styler):
    """
    동모음 탈락
    떠나어요 (x)
    떠나요 (o)
    """
    sent = "자, 떠나자. 동해 바다로."
    assert "자, 떠나자. 동해 바다로." == styler(sent, 1)
    assert "자, 떠나요. 동해 바다로." == styler(sent, 2)
    assert "자, 떠납시다. 동해 바다로." == styler(sent, 3)


def test_conjugate_ah_3(styler):
    """
    동모음 탈락 (3)
    """
    sent = "자, 떠나요. 동해 바다로."
    assert "자, 떠나. 동해 바다로." == styler(sent, 1)
    assert "자, 떠나요. 동해 바다로." == styler(sent, 2)
    assert "자, 떠납니다. 동해 바다로." == styler(sent, 3)


def test_conjugate_digud(styler):
    """
    ㄷ 불규칙
    """
    sent = "나는 오늘 그 사실을 깨달았다."
    assert "나는 오늘 그 사실을 깨달았다." == styler(sent, 1)
    assert "저는 오늘 그 사실을 깨달았어요." == styler(sent, 2)
    assert "저는 오늘 그 사실을 깨달았습니다." == styler(sent, 3)
    sent = "저는 오늘 그 사실을 깨달았어요."
    assert "나는 오늘 그 사실을 깨달았어." == styler(sent, 1)
    assert "저는 오늘 그 사실을 깨달았어요." == styler(sent, 2)
    assert "저는 오늘 그 사실을 깨달았습니다." == styler(sent, 3)


def test_conjugate_ru(styler):
    """
    르 불규칙
    e.g. 들르 + 어 -> 들러
    e.g. 이르 + 어  -> 일러
    """
    sent = "나는 그 상점을 들렀다."
    assert "나는 그 상점을 들렀다." == styler(sent, 1)
    assert "저는 그 상점을 들렀어요." == styler(sent, 2)
    assert "저는 그 상점을 들렀습니다." == styler(sent, 3)
    sent = "저는 그 상점을 들렀어요."
    assert "나는 그 상점을 들렀어." == styler(sent, 1)
    assert "저는 그 상점을 들렀어요." == styler(sent, 2)
    assert "저는 그 상점을 들렀습니다." == styler(sent, 3)
    sent = "지금은 좀 일러."
    assert "지금은 좀 일러." == styler(sent, 1)
    assert "지금은 좀 일러요." == styler(sent, 2)
    assert "지금은 좀 이릅니다." == styler(sent, 3)


def test_conjugate_bieup_1(styler):
    """
    ㅂ 불규칙 (모음 조화 o)
    """
    sent = "모래가 참 고와."
    assert "모래가 참 고와." == styler(sent, 1)
    assert "모래가 참 고와요." == styler(sent, 2)
    assert "모래가 참 곱습니다." == styler(sent, 3)
    sent = "모래가 참 고와요."
    assert "모래가 참 고와." == styler(sent, 1)
    assert "모래가 참 고와요." == styler(sent, 2)
    assert "모래가 참 곱습니다." == styler(sent, 3)


def test_conjugate_bieup_2(styler):
    """
    ㅂ 불규칙 (모음 조화 x)
    """
    sent = "참 아름답다."
    assert "참 아름답다." == styler(sent, 1)
    assert "참 아름다워요." == styler(sent, 2)
    assert "참 아름답습니다." == styler(sent, 3)
    sent = "참 아름다워요."
    assert "참 아름다워." == styler(sent, 1)
    assert "참 아름다워요." == styler(sent, 2)
    assert "참 아름답습니다." == styler(sent, 3)


def test_conjugate_bieup_3(styler):
    """
    더워의 경우.
    """
    sent = "오늘이 어제보다 더워."
    assert "오늘이 어제보다 더워." == styler(sent, 1)
    assert "오늘이 어제보다 더워요." == styler(sent, 2)
    assert "오늘이 어제보다 덥습니다." == styler(sent, 3)
    sent = "오늘이 어제보다 더워요."
    assert "오늘이 어제보다 더워." == styler(sent, 1)
    assert "오늘이 어제보다 더워요." == styler(sent, 2)
    assert "오늘이 어제보다 덥습니다." == styler(sent, 3)


def test_conjugate_bieup_4(styler):
    """
    가려워의 경우.
    """
    sent = "너무 가려워."
    assert "너무 가려워." == styler(sent, 1)
    assert "너무 가려워요." == styler(sent, 2)
    assert "너무 가렵습니다." == styler(sent, 3)
    sent = "너무 가려워요."
    assert "너무 가려워." == styler(sent, 1)
    assert "너무 가려워요." == styler(sent, 2)
    assert "너무 가렵습니다." == styler(sent, 3)


def test_conjugate_r_cho_is_bieup(styler):
    """
    ㅂ니다
    """
    sent = "이름은 김유빈이야."
    assert "이름은 김유빈입니다." == styler(sent, 3)
    sent = "이름은 김유빈이에요."
    assert "이름은 김유빈입니다." == styler(sent, 3)


def test_conjugate_siot(styler):
    """
    ㅅ 불규칙
    """
    sent = "거기에 선을 그어."
    assert "거기에 선을 그어." == styler(sent, 1)
    assert "거기에 선을 그어요." == styler(sent, 2)
    assert "거기에 선을 긋습니다." == styler(sent, 3)
    sent = "거기에 선을 그어요."
    assert "거기에 선을 그어." == styler(sent, 1)
    assert "거기에 선을 그어요." == styler(sent, 2)
    assert "거기에 선을 긋습니다." == styler(sent, 3)


def test_conjugate_siot_exception(styler):
    """
    ㅅ 불규칙 (벗어는 예외)
    """
    sent = "한국의 목욕탕에서는 옷을 벗어."
    assert "한국의 목욕탕에서는 옷을 벗어." == styler(sent, 1)
    assert "한국의 목욕탕에서는 옷을 벗어요." == styler(sent, 2)
    assert "한국의 목욕탕에서는 옷을 벗습니다." == styler(sent, 3)
    sent = "한국의 목욕탕에서는 옷을 벗어요."
    assert "한국의 목욕탕에서는 옷을 벗어." == styler(sent, 1)
    assert "한국의 목욕탕에서는 옷을 벗어요." == styler(sent, 2)
    assert "한국의 목욕탕에서는 옷을 벗습니다." == styler(sent, 3)


def test_conjugate_u(styler):
    """
    우 불규칙
    """
    sent = "이 포스팅 퍼 갈게."
    assert "이 포스팅 퍼 갈게." == styler(sent, 1)
    assert "이 포스팅 퍼 갈게요." == styler(sent, 2)
    assert "이 포스팅 퍼 가겠습니다." == styler(sent, 3)
    sent = "이 포스팅 퍼 갈게요."
    assert "이 포스팅 퍼 갈게." == styler(sent, 1)
    assert "이 포스팅 퍼 갈게요." == styler(sent, 2)
    assert "이 포스팅 퍼 가겠습니다." == styler(sent, 3)


def test_conjugate_u_jup(styler):
    """
    우 불규칙 - 줍은 예외
    """
    sent = "쓰레기를 줍자."
    assert "쓰레기를 줍자." == styler(sent, 1)
    assert "쓰레기를 주워요." == styler(sent, 2)
    assert "쓰레기를 주웁시다." == styler(sent, 3)
    sent = "쓰레기를 주워요."
    assert "쓰레기를 주워." == styler(sent, 1)
    assert "쓰레기를 주워요." == styler(sent, 2)
    assert "쓰레기를 줍습니다." == styler(sent, 3)


def test_conjugate_o(styler):
    """
    오 불규칙
    """
    sent = "오늘 제주도로 여행 왔어."
    assert "오늘 제주도로 여행 왔어." == styler(sent, 1)
    assert "오늘 제주도로 여행 왔어요." == styler(sent, 2)
    assert "오늘 제주도로 여행 왔습니다." == styler(sent, 3)
    sent = "오늘 제주도로 여행 왔어요."
    assert "오늘 제주도로 여행 왔어." == styler(sent, 1)
    assert "오늘 제주도로 여행 왔어요." == styler(sent, 2)
    assert "오늘 제주도로 여행 왔습니다." == styler(sent, 3)


def test_conjugate_drop_ue(styler):
    """
    으 탈락 불규칙
    """
    sent = "전등을 껐다."
    assert "전등을 껐다." == styler(sent, 1)
    assert "전등을 껐어요." == styler(sent, 2)
    assert "전등을 껐습니다." == styler(sent, 3)
    sent = "전등을 껐어요."
    assert "전등을 껐어." == styler(sent, 1)
    assert "전등을 껐어요." == styler(sent, 2)
    assert "전등을 껐습니다." == styler(sent, 3)


def test_conjugate_gara(styler):
    """
    -가라 불규칙
    """
    sent = "저기로 가거라."
    assert "저기로 가거라." == styler(sent, 1)
    assert "저기로 가세요." == styler(sent, 2)
    assert "저기로 가십시오." == styler(sent, 3)
    sent = "저기로 가세요."
    assert "저기로 가." == styler(sent, 1)
    assert "저기로 가세요." == styler(sent, 2)
    assert "저기로 가십시오." == styler(sent, 3)


def test_conjugate_neura(styler):
    """
    -너라 불규칙
    """
    sent = "이리 오너라."
    assert "이리 오너라." == styler(sent, 1)
    assert "이리 오세요." == styler(sent, 2)
    assert "이리 오십시오." == styler(sent, 3)
    sent = "이리 오세요."
    assert "이리 와." == styler(sent, 1)
    assert "이리 오세요." == styler(sent, 2)
    assert "이리 오십시오." == styler(sent, 3)


def test_conjugate_drop_hiut(styler):
    """
    ㅎ 탈락
    """
    sent = "하늘이 파랗다."
    assert "하늘이 파랗다." == styler(sent, 1)
    assert "하늘이 파래요." == styler(sent, 2)
    assert "하늘이 파랗습니다." == styler(sent, 3)
    sent = "하늘이 파래요."
    assert "하늘이 파래." == styler(sent, 1)
    assert "하늘이 파래요." == styler(sent, 2)
    assert "하늘이 파랗습니다." == styler(sent, 3)


def test_conjugate_drop_yi(styler):
    """
    ㅓ + 이.
    """
    sent = "이렇게 하는 거야?"
    assert "이렇게 하는 거야?" == styler(sent, 1)
    assert "이렇게 하는 거죠?" == styler(sent, 2)
    assert "이렇게 하는 겁니까?" == styler(sent, 3)
    sent = "이렇게 하는 거죠?"
    assert "이렇게 하는 거지?" == styler(sent, 1)
    assert "이렇게 하는 거죠?" == styler(sent, 2)
    assert "이렇게 하는 겁니까?" == styler(sent, 3)


# --- known issues --- #
@pytest.mark.skip("추가할만한 기능 (1): 밥 -> 진지")
def test_more_1():
    sent = "밥 먹어"
    assert "밥 먹어." == styler(sent, 1)
    assert "밥 먹어요" == styler(sent, 2)
    assert "진지 잡수세요" == styler(sent, 3)


@pytest.mark.skip("추가할만한 기능 (2): 존대를 할 때는 주어를 생략할 때가 있다")
def test_more_2():
    sent = "자네만 믿고 있겠네"
    # 만약.. 들어오는 입력이 반말이라면, 굳이 반말인 경우를 수정할 필요가 없다.
    assert "자네만 믿고 있겠네." == styler(sent, 1)
    assert "믿고 있겠어요." == styler(sent, 2)
    assert "믿고 있겠습니다." == styler(sent, 3)


@pytest.mark.skip()
def test_khaiii_error_1(styler):
    """
    이건 khaiii에서의 문제다.
    "줍"만을 어간으로 추출해야하는데 알 수 없는 이유로 그렇게 되지 않는다.
    결과적으로,
    줍웠 + 어
    만을 고려하게된다. 그래서 ㅂ 블규칙이 적용되지 않음.
    """
    sent = "길가다가 동전을 주웠어."
    assert "길가다가 동전을 주웠어." == styler(sent, 1)
    assert "길가다가 동전을 주웠어요." == styler(sent, 2)
    assert "길가다가 동전을 주웠습니다." == styler(sent, 3)
    sent = "길가다가 동전을 주웠어요."  # 아... 줍우... 줍이 아니라.. 줍우..
    assert "길가다가 동전을 주웠어." == styler(sent, 1)
    assert "길가다가 동전을 주웠어요." == styler(sent, 2)
    assert "길가다가 동전을 주웠습니다." == styler(sent, 3)


@pytest.mark.skip()
def test_khaiii_error_2(styler):
    """
    이것도 khaiii에서의 문제다.
    걷어를 맥락을 고려하지 않고 무조건적으로 걸어로 분석한다.
    """
    sent = "이참에 돈을 걷어가자."
    assert "이참에 돈을 걷어가자." == styler(sent, 1)
    assert "이참에 돈을 걷어가요." == styler(sent, 2)
    assert "이참에 돈을 걷어갑시다." == styler(sent, 3)


@pytest.mark.skip()
def test_khaiii_error_3(styler):
    sent = "가까우니까 걸어가요."
    assert "가까우니까 걸어가자." == styler(sent, 1)
    assert "가까우니까 걸어가요." == styler(sent, 2)
    assert "가까우니까 걸어갑시다." == styler(sent, 3)


@pytest.mark.skip()
def test_contextual_1(styler):
    # 이런 식으로 맥락이 필요한 경우도 대응이 어렵다. (존대 종결어미 선정에 맥락이 관여하는 경우)
    # 이제, 밥을 등, 단어 선택에 따라 formal의 형태가 달라지는데, 이것에 대응하는 것은 불가능하다.
    # 맥락이 필요하다. 오직 규칙만으로는 불가능하다.
    sent = "자 이제 먹어요."
    assert "자 이제 먹읍시다" == styler(sent, 3)
    sent = "전 밥을 먹어요."
    assert "전 밥을 먹습니다" == styler(sent, 3)


@pytest.mark.skip()
def test_contextual_2(styler):
    """
    -르 불규칙 (conjugation 규칙에 맥락이 관여하는 경우)
    e.g. 이르 + 어 -> 이르러
    e.g.
    이건 -러 불규칙과 구분히 불가능하다. 나중에 맥락까지 고려할 수 있게된다면 그 때 해보자.
    여기 이슈참고: https://github.com/eubinecto/politely/issues/56#issue-1233231686
    """
    sent = "하지 말라고 일렀다."
    assert "하지 말라고 일렀다." == styler(sent, 1)
    assert "하지 말라고 일렀어요." == styler(sent, 2)
    assert "하지 말라고 일렀습니다." == styler(sent, 3)
    sent = "드디어 정상에 이르렀다."
    assert "드디어 정상에 이르렀다." == styler(sent, 1)
    assert "드디어 정상에 이르렀어요." == styler(sent, 2)
    assert "드디어 정상에 이르렀습니다." == styler(sent, 3)

@pytest.mark.skip()
def test_contextual_3(styler):
    """
    쓰레기를 주워요 -> 쓰레기를 주웁시다 / 쓰레기를 줍습니다 (존대 종결어미 선정에 맥락이 관여하는 경우)
    둘다 가능하다. 이 경우는 맥락이 필요하다. 규칙만으로는 불가능하다.
    # 자세한 설명: https://github.com/eubinecto/politely/issues/60#issuecomment-1126839221
    """
    sent = "저는 쓰레기를 주워요."
    assert "나는 쓰레기를 주워." == styler(sent, 1)
    assert "저는 쓰레기를 주워요." == styler(sent, 2)
    assert "저는 쓰레기를 줍습니다." == styler(sent, 3)
    sent = "같이 쓰레기를 주워요."
    assert "같이 쓰레기를 줍자." == styler(sent, 1)
    assert "같이 쓰레기를 주워요." == styler(sent, 2)
    assert "같이 쓰레기를 주웁시다." == styler(sent, 3)


@pytest.mark.skip()
def test_contextual_4(styler):
    """
    이것도 마찬가지로 맥락이 필요하다.
    떠나요 -> 떠나 / 떠나자, 둘 중 무엇이 정답인지는 맥락을 보아야만 알 수 있다.
    떠나요 -> 떠납니다 / 떠납시다 -> 둘 중 무엇이 맞는지도... 마찬가지
    """
    sent = "자, 떠나요. 동해 바다로."
    assert "자, 떠나자. 동해 바다로." == styler(sent, 1)
    assert "자, 떠나요. 동해 바다로." == styler(sent, 2)
    assert "자, 떠납시다. 동해 바다로." == styler(sent, 3)
