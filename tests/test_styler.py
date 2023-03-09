import pytest
from politely import Styler
from politely.errors import SFNotIncludedError


@pytest.fixture(scope="session")
def styler():
    return Styler(strict=True)


# pytest teardown
@pytest.fixture(autouse=True)
def setup(styler):
    # always make sure that styler is in debug mode
    styler.strict = True
    yield
    # always make sure that styler is reset after a test is cleared.
    styler.setup()


def test_preprocess_with_period(styler):
    sent = "이것은 예시 문장이다."
    styler.preprocess(sent)
    assert styler.out == "이것은 예시 문장이다."


def test_preprocess_with_period_with_trailing_spaces(styler):
    sent = "이것은 예시 문장이다. "
    styler.preprocess(sent)
    assert styler.out == "이것은 예시 문장이다."


def test_preprocess_no_period(styler):
    sent = "이것은 예시 문장이다"
    styler.preprocess(sent)
    assert styler.out == "이것은 예시 문장이다."


def test_preprocess_no_period_with_trailing_spaces(styler):
    sent = "이것은 예시 문장이다  "
    styler.preprocess(sent)
    assert styler.out == "이것은 예시 문장이다."


def test_check_raises_sf_not_included_error_on_strict_true(styler):
    styler.strict = True
    sent = "용서해주소서"
    with pytest.raises(SFNotIncludedError):
        styler.out = sent
        # don't preprocess it
        styler.analyze().check()


@pytest.mark.skip()
def test_honorify_ends_with_special_char_1(styler):
    """
    this test is for the case where the last character is a special character
    """
    sent = "최선을 다 했어."
    assert styler(sent, 0) == "최선을 다 했어."
    assert styler(sent, 1) == "최선을 다 했어요."
    assert styler(sent, 2) == "최선을 다 했습니다."
    sent = "최선을 다 했어?"
    assert styler(sent, 0) == "최선을 다 했어?"
    assert styler(sent, 1) == "최선을 다 했어요?"
    assert styler(sent, 2) == "최선을 다 했습니까?"
    sent = "최선을 다 했어!"
    assert styler(sent, 0) == "최선을 다 했어!"
    assert styler(sent, 1) == "최선을 다 했어요!"
    assert styler(sent, 2) == "최선을 다 했습니다!"


@pytest.mark.skip()
def test_honorify_ends_with_special_char_2(styler):
    sent = "그 일은 내 담당이야."
    assert styler(sent, 0) == "그 일은 내 담당이야."
    assert styler(sent, 1) == "그 일은 제 담당예요."
    assert styler(sent, 2) == "그 일은 제 담당입니다."
    sent = "그 일은 내 담당이야?"
    assert styler(sent, 0) == "그 일은 내 담당이야?"
    assert styler(sent, 1) == "그 일은 제 담당이죠?"
    assert styler(sent, 2) == "그 일은 제 담당입니까?"
    sent = "그 일은 내 담당이야!"
    assert styler(sent, 0) == "그 일은 내 담당이야!"
    assert styler(sent, 1) == "그 일은 제 담당예요!"
    assert styler(sent, 2) == "그 일은 제 담당입니다!"


@pytest.mark.skip()
def test_honorify_yi_da_1(styler):
    """
    이 + 다
    """
    sent = "한글은 한국의 글자이다."
    assert styler(sent, 0) == "한글은 한국의 글자다."
    assert styler(sent, 1) == "한글은 한국의 글자에요."
    assert styler(sent, 2) == "한글은 한국의 글잡니다."


@pytest.mark.skip()
def test_honorify_yi_da_2(styler):
    """
    이 + 다
    """
    sent = "당초에는 비하적 의미가 없었다는 게 정설이다. 더 자세한 내용은 한글/ 역사 문서로."
    assert styler(sent, 0) == "당초에는 비하적 의미가 없었다는 게 정설이다. 더 자세한 내용은 한글/ 역사 문서로."
    assert styler(sent, 1) == "당초에는 비하적 의미가 없었다는 게 정설예요. 더 자세한 내용은 한글/ 역사 문서로."
    assert styler(sent, 2) == "당초에는 비하적 의미가 없었다는 게 정설입니다. 더 자세한 내용은 한글/ 역사 문서로."


@pytest.mark.skip()
def test_honorify_randa(styler):
    """
    -란다
    """
    sent = "여기서 얼른 먹어 버리란다."
    assert styler(sent, 0) == "여기서 얼른 먹어 버리란다."
    assert styler(sent, 1) == "여기서 얼른 먹어 버리래요."
    assert styler(sent, 2) == "여기서 얼른 먹어 버리랍니다."


def test_honorify_nieun_da_1(styler):
    """
    ㄴ다
    """
    sent = "조선민주주의인민공화국에서는 조선 글이라 부른다."
    assert styler(sent, 0) == "조선민주주의인민공화국에서는 조선 글이라 부른다."
    assert styler(sent, 1) == "조선민주주의인민공화국에서는 조선 글이라 불러요."
    assert styler(sent, 2) == "조선민주주의인민공화국에서는 조선 글이라 부릅니다."


@pytest.mark.skip()
def test_honorify_nieun_da_4(styler):
    """
    ㄴ다
    """
    sent = "봄 감자가 맛있단다."
    assert styler(sent, 0) == "봄 감자가 맛있단다."
    assert styler(sent, 1) == "봄 감자가 맛있어요."
    assert styler(sent, 2) == "봄 감자가 맛있습니다."


@pytest.mark.skip()
def test_honorify_ja_1(styler):
    """
    -자
    """
    sent = "이참에 돈을 걷어 가자."
    assert styler(sent, 0) == "이참에 돈을 걷어 가자."
    assert styler(sent, 1) == "이참에 돈을 걷어 가요."
    assert styler(sent, 2) == "이참에 돈을 걷어 갑시다."


@pytest.mark.skip()
def test_honorify_nya(styler):
    """
    -냐
    """
    sent = "나중에는 눈물까지 어리는 게 아니냐."
    assert styler(sent, 0) == "나중에는 눈물까지 어리는 게 아니냐."
    assert styler(sent, 1) == "나중에는 눈물까지 어리는 게 아녀요."
    assert styler(sent, 2) == "나중에는 눈물까지 어리는 게 아닙디다."


@pytest.mark.skip()
def test_honorify_ja_2(styler):
    """
    종결어미 -자
    """
    sent = "자 이제 먹자."
    assert styler(sent, 0) == "자 이제 먹자."
    assert styler(sent, 1) == "자 이제 먹어요."
    assert styler(sent, 2) == "자 이제 먹읍시다."


@pytest.mark.skip()
def test_honorify_eora(styler):
    """
    종결어미 -어라
    """
    sent = "그대로 하지 마라."
    assert styler(sent, 0) == "그대로 하지 마라."
    assert styler(sent, 1) == "그대로 하지 마요."
    assert styler(sent, 2) == "그대로 하지 마십시오."


@pytest.mark.skip()
def test_honorify_ra(styler):
    """
    종결어미 -라
    """
    sent = "최선을 다하라."
    assert styler(sent, 0) == "최선을 다하라."
    assert styler(sent, 1) == "최선을 다하세요."
    assert styler(sent, 2) == "최선을 다합시다."


@pytest.mark.skip()
def test_honorify_nieun_dae(styler):
    """
    종결어미 ㄴ대
    """
    sent = "밥 먹고 누우면 안 된대."
    assert styler(sent, 0) == "밥 먹고 누우면 안 된대."
    assert styler(sent, 1) == "밥 먹고 누우면 안 된대요."
    assert styler(sent, 2) == "밥 먹고 누우면 안 된답니다."


@pytest.mark.skip()
def test_honorify_nieun_dae_yo(styler):
    """
    종결어미 ㄴ대요
    """
    sent = "밥 먹고 누우면 안 된대요."
    assert styler(sent, 0) == "밥 먹고 누우면 안 된대."
    assert styler(sent, 1) == "밥 먹고 누우면 안 된대요."
    assert styler(sent, 2) == "밥 먹고 누우면 안 된답니다."


@pytest.mark.skip()
def test_honorify_gae(styler):
    sent = "회의를 시작할게."
    assert styler(sent, 0) == "회의를 시작할게."
    assert styler(sent, 1) == "회의를 시작할게요."
    assert styler(sent, 2) == "회의를 시작하겠습니다."


def test_honorify_eo_1(styler):
    """
    종결어미 -어
    """
    sent = "그 일은 내가 처리했어."
    assert styler(sent, 0) == "그 일은 내가 처리했어."
    assert styler(sent, 1) == "그 일은 제가 처리했어요."
    assert styler(sent, 2) == "그 일은 제가 처리했습니다."


def test_honorify_eo_2(styler):
    """
    -어
    """
    sent = "길 가다가 동전을 주웠어."
    assert styler(sent, 0) == "길 가다가 동전을 주웠어."
    assert styler(sent, 1) == "길 가다가 동전을 주웠어요."
    assert styler(sent, 2) == "길 가다가 동전을 주웠습니다."


@pytest.mark.skip()
def test_honorify_yo(styler):
    """
    종결어미 -요
    """
    sent = "제 패션을 함부로 비꼬지 마요."
    assert styler(sent, 0) == "내 패션을 함부로 비꼬지 마."
    assert styler(sent, 1) == "제 패션을 함부로 비꼬지 마요."
    assert styler(sent, 2) == "제 패션을 함부로 비꼬지 마십시오."


@pytest.mark.skip()
def test_honorify_ge_yo(styler):
    """
    게 + 종결어미 -요
    """
    sent = "회의를 시작할게요."
    assert styler(sent, 0) == "회의를 시작할게."
    assert styler(sent, 1) == "회의를 시작할게요."
    assert styler(sent, 2) == "회의를 시작하겠습니다."


@pytest.mark.skip()
def test_honorify_yi_ya(styler):
    """
    이+야
    """
    sent = "그 일은 내 담당이야."
    assert styler(sent, 0) == "그 일은 내 담당이야."
    assert styler(sent, 1) == "그 일은 제 담당예요."
    assert styler(sent, 2) == "그 일은 제 담당입니다."


@pytest.mark.skip()
def test_honorify_se_yo(styler):
    """
    세+요
    """
    sent = "최선을 다 하세요."
    assert styler(sent, 0) == "최선을 다 해."
    assert styler(sent, 1) == "최선을 다 해요."
    assert styler(sent, 2) == "최선을 다 하십시오."


@pytest.mark.skip()
def test_honorify_yi_eyo(styler):
    """
    이 + 에요
    """
    sent = "그 일은 제 담당이에요."
    assert styler(sent, 0) == "그 일은 내 담당이야."
    assert styler(sent, 1) == "그 일은 제 담당예요."
    assert styler(sent, 2) == "그 일은 제 담당입니다."


def test_honorify_eu_yo_1(styler):
    """
    종결어미 -어요 (1)
    """
    sent = "자 이제 먹어요."
    assert styler(sent, 0) == "자 이제 먹어."
    assert styler(sent, 1) == "자 이제 먹어요."
    assert styler(sent, 2) == "자 이제 먹습니다."


def test_honorify_eu_yo_2(styler):
    """
    종결어미 -어요 (2)
    """
    sent = "그 일은 제가 처리했어요."
    assert styler(sent, 0) == "그 일은 내가 처리했어."
    assert styler(sent, 1) == "그 일은 제가 처리했어요."
    assert styler(sent, 2) == "그 일은 제가 처리했습니다."


@pytest.mark.skip()
def test_honorify_bo_ayo(styler):
    """
    보 + 종결어미 -아요
    """
    sent = "좀만 더 버텨 봐요."
    assert styler(sent, 0) == "좀만 더 버텨 봐."
    assert styler(sent, 1) == "좀만 더 버텨 봐요."
    assert styler(sent, 2) == "좀만 더 버텨 봅시다."

@pytest.mark.skip()
def test_honorify_ma(styler):
    sent = "내 패션을 함부로 비꼬지 마."
    assert styler(sent, 0) == "내 패션을 함부로 비꼬지 마."
    assert styler(sent, 1) == "제 패션을 함부로 비꼬지 마요."
    assert styler(sent, 2) == "제 패션을 함부로 비꼬지 마십시오."


@pytest.mark.skip()
def test_honorify_bo_a(styler):
    sent = "좀만 더 버텨 봐."
    assert styler(sent, 0) == "좀만 더 버텨 봐."
    assert styler(sent, 1) == "좀만 더 버텨 봐요."
    assert styler(sent, 2) == "좀만 더 버텨 봅시다."


def test_honorify_dae_q(styler):
    sent = "걔 오늘 기분이 왜 이렇게 좋대?"
    assert styler(sent, 0) == "걔 오늘 기분이 왜 이렇게 좋대?"
    assert styler(sent, 1) == "걔 오늘 기분이 왜 이렇게 좋아요?"
    assert styler(sent, 2) == "걔 오늘 기분이 왜 이렇게 좋습니까?"


def test_honorify_dae_yo_q(styler):
    sent = "걔 오늘 기분이 왜 이렇게 좋대요?"
    assert styler(sent, 0) == "걔 오늘 기분이 왜 이렇게 좋아?"
    assert styler(sent, 1) == "걔 오늘 기분이 왜 이렇게 좋대요?"
    assert styler(sent, 2) == "걔 오늘 기분이 왜 이렇게 좋습니까?"


def test_honorify_eo_q(styler):
    """
    어?
    """
    # 했어?
    sent = "어제 공부는 마무리했어?"
    assert styler(sent, 0) == "어제 공부는 마무리했어?"
    assert styler(sent, 1) == "어제 공부는 마무리했어요?"
    assert styler(sent, 2) == "어제 공부는 마무리했습니까?"


def test_honorify_eo_yo(styler):
    sent = "길 가다가 동전을 주웠어요."
    assert styler(sent, 0) == "길 가다가 동전을 주웠어."
    assert styler(sent, 1) == "길 가다가 동전을 주웠어요."
    assert styler(sent, 2) == "길 가다가 동전을 주웠습니다."


def test_honorify_eo_yo_q_1(styler):
    """
    의문형 종결어미 -어요? (1)
    """
    sent = "어제 공부는 마무리했어요?"
    assert styler(sent, 0) == "어제 공부는 마무리했어?"
    assert styler(sent, 1) == "어제 공부는 마무리했어요?"
    assert styler(sent, 2) == "어제 공부는 마무리했습니까?"


@pytest.mark.skip()
def test_honorify_eo_yo_q_2(styler):
    """
    의문형 종결어미 -어요 (2)
    """
    sent = "어디 가세요?"
    assert styler(sent, 0) == "어디 가?"
    assert styler(sent, 1) == "어디 가세요?"
    assert styler(sent, 2) == "어디 가십니까?"


@pytest.mark.skip()
def test_honorify_ga(styler):
    """
    시 + 의문형 종결어미 -어?
    """
    # 가셔? (가시어?)
    sent = "어디 가?"
    assert styler(sent, 0) == "어디 가?"
    assert styler(sent, 1) == "어디 가요?"
    assert styler(sent, 2) == "어디 가십니까?"


@pytest.mark.skip()
def test_honorify_ddae_q(styler):
    sent = "순서를 바꾸는 거는 어때?"
    assert styler(sent, 0) == "순서를 바꾸는 거는 어때?"
    assert styler(sent, 1) == "순서를 바꾸는 거는 어때요?"
    assert styler(sent, 2) == "순서를 바꾸는 거는 어떻습니까?"
    sent = "순서를 바꾸는 거는 어때요?"
    assert styler(sent, 0) == "순서를 바꾸는 거는 어때?"
    assert styler(sent, 1) == "순서를 바꾸는 거는 어때요?"
    assert styler(sent, 2) == "순서를 바꾸는 거는 어떻습니까?"


def test_honorify_bieup_nida(styler):
    sent = "지금 갑니다."
    assert styler(sent, 0) == "지금 가."
    assert styler(sent, 1) == "지금 가요."
    assert styler(sent, 2) == "지금 갑니다."


def test_honorify_jo(styler):
    """
    -죠
    """
    sent = "그거는 제가 하죠."
    assert styler(sent, 0) == "그거는 내가 해."
    assert styler(sent, 1) == "그거는 제가 하죠."
    assert styler(sent, 2) == "그거는 제가 합니다."


def test_honorify_nan(styler):
    """
    난
    """
    sent = "난 감자 안 먹는다."
    assert styler(sent, 0) == "난 감자 안 먹는다."
    assert styler(sent, 1) == "전 감자 안 먹어요."
    assert styler(sent, 2) == "전 감자 안 먹습니다."


# --- known issues --- #
@pytest.mark.skip("추가할만한 기능 (1): 밥 -> 진지")
def test_more_1():
    sent = "밥 먹어"
    assert styler(sent, 0) == "밥 먹어."
    assert styler(sent, 1) == "밥 먹어요"
    assert styler(sent, 2) == "진지 잡수세요"


@pytest.mark.skip("추가할만한 기능 (2): 존대를 할 때는 주어를 생략할 때가 있다")
def test_more_2():
    sent = "자네만 믿고 있겠네"
    # 만약.. 들어오는 입력이 반말이라면, 굳이 반말인 경우를 수정할 필요가 없다.
    assert styler(sent, 0) == "자네만 믿고 있겠네."
    assert styler(sent, 1) == "믿고 있겠어요."
    assert styler(sent, 2) == "믿고 있겠습니다."


@pytest.mark.skip()
def test_kiwi_error_3(styler):
    """
    이 + 다.
    어간에 받침이 있는 경우, 이에요.
    어간에 받침이 없는 경우, 예요.
    그리고 에요는? - 생각해볼게 많다.
    """
    sent = "콩나물은 에어팟의 별칭이다."
    assert styler(sent, 0) == "콩나물은 에어팟의 별칭이다."
    assert styler(sent, 1) == "콩나물은 에어팟의 별칭이에요."
    assert styler(sent, 2) == "콩나물은 에어팟의 별칭입니다."


@pytest.mark.skip()
def test_contextual_1(styler):
    # 이런 식으로 맥락이 필요한 경우도 대응이 어렵다. (존대 종결어미 선정에 맥락이 관여하는 경우)
    # 이제, 밥을 등, 단어 선택에 따라 formal의 형태가 달라지는데, 이것에 대응하는 것은 불가능하다.
    # 맥락이 필요하다. 오직 규칙만으로는 불가능하다.
    sent = "자 이제 먹어요."
    assert styler(sent, 2) == "자 이제 먹읍시다"
    sent = "전 밥을 먹어요."
    assert styler(sent, 2) == "전 밥을 먹습니다"


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
    assert styler(sent, 0) == "하지 말라고 일렀다."
    assert styler(sent, 1) == "하지 말라고 일렀어요."
    assert styler(sent, 2) == "하지 말라고 일렀습니다."
    sent = "드디어 정상에 이르렀다."
    assert styler(sent, 0) == "드디어 정상에 이르렀다."
    assert styler(sent, 1) == "드디어 정상에 이르렀어요."
    assert styler(sent, 2) == "드디어 정상에 이르렀습니다."


@pytest.mark.skip()
def test_contextual_3(styler):
    """
    쓰레기를 주워요 -> 쓰레기를 주웁시다 / 쓰레기를 줍습니다 (존대 종결어미 선정에 맥락이 관여하는 경우)
    둘다 가능하다. 이 경우는 맥락이 필요하다. 규칙만으로는 불가능하다.
    # 자세한 설명: https://github.com/eubinecto/politely/issues/60#issuecomment-1126839221
    """
    sent = "저는 쓰레기를 주워요."
    assert styler(sent, 0) == "나는 쓰레기를 주워."
    assert styler(sent, 1) == "저는 쓰레기를 주워요."
    assert styler(sent, 2) == "저는 쓰레기를 줍습니다."
    sent = "같이 쓰레기를 주워요."
    assert styler(sent, 0) == "같이 쓰레기를 줍자."
    assert styler(sent, 1) == "같이 쓰레기를 주워요."
    assert styler(sent, 2) == "같이 쓰레기를 주웁시다."


@pytest.mark.skip()
def test_contextual_4(styler):
    """
    이것도 마찬가지로 맥락이 필요하다.
    떠나요 -> 떠나 / 떠나자, 둘 중 무엇이 정답인지는 맥락을 보아야만 알 수 있다.
    떠나요 -> 떠납니다 / 떠납시다 -> 둘 중 무엇이 맞는지도... 마찬가지
    """
    sent = "자, 떠나요. 동해 바다로."
    assert styler(sent, 0) == "자, 떠나자. 동해 바다로."
    assert styler(sent, 1) == "자, 떠나요. 동해 바다로."
    assert styler(sent, 2) == "자, 떠납시다. 동해 바다로."


@pytest.mark.skip()
def test_contextual_5(styler):
    sent = "가까우니까 걸어가요."
    assert styler(sent, 0) == "가까우니까 걸어가."
    assert styler(sent, 1) == "가까우니까 걸어가요."
    assert styler(sent, 2) == "가까우니까 걸어갑시다."
