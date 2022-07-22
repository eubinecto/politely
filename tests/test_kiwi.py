import pytest
from kiwipiepy import Kiwi
from politely.fetchers import fetch_kiwi


@pytest.fixture(scope="session")
def kiwi() -> Kiwi:
    return fetch_kiwi()


# --- testing the `add_..` functions --- #
def test_add_user_word_urimal_as_a_noun(kiwi):
    """
    우리말 -> 우리 말 (x) 우리말 (o)
    """
    sent = "이맘때면 우리말 글에 대한 기사와 기고문이 쏟아진다."
    assert kiwi.join(kiwi.tokenize(sent)) == sent  # noqa


def test_add_pre_analyzed_word_but_seo_period(kiwi):
    sent = "한국의 목욕탕에서는 옷을 벗어."
    assert "어/EF" in [token.tagged_form for token in kiwi.tokenize(sent)]


# --- testing the `join` function --- #
def test_join_double_syllables_1(kiwi):
    """
    동모음 탈락
    가어요 (x)
    가요 (o)
    """
    assert "가요" == kiwi.join([("가", "VV"), ("어요", "EF")])


def test_join_double_syllables_2(kiwi):
    """
    동모음 탈락
    떠나어요 (x)
    떠나요 (o)
    """
    assert "떠나요" == kiwi.join([("떠나", "VV"), ("어요", "EF")])


# --- these don't work for now --- #
@pytest.mark.skip()
def test_join_ah_jut(kiwi):
    sent = "한글은 어떻게 만들어졌나요?"
    assert kiwi.join(kiwi.tokenize(sent)) == sent  # noqa