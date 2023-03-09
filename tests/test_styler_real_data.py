"""
Test Styler on real data (e.g. Wikipedia articles)
"""
from pprint import pprint
from politely import Styler
import pytest  # noqa
from politely.fetchers import fetch_kiwi

kiwi = fetch_kiwi()

HANGLE_WIKI = """한글(韓㐎[1], 영어: Hangeul[2]또는 Hangul[3])은 한국어의 공식문자로서, 세종이 한국어를 표기하기 위하여 창제한 문자인 '훈민정음'(訓民正音)을 20세기 초반 이후 달리 이르는 명칭이다.[4][5] 한글이란 이름은 주시경 선생과 국어연구학회 회원들에 의해 지어진것으로 알려져 있으며[6][7][8][9] 그 뜻은 '으뜸이 되는 큰글', '오직 하나뿐인 큰글', '한국인의 글자'이다.[6][10] 한글의 또 다른 별칭으로는 정음(正音), 언문(諺文)[11], 언서(諺書), 반절(反切), 암클, 아햇글, 가갸글, 국문(國文)[12] 등이 있다.[5]
음소문자인 한글은 홀소리(모음)와 닿소리(자음) 모두 소리틀을 본떠 만들었으며[13] 창제된 초기에는 닿소리 17개에 홀소리 11개, 총 28개였으나, 점차 4자(ㅿ, ㆁ, ㆆ, ㆍ)를 사용하지 않게 되어 현재는 홀소리 10자, 닿소리 14자만 쓰고 있다. 한글은 표음문자(소리글자)이자 자질문자로서 표의문자인 한자에 비해서 배우기 쉽고 읽고 쓰기가 쉬운 장점을 가지고 있다. 조선민주주의인민공화국에서는 '조선글'이라 부른다.
한글(훈민정음)은 창제된 이후 약 500년 동안 많은 시련을 겪었다. 조선의 선비들은 한글을 무시하고 홀대했으며 연산군은 한글 사용을 탄압했다.[14][15][16] 일제는 조선어학회 사건(1942)을 조작하는 등 한국어와 한글 사용을 금지하는 민족정신 말살정책을 펼쳤다. 이런 어려움 속에서도 주시경, 최현배등 많은 선각자들이 한글을 체계적으로 연구하여 한글의 우수성을 알리고 널리 보급하려 노력하였다.
1908년 국어연구학회가 창립된 이래 여러 시련에도 불구하고 한글연구의 명맥은 꾸준히 이어졌으며, 한글날 제정, 사전편찬, 맞춤법 제정등 많은 성과들을 일구어냈다. 광복후 '조선어학회'가 활동을 재개하였고 1949년에 '한글학회'로 개칭되면서 한글 표준화 사업등 많은 노력이 있었다. 그 결과 한글은 한국어를 표기하는 국어로서의 위상을 지키게 되었다."""

HANGLE_WIKI_SENTS = [
    sent.text
    for sent in kiwi.split_into_sents(HANGLE_WIKI)
]

HANGLE_NAMU = """세종이 훈민정음을 반포했을 당시에는 배우고 익히기 어려운 한자와 구별하여, 주로 백성들이 일상적으로 쓰는 글이라는 뜻에서 언문(諺文)이라고도 불렸다. 흔히 언문에 대해 '한글을 낮춰 부르는 말'이라는 오해가 있으나, 사실 '언문'이라는 명칭을 처음 사용한 것은 창제자인 세종대왕 본인이었기 때문에 당초에는 비하적 의미가 없었다는 것이 정설이다. 더 자세한 내용은 한글/역사 문서로.
구한말에는 '나라의 글'이란 뜻으로 '국문(國文)'이라 불렀다. 그러다 일제강점기를 전후하여 '한글'이라는 이름이 등장했고, 이것이 오늘날 한글을 가리키는 표준 명칭이 되었다. '한글'이라는 이름의 유래와 작명자에 대하여서는 꽤 다양한 견해가 있다.
현재 쓰이는 '한글'이라는 이름은 창시자가 불분명하지만 대체로 주시경이 약 1912년 경에 저술한 《소리갈》(음성학)이라는 책에서 처음 쓴 것으로 여겨지고 있다. 주시경은 1911년에 '국어'라는 말 대신에 '배달말'이라는 말을 쓴 적이 있었는데, 아무래도 '배달'이라는 단어가 생소할 수 있어 '한말', '한글'이라는 표현으로 바꾼 듯하다(고영근 2003: 140)(고영근(2003), '한글'의 作名父는 누구일까, 새국어생활 2003년 봄.)"""


HANGLE_NAMU_SENTS = [
    sent.text
    for sent in kiwi.split_into_sents(HANGLE_NAMU)
]


@pytest.fixture(scope="session")
def styler():
    return Styler(strict=True)


def test_raise_no_exceptions_on_hangle_wiki_to_1(styler):  # noqa
    try:
        for sent in HANGLE_WIKI_SENTS:
            styler(sent, 0)
    except Exception as e:
        pytest.fail(str(e), e)

def test_raise_no_exceptions_on_hangle_wiki_to_2(styler):  # noqa
    try:
        for sent in HANGLE_WIKI_SENTS:
            styler(sent, 1)
    except Exception as e:
        pytest.fail(str(e), e)


def test_raise_no_exceptions_on_hangle_wiki_to_3(styler):  # noqa
    try:
        for sent in HANGLE_WIKI_SENTS:
            styler(sent, 2)
    except Exception as e:
        pytest.fail(str(e), e)
