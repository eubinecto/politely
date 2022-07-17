import re

print(chr(44032))  # 가 - 한글의 유니코드 값은 44032에서 시작 (hexadecimal = 0xAC00)
# 한글의 종성은 28개. 받침없음도 종성에 포함. 28의 배수를 더하면 종성이 없는 다음 글자를 얻을 수 있음
print(chr(44032 + 28))  # 개
print(chr(44032 + 28 * 2))  # 갸
print(chr(44032 + 28 * 3))  # 걔
print(chr(44032 + 28 * 4))  # 거
print(chr(44032 + 28 * 5))  # 게
print(chr(44032 + 28 * 6))  # 겨
print(chr(44032 + 28 * 7))  # 계
...
print(chr(44032 + 28 * 398))  # 히 - 398번 반복하면 종성이 없는 마지막 글자인 "히"에 도덜
print("---")
print(chr(55176 + 27))  # 힣 - 한글의 마지막 글자
print(chr(55176 + 28))  # 힤 - 당연히 28까지 더하면 한글이 아님.
print(55176 + 27)
# 44032애서 시작. 마지막 종성없는 글자인 44032 + 28 * 398 = 55176까지 모아주면 종성없는 글자 모임 완성.
# 그걸 정규표현식으로 묶어주면 끝.
NO_JONG_SUNG = rf"({'|'.join([chr(44032 + 28 * i) for i in range(399)])})"
# 활용 에 - 문장에서 모든 종성 찾아내기
print(re.findall(NO_JONG_SUNG, "한글 NLP 엔지니어가 되려면"))  # ['지', '니', '어', '가', '되', '려']
print(
    re.findall(NO_JONG_SUNG, "유니코드 공부좀 더 해야겠다")
)  # ['유', '니', '코', '드', '부', '더', '해', '야', '다']
print(
    re.findall("\uAC00", "유니코드 공부좀 더 해야겠다 아이가")
)  # ['유', '니', '코', '드', '부', '더', '해', '야', '다']
