from politely import Styler
import pytest  # noqa
from politely.errors import EFNotSupportedError, SFNotIncludedError


@pytest.fixture(scope="session")
def styler():
    return Styler(debug=True)


# pytest teardown
@pytest.fixture(autouse=True)
def setup(styler):
    # always make sure that styler is in debug mode
    styler.debug = True
    yield
    # always make sure that styler is reset after a test is cleared.
    styler.setup()


def test_preprocess_with_period(styler):
    sent = "이것은 예시 문장이다."
    styler.preprocess(sent)
    assert " ".join(styler.out) == "이것은 예시 문장이다."


def test_preprocess_with_period_with_trailing_spaces(styler):
    sent = "이것은 예시 문장이다. "
    styler.preprocess(sent)
    assert " ".join(styler.out) == "이것은 예시 문장이다."


def test_preprocess_no_period(styler):
    sent = "이것은 예시 문장이다"
    styler.preprocess(sent)
    assert " ".join(styler.out) == "이것은 예시 문장이다."


def test_preprocess_no_period_with_trailing_spaces(styler):
    sent = "이것은 예시 문장이다  "
    styler.preprocess(sent)
    assert " ".join(styler.out) == "이것은 예시 문장이다."


def test_preprocess_two_sentences_with_period(styler):
    sent = "이것은 예시 문장이다. 그리고 이건 다음 문장이다."
    styler.preprocess(sent)
    assert " ".join(styler.out) == "이것은 예시 문장이다. 그리고 이건 다음 문장이다."


def test_preprocess_two_sentences_without_a_period(styler):
    sent = "이것은 예시 문장이다. 그리고 이건 다음 문장이다"
    styler.preprocess(sent)
    # a period should be added there
    assert " ".join(styler.out) == "이것은 예시 문장이다. 그리고 이건 다음 문장이다."


def test_preprocess_two_sentences_without_no_periods_at_all(styler):
    """
    This is what we need the most. Styler should automatically split a paragraph into sentences,
    and insert a period at the end of each sentence.
    """
    sent = "이것은 예시 문장이다 그리고 이건 다음 문장이다"
    styler.preprocess(sent)
    # a period should be added there
    assert " ".join(styler.out) == "이것은 예시 문장이다. 그리고 이건 다음 문장이다."


def test_check_raises_sf_not_included_error_on_debug_true(styler):
    sent = "용서해주소서"
    with pytest.raises(SFNotIncludedError):
        styler.out = sent
        # don't preprocess it
        styler.analyze().check()


def test_check_raises_ef_not_supported_error_on_debug_true(styler):
    sent = "용서해주소서"
    with pytest.raises(EFNotSupportedError):
        styler.preprocess(sent).analyze().check()


def test_check_does_not_raise_ef_not_supported_error_on_debug_false(styler):
    styler.debug = False
    sent = "용서해주소서"
    try:
        styler.setup().preprocess(sent).analyze().check()
    except EFNotSupportedError:
        pytest.fail("Exception raised")


def test_honorify_ends_with_special_char_1(styler):
    sent = "최선을 다 했어."
    assert styler(sent, 1) == "최선을 다 했어."
    assert styler(sent, 2) == "최선을 다 했어요."
    assert styler(sent, 3) == "최선을 다 했습니다."
    sent = "최선을 다 했어?"
    assert styler(sent, 1) == "최선을 다 했어?"
    assert styler(sent, 2) == "최선을 다 했어요?"
    assert styler(sent, 3) == "최선을 다 했습니까?"
    sent = "최선을 다 했어!"
    assert styler(sent, 1) == "최선을 다 했어!"
    assert styler(sent, 2) == "최선을 다 했어요!"
    assert styler(sent, 3) == "최선을 다 했습니다!"


def test_honorify_ends_with_special_char_2(styler):
    sent = "그 일은 내 담당이야."
    assert styler(sent, 1) == "그 일은 내 담당이야."
    assert styler(sent, 2) == "그 일은 제 담당예요."
    assert styler(sent, 3) == "그 일은 제 담당입니다."
    sent = "그 일은 내 담당이야?"
    assert styler(sent, 1) == "그 일은 내 담당이야?"
    assert styler(sent, 2) == "그 일은 제 담당이죠?"
    assert styler(sent, 3) == "그 일은 제 담당입니까?"
    sent = "그 일은 내 담당이야!"
    assert styler(sent, 1) == "그 일은 내 담당이야!"
    assert styler(sent, 2) == "그 일은 제 담당예요!"
    assert styler(sent, 3) == "그 일은 제 담당입니다!"


def test_honorify_yi_da_1(styler):
    """
    이 + 다
    """
    sent = "한글은 한국의 글자이다."
    assert styler(sent, 1) == "한글은 한국의 글자다."
    assert styler(sent, 2) == "한글은 한국의 글자에요."
    assert styler(sent, 3) == "한글은 한국의 글잡니다."


def test_honorify_yi_da_2(styler):
    """
    이 + 다
    """
    sent = "당초에는 비하적 의미가 없었다는 게 정설이다. 더 자세한 내용은 한글/ 역사 문서로."
    assert styler(sent, 1) == "당초에는 비하적 의미가 없었다는 게 정설이다. 더 자세한 내용은 한글/ 역사 문서로."
    assert styler(sent, 2) == "당초에는 비하적 의미가 없었다는 게 정설예요. 더 자세한 내용은 한글/ 역사 문서로."
    assert styler(sent, 3) == "당초에는 비하적 의미가 없었다는 게 정설입니다. 더 자세한 내용은 한글/ 역사 문서로."


def test_honorify_nieun_da_1(styler):
    """
    ㄴ다
    """
    sent = "조선민주주의인민공화국에서는 조선 글이라 부른다."
    assert styler(sent, 1) == "조선민주주의인민공화국에서는 조선 글이라 부른다."
    assert styler(sent, 2) == "조선민주주의인민공화국에서는 조선 글이라 불러요."
    assert styler(sent, 3) == "조선민주주의인민공화국에서는 조선 글이라 부릅니다."


def test_honorify_nieun_da_2(styler):
    """
    ㄴ다 - followed by 다.
    """
    sent = "조선민주주의인민공화국에서는 조선 글이라 부른다. 다음 문장도 이렇다."
    assert styler(sent, 1) == "조선민주주의인민공화국에서는 조선 글이라 부른다. 다음 문장도 이렇다."
    assert styler(sent, 2) == "조선민주주의인민공화국에서는 조선 글이라 불러요. 다음 문장도 이래요."
    assert styler(sent, 3) == "조선민주주의인민공화국에서는 조선 글이라 부릅니다. 다음 문장도 이렇습니다."


def test_honorify_nieun_da_3(styler):
    """
    ㄴ다 - followed by 지.
    """
    sent = "조선민주주의인민공화국에서는 조선 글이라 부른다. 다음 문장은 이렇지."
    assert styler(sent, 1) == "조선민주주의인민공화국에서는 조선 글이라 부른다. 다음 문장은 이렇지."
    assert styler(sent, 2) == "조선민주주의인민공화국에서는 조선 글이라 불러요. 다음 문장은 이래요."
    assert styler(sent, 3) == "조선민주주의인민공화국에서는 조선 글이라 부릅니다. 다음 문장은 이렇습니다."


def test_honorify_ja_1(styler):
    """
    -자
    """
    sent = "이참에 돈을 걷어 가자."
    assert styler(sent, 1) == "이참에 돈을 걷어 가자."
    assert styler(sent, 2) == "이참에 돈을 걷어 가요."
    assert styler(sent, 3) == "이참에 돈을 걷어 갑시다."


def test_honorify_ja_2(styler):
    """
    종결어미 -자
    """
    sent = "자 이제 먹자."
    assert styler(sent, 1) == "자 이제 먹자."
    assert styler(sent, 2) == "자 이제 먹어요."
    assert styler(sent, 3) == "자 이제 먹읍시다."


def test_honorify_eora(styler):
    """
    종결어미 -어라
    """
    sent = "그대로 하지 마라."
    assert styler(sent, 1) == "그대로 하지 마라."
    assert styler(sent, 2) == "그대로 하지 마요."
    assert styler(sent, 3) == "그대로 하지 마십시오."


def test_honorify_ra(styler):
    """
    종결어미 -라
    """
    sent = "최선을 다하라."
    assert styler(sent, 1) == "최선을 다하라."
    assert styler(sent, 2) == "최선을 다하세요."
    assert styler(sent, 3) == "최선을 다합시다."


def test_honorify_nieun_dae(styler):
    """
    종결어미 ㄴ대
    """
    sent = "밥 먹고 누우면 안 된대."
    assert styler(sent, 1) == "밥 먹고 누우면 안 된대."
    assert styler(sent, 2) == "밥 먹고 누우면 안 된대요."
    assert styler(sent, 3) == "밥 먹고 누우면 안 된답니다."


def test_honorify_nieun_dae_yo(styler):
    """
    종결어미 ㄴ대요
    """
    sent = "밥 먹고 누우면 안 된대요."
    assert styler(sent, 1) == "밥 먹고 누우면 안 된대."
    assert styler(sent, 2) == "밥 먹고 누우면 안 된대요."
    assert styler(sent, 3) == "밥 먹고 누우면 안 된답니다."


def test_honorify_gae(styler):
    sent = "회의를 시작할게."
    assert styler(sent, 1) == "회의를 시작할게."
    assert styler(sent, 2) == "회의를 시작할게요."
    assert styler(sent, 3) == "회의를 시작하겠습니다."


def test_honorify_eo_1(styler):
    """
    종결어미 -어
    """
    sent = "그 일은 내가 처리했어."
    assert styler(sent, 1) == "그 일은 내가 처리했어."
    assert styler(sent, 2) == "그 일은 제가 처리했어요."
    assert styler(sent, 3) == "그 일은 제가 처리했습니다."


def test_honorify_eo_2(styler):
    """
    -어
    """
    sent = "길 가다가 동전을 주웠어."
    assert styler(sent, 1) == "길 가다가 동전을 주웠어."
    assert styler(sent, 2) == "길 가다가 동전을 주웠어요."
    assert styler(sent, 3) == "길 가다가 동전을 주웠습니다."


def test_honorify_yo(styler):
    """
    종결어미 -요
    """
    sent = "제 패션을 함부로 비꼬지 마요."
    assert styler(sent, 1) == "내 패션을 함부로 비꼬지 마."
    assert styler(sent, 2) == "제 패션을 함부로 비꼬지 마요."
    assert styler(sent, 3) == "제 패션을 함부로 비꼬지 마십시오."


def test_honorify_ge_yo(styler):
    """
    게 + 종결어미 -요
    """
    sent = "회의를 시작할게요."
    assert styler(sent, 1) == "회의를 시작할게."
    assert styler(sent, 2) == "회의를 시작할게요."
    assert styler(sent, 3) == "회의를 시작하겠습니다."


def test_honorify_yi_ya(styler):
    """
    이+야
    """
    sent = "그 일은 내 담당이야."
    assert styler(sent, 1) == "그 일은 내 담당이야."
    assert styler(sent, 2) == "그 일은 제 담당예요."
    assert styler(sent, 3) == "그 일은 제 담당입니다."


def test_honorify_se_yo(styler):
    """
    세+요
    """
    sent = "최선을 다 하세요."
    assert styler(sent, 1) == "최선을 다 해."
    assert styler(sent, 2) == "최선을 다 하세요."
    assert styler(sent, 3) == "최선을 다 하십시오."


def test_honorify_yi_eyo(styler):
    """
    이 + 에요
    """
    sent = "그 일은 제 담당예요."
    assert styler(sent, 1) == "그 일은 내 담당이야."
    assert styler(sent, 2) == "그 일은 제 담당예요."
    assert styler(sent, 3) == "그 일은 제 담당입니다."


def test_honorify_eu_yo_1(styler):
    """
    종결어미 -어요 (1)
    """
    sent = "자 이제 먹어요."
    assert styler(sent, 1) == "자 이제 먹어."
    assert styler(sent, 2) == "자 이제 먹어요."
    assert styler(sent, 3) == "자 이제 먹습니다."


def test_honorify_eu_yo_2(styler):
    """
    종결어미 -어요 (2)
    """
    sent = "그 일은 제가 처리했어요."
    assert styler(sent, 1) == "그 일은 내가 처리했어."
    assert styler(sent, 2) == "그 일은 제가 처리했어요."
    assert styler(sent, 3) == "그 일은 제가 처리했습니다."


def test_honorify_bo_ayo(styler):
    """
    보 + 종결어미 -아요
    """
    sent = "좀만 더 버텨 봐요."
    assert styler(sent, 1) == "좀만 더 버텨 봐."
    assert styler(sent, 2) == "좀만 더 버텨 봐요."
    assert styler(sent, 3) == "좀만 더 버텨 봅시다."


def test_honorify_ma(styler):
    sent = "내 패션을 함부로 비꼬지 마."
    assert styler(sent, 1) == "내 패션을 함부로 비꼬지 마."
    assert styler(sent, 2) == "제 패션을 함부로 비꼬지 마요."
    assert styler(sent, 3) == "제 패션을 함부로 비꼬지 마십시오."


def test_honorify_bo_a(styler):
    sent = "좀만 더 버텨 봐."
    assert styler(sent, 1) == "좀만 더 버텨 봐."
    assert styler(sent, 2) == "좀만 더 버텨 봐요."
    assert styler(sent, 3) == "좀만 더 버텨 봅시다."


def test_honorify_dae_q(styler):
    sent = "걔 오늘 기분이 왜 이렇게 좋대?"
    assert styler(sent, 1) == "걔 오늘 기분이 왜 이렇게 좋대?"
    assert styler(sent, 2) == "걔 오늘 기분이 왜 이렇게 좋대요?"
    assert styler(sent, 3) == "걔 오늘 기분이 왜 이렇게 좋답니까?"


def test_honorify_dae_yo_q(styler):
    sent = "걔 오늘 기분이 왜 이렇게 좋대요?"
    assert styler(sent, 1) == "걔 오늘 기분이 왜 이렇게 좋대?"
    assert styler(sent, 2) == "걔 오늘 기분이 왜 이렇게 좋대요?"
    assert styler(sent, 3) == "걔 오늘 기분이 왜 이렇게 좋답니까?"


def test_honorify_eo_q(styler):
    """
    어?
    """
    # 했어?
    sent = "어제 공부는 마무리했어?"
    assert styler(sent, 1) == "어제 공부는 마무리했어?"
    assert styler(sent, 2) == "어제 공부는 마무리했어요?"
    assert styler(sent, 3) == "어제 공부는 마무리했습니까?"


def test_honorify_eo_yo(styler):
    sent = "길 가다가 동전을 주웠어요."
    assert styler(sent, 1) == "길 가다가 동전을 주웠어."
    assert styler(sent, 2) == "길 가다가 동전을 주웠어요."
    assert styler(sent, 3) == "길 가다가 동전을 주웠습니다."


def test_honorify_eo_yo_q_1(styler):
    """
    의문형 종결어미 -어요? (1)
    """
    sent = "어제 공부는 마무리했어요?"
    assert styler(sent, 1) == "어제 공부는 마무리했어?"
    assert styler(sent, 2) == "어제 공부는 마무리했어요?"
    assert styler(sent, 3) == "어제 공부는 마무리했습니까?"


def test_honorify_eo_yo_q_2(styler):
    """
    의문형 종결어미 -어요 (2)
    """
    sent = "어디 가세요?"
    assert styler(sent, 1) == "어디 가?"
    assert styler(sent, 2) == "어디 가세요?"
    assert styler(sent, 3) == "어디 가십니까?"


def test_honorify_ga(styler):
    """
    시 + 의문형 종결어미 -어?
    """
    # 가셔? (가시어?)
    sent = "어디 가?"
    assert styler(sent, 1) == "어디 가?"
    assert styler(sent, 2) == "어디 가요?"
    assert styler(sent, 3) == "어디 갑니까?"


def test_honorify_ddae_q(styler):
    sent = "순서를 바꾸는 거는 어때?"
    assert styler(sent, 1) == "순서를 바꾸는 거는 어때?"
    assert styler(sent, 2) == "순서를 바꾸는 거는 어때요?"
    assert styler(sent, 3) == "순서를 바꾸는 거는 어떻습니까?"
    sent = "순서를 바꾸는 거는 어때요?"
    assert styler(sent, 1) == "순서를 바꾸는 거는 어때?"
    assert styler(sent, 2) == "순서를 바꾸는 거는 어때요?"
    assert styler(sent, 3) == "순서를 바꾸는 거는 어떻습니까?"


def test_honorify_bieup_nida(styler):
    sent = "지금 갑니다."
    assert styler(sent, 1) == "지금 가."
    assert styler(sent, 2) == "지금 가요."
    assert styler(sent, 3) == "지금 갑니다."


def test_honorify_jo(styler):
    """
    -죠
    """
    sent = "그거는 제가 하죠."
    assert styler(sent, 1) == "그거는 내가 할게."
    assert styler(sent, 2) == "그거는 제가 하죠."
    assert styler(sent, 3) == "그거는 제가 합니다."


# --- tests by irregular conjugations --- #
def test_conjugate_ah_1(styler):
    """
    동모음 탈락
    걸어가어요 (x)
    걸어가요 (o)
    """
    sent = "가까우니까 걸어가자."
    assert styler(sent, 1) == "가까우니까 걸어가자."
    assert styler(sent, 2) == "가까우니까 걸어가요."
    assert styler(sent, 3) == "가까우니까 걸어갑시다."


def test_conjugate_ah_2(styler):
    """
    동모음 탈락
    떠나어요 (x)
    떠나요 (o)
    """
    sent = "자, 떠나자."
    assert styler(sent, 1) == "자, 떠나자."
    assert styler(sent, 2) == "자, 떠나요."
    assert styler(sent, 3) == "자, 떠납시다."


def test_conjugate_digud(styler):
    """
    ㄷ 불규칙
    """
    sent = "나는 오늘 그 사실을 깨달았다."
    assert styler(sent, 1) == "나는 오늘 그 사실을 깨달았다."
    assert styler(sent, 2) == "저는 오늘 그 사실을 깨달았어요."
    assert styler(sent, 3) == "저는 오늘 그 사실을 깨달았습니다."
    sent = "저는 오늘 그 사실을 깨달았어요."
    assert styler(sent, 1) == "나는 오늘 그 사실을 깨달았어."
    assert styler(sent, 2) == "저는 오늘 그 사실을 깨달았어요."
    assert styler(sent, 3) == "저는 오늘 그 사실을 깨달았습니다."


def test_conjugate_ru(styler):
    """
    르 불규칙
    e.g. 들르 + 어 -> 들러
    e.g. 이르 + 어  -> 일러
    """
    sent = "나는 그 상점을 들렀다."
    assert styler(sent, 1) == "나는 그 상점을 들렀다."
    assert styler(sent, 2) == "저는 그 상점을 들렀어요."
    assert styler(sent, 3) == "저는 그 상점을 들렀습니다."
    sent = "저는 그 상점을 들렀어요."
    assert styler(sent, 1) == "나는 그 상점을 들렀어."
    assert styler(sent, 2) == "저는 그 상점을 들렀어요."
    assert styler(sent, 3) == "저는 그 상점을 들렀습니다."
    sent = "지금은 좀 일러."
    assert styler(sent, 1) == "지금은 좀 일러."
    assert styler(sent, 2) == "지금은 좀 일러요."
    assert styler(sent, 3) == "지금은 좀 이릅니다."


def test_conjugate_bieup_1(styler):
    """
    ㅂ 불규칙 (모음 조화 o)
    """
    sent = "모래가 참 고와."
    assert styler(sent, 1) == "모래가 참 고와."
    assert styler(sent, 2) == "모래가 참 고와요."
    assert styler(sent, 3) == "모래가 참 곱습니다."
    sent = "모래가 참 고와요."
    assert styler(sent, 1) == "모래가 참 고와."
    assert styler(sent, 2) == "모래가 참 고와요."
    assert styler(sent, 3) == "모래가 참 곱습니다."


def test_conjugate_bieup_2(styler):
    """
    ㅂ 불규칙 (모음 조화 x)
    """
    sent = "참 아름답다."
    assert styler(sent, 1) == "참 아름답다."
    assert styler(sent, 2) == "참 아름다워요."
    assert styler(sent, 3) == "참 아름답습니다."
    sent = "참 아름다워요."
    assert styler(sent, 1) == "참 아름다워."
    assert styler(sent, 2) == "참 아름다워요."
    assert styler(sent, 3) == "참 아름답습니다."


def test_conjugate_bieup_3(styler):
    """
    더워의 경우.
    """
    sent = "오늘이 어제보다 더워."
    assert styler(sent, 1) == "오늘이 어제보다 더워."
    assert styler(sent, 2) == "오늘이 어제보다 더워요."
    assert styler(sent, 3) == "오늘이 어제보다 덥습니다."
    sent = "오늘이 어제보다 더워요."
    assert styler(sent, 1) == "오늘이 어제보다 더워."
    assert styler(sent, 2) == "오늘이 어제보다 더워요."
    assert styler(sent, 3) == "오늘이 어제보다 덥습니다."


def test_conjugate_bieup_4(styler):
    """
    가려워의 경우.
    """
    sent = "너무 가려워."
    assert styler(sent, 1) == "너무 가려워."
    assert styler(sent, 2) == "너무 가려워요."
    assert styler(sent, 3) == "너무 가렵습니다."
    sent = "너무 가려워요."
    assert styler(sent, 1) == "너무 가려워."
    assert styler(sent, 2) == "너무 가려워요."
    assert styler(sent, 3) == "너무 가렵습니다."


def test_conjugate_r_cho_is_bieup(styler):
    """
    ㅂ니다
    """
    sent = "이름은 김유빈이야."
    assert styler(sent, 3) == "이름은 김유빈입니다."
    sent = "이름은 김유빈이에요."
    assert styler(sent, 3) == "이름은 김유빈입니다."


def test_conjugate_siot(styler):
    """
    ㅅ 불규칙
    """
    sent = "거기에 선을 그어."
    assert styler(sent, 1) == "거기에 선을 그어."
    assert styler(sent, 2) == "거기에 선을 그어요."
    assert styler(sent, 3) == "거기에 선을 긋습니다."
    sent = "거기에 선을 그어요."
    assert styler(sent, 1) == "거기에 선을 그어."
    assert styler(sent, 2) == "거기에 선을 그어요."
    assert styler(sent, 3) == "거기에 선을 긋습니다."


def test_conjugate_siot_exception(styler):
    """
    ㅅ 불규칙 (벗어는 예외)
    """
    sent = "한국의 목욕탕에서는 옷을 벗어."
    assert styler(sent, 1) == "한국의 목욕탕에서는 옷을 벗어."
    assert styler(sent, 2) == "한국의 목욕탕에서는 옷을 벗어요."
    assert styler(sent, 3) == "한국의 목욕탕에서는 옷을 벗습니다."
    sent = "한국의 목욕탕에서는 옷을 벗어요."
    assert styler(sent, 1) == "한국의 목욕탕에서는 옷을 벗어."
    assert styler(sent, 2) == "한국의 목욕탕에서는 옷을 벗어요."
    assert styler(sent, 3) == "한국의 목욕탕에서는 옷을 벗습니다."


def test_conjugate_u(styler):
    """
    우 불규칙
    """
    sent = "이 포스팅 퍼 갈게."
    assert styler(sent, 1) == "이 포스팅 퍼 갈게."
    assert styler(sent, 2) == "이 포스팅 퍼 갈게요."
    assert styler(sent, 3) == "이 포스팅 퍼 가겠습니다."
    sent = "이 포스팅 퍼 갈게요."
    assert styler(sent, 1) == "이 포스팅 퍼 갈게."
    assert styler(sent, 2) == "이 포스팅 퍼 갈게요."
    assert styler(sent, 3) == "이 포스팅 퍼 가겠습니다."


def test_conjugate_u_jup(styler):
    """
    우 불규칙 - 줍은 예외
    """
    sent = "쓰레기를 줍자."
    assert styler(sent, 1) == "쓰레기를 줍자."
    assert styler(sent, 2) == "쓰레기를 주워요."
    assert styler(sent, 3) == "쓰레기를 주웁시다."
    sent = "쓰레기를 주워요."
    assert styler(sent, 1) == "쓰레기를 주워."
    assert styler(sent, 2) == "쓰레기를 주워요."
    assert styler(sent, 3) == "쓰레기를 줍습니다."


def test_conjugate_o(styler):
    """
    오 불규칙
    """
    sent = "오늘 제주도로 여행 왔어."
    assert styler(sent, 1) == "오늘 제주도로 여행 왔어."
    assert styler(sent, 2) == "오늘 제주도로 여행 왔어요."
    assert styler(sent, 3) == "오늘 제주도로 여행 왔습니다."
    sent = "오늘 제주도로 여행 왔어요."
    assert styler(sent, 1) == "오늘 제주도로 여행 왔어."
    assert styler(sent, 2) == "오늘 제주도로 여행 왔어요."
    assert styler(sent, 3) == "오늘 제주도로 여행 왔습니다."


def test_conjugate_drop_ue(styler):
    """
    으 탈락 불규칙
    """
    sent = "전등을 껐다."
    assert styler(sent, 1) == "전등을 껐다."
    assert styler(sent, 2) == "전등을 껐어요."
    assert styler(sent, 3) == "전등을 껐습니다."
    sent = "전등을 껐어요."
    assert styler(sent, 1) == "전등을 껐어."
    assert styler(sent, 2) == "전등을 껐어요."
    assert styler(sent, 3) == "전등을 껐습니다."


def test_conjugate_gara(styler):
    """
    -가라 불규칙
    """
    sent = "저기로 가거라."
    assert styler(sent, 1) == "저기로 가거라."
    assert styler(sent, 2) == "저기로 가세요."
    assert styler(sent, 3) == "저기로 가십시오."
    sent = "저기로 가세요."
    assert styler(sent, 1) == "저기로 가."
    assert styler(sent, 2) == "저기로 가세요."
    assert styler(sent, 3) == "저기로 가십시오."


def test_conjugate_neura(styler):
    """
    -너라 불규칙
    """
    sent = "이리 오너라."
    assert styler(sent, 1) == "이리 오너라."
    assert styler(sent, 2) == "이리 오세요."
    assert styler(sent, 3) == "이리 오십시오."


def test_conjugate_drop_hiut(styler):
    """
    ㅎ 탈락
    """
    sent = "하늘이 파랗다."
    assert styler(sent, 1) == "하늘이 파랗다."
    assert styler(sent, 2) == "하늘이 파래요."
    assert styler(sent, 3) == "하늘이 파랗습니다."
    sent = "하늘이 파래요."
    assert styler(sent, 1) == "하늘이 파래."
    assert styler(sent, 2) == "하늘이 파래요."
    assert styler(sent, 3) == "하늘이 파랗습니다."


def test_conjugate_drop_yi(styler):
    """
    ㅓ + 이.
    """
    sent = "이렇게 하는 거야?"
    assert styler(sent, 1) == "이렇게 하는 거야?"
    assert styler(sent, 2) == "이렇게 하는 거죠?"
    assert styler(sent, 3) == "이렇게 하는 겁니까?"
    sent = "이렇게 하는 거죠?"
    assert styler(sent, 1) == "이렇게 하는 거지?"
    assert styler(sent, 2) == "이렇게 하는 거죠?"
    assert styler(sent, 3) == "이렇게 하는 겁니까?"


# --- known issues --- #
@pytest.mark.skip("추가할만한 기능 (1): 밥 -> 진지")
def test_more_1():
    sent = "밥 먹어"
    assert styler(sent, 1) == "밥 먹어."
    assert styler(sent, 2) == "밥 먹어요"
    assert styler(sent, 3) == "진지 잡수세요"


@pytest.mark.skip("추가할만한 기능 (2): 존대를 할 때는 주어를 생략할 때가 있다")
def test_more_2():
    sent = "자네만 믿고 있겠네"
    # 만약.. 들어오는 입력이 반말이라면, 굳이 반말인 경우를 수정할 필요가 없다.
    assert styler(sent, 1) == "자네만 믿고 있겠네."
    assert styler(sent, 2) == "믿고 있겠어요."
    assert styler(sent, 3) == "믿고 있겠습니다."


@pytest.mark.skip()
def test_kiwi_error_3(styler):
    """
    이 + 다.
    어간에 받침이 있는 경우, 이에요.
    어간에 받침이 없는 경우, 예요.
    그리고 에요는? - 생각해볼게 많다.
    """
    sent = "콩나물은 에어팟의 별칭이다."
    assert styler(sent, 1) == "콩나물은 에어팟의 별칭이다."
    assert styler(sent, 2) == "콩나물은 에어팟의 별칭이에요."
    assert styler(sent, 3) == "콩나물은 에어팟의 별칭입니다."


@pytest.mark.skip()
def test_contextual_1(styler):
    # 이런 식으로 맥락이 필요한 경우도 대응이 어렵다. (존대 종결어미 선정에 맥락이 관여하는 경우)
    # 이제, 밥을 등, 단어 선택에 따라 formal의 형태가 달라지는데, 이것에 대응하는 것은 불가능하다.
    # 맥락이 필요하다. 오직 규칙만으로는 불가능하다.
    sent = "자 이제 먹어요."
    assert styler(sent, 3) == "자 이제 먹읍시다"
    sent = "전 밥을 먹어요."
    assert styler(sent, 3) == "전 밥을 먹습니다"


@pytest.mark.skip()
def test_contextual_2(styler):
    """
    -르 불규칙 (conjugation 규칙에 맥락이 관여하는 경우)
    e.g. 이르 + 어 -> 이르러
    e.g.
    이건 -러 불규칙과 구분이 불가능하다. 나중에 맥락까지 고려할 수 있게된다면 그 때 해보자.
    여기 이슈참고: https://github.com/eubinecto/politely/issues/56#issue-1233231686
    """
    sent = "하지 말라고 일렀다."
    assert styler(sent, 1) == "하지 말라고 일렀다."
    assert styler(sent, 2) == "하지 말라고 일렀어요."
    assert styler(sent, 3) == "하지 말라고 일렀습니다."
    sent = "드디어 정상에 이르렀다."
    assert styler(sent, 1) == "드디어 정상에 이르렀다."
    assert styler(sent, 2) == "드디어 정상에 이르렀어요."
    assert styler(sent, 3) == "드디어 정상에 이르렀습니다."


@pytest.mark.skip()
def test_contextual_3(styler):
    """
    쓰레기를 주워요 -> 쓰레기를 주웁시다 / 쓰레기를 줍습니다 (존대 종결어미 선정에 맥락이 관여하는 경우)
    둘다 가능하다. 이 경우는 맥락이 필요하다. 규칙만으로는 불가능하다.
    # 자세한 설명: https://github.com/eubinecto/politely/issues/60#issuecomment-1126839221
    """
    sent = "저는 쓰레기를 주워요."
    assert styler(sent, 1) == "나는 쓰레기를 주워."
    assert styler(sent, 2) == "저는 쓰레기를 주워요."
    assert styler(sent, 3) == "저는 쓰레기를 줍습니다."
    sent = "같이 쓰레기를 주워요."
    assert styler(sent, 1) == "같이 쓰레기를 줍자."
    assert styler(sent, 2) == "같이 쓰레기를 주워요."
    assert styler(sent, 3) == "같이 쓰레기를 주웁시다."


@pytest.mark.skip()
def test_contextual_4(styler):
    """
    이것도 마찬가지로 맥락이 필요하다.
    떠나요 -> 떠나 / 떠나자, 둘 중 무엇이 정답인지는 맥락을 보아야만 알 수 있다.
    떠나요 -> 떠납니다 / 떠납시다 -> 둘 중 무엇이 맞는지도... 마찬가지
    """
    sent = "자, 떠나요. 동해 바다로."
    assert styler(sent, 1) == "자, 떠나자. 동해 바다로."
    assert styler(sent, 2) == "자, 떠나요. 동해 바다로."
    assert styler(sent, 3) == "자, 떠납시다. 동해 바다로."


@pytest.mark.skip()
def test_contextual_5(styler):
    sent = "가까우니까 걸어가요."
    assert styler(sent, 1) == "가까우니까 걸어가."
    assert styler(sent, 2) == "가까우니까 걸어가요."
    assert styler(sent, 3) == "가까우니까 걸어갑시다."
