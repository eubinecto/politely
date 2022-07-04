
from kiwipiepy import Kiwi

short = "안녕하세요! 만나서 반갑습니다"
long = "한글(韓㐎[1], 영어: Hangeul[2]또는 Hangul[3])은 한국어의 공식문자로서, 세종이 한국어를 표기하기 위하여 창제한 문자인 '훈민정음'(訓民正音)을 20세기 초반 이후 달리 이르는 명칭이다.[4][5] 한글이란 이름은 주시경 선생과 국어연구학회 회원들에 의해 지어진것으로 알려져 있으며[6][7][8][9] 그 뜻은 '으뜸이 되는 큰글', '오직 하나뿐인 큰글', '한국인의 글자'이다.[6][10] 한글의 또 다른 별칭으로는 정음(正音), 언문(諺文)[11], 언서(諺書), 반절(反切), 암클, 아햇글, 가갸글, 국문(國文)[12] 등이 있다.[5]"

kiwi = Kiwi()
# this succeeds
print(kiwi.join(kiwi.tokenize(short)))
# but this does not
print(kiwi.join(kiwi.tokenize(long)))