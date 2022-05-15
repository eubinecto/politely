import hgtk


def main():
    print(hgtk.letter.decompose("난"))
    print(hgtk.text.decompose("난 너가 좋아"))
    print(hgtk.text.decompose("먹ㅂ시다."))  # 앞 글자에 ㄱ 종성이 있으면.. 읍
    print(hgtk.text.decompose("시작하겠ㅂ니다."))  # 앞 글자에 종성이 있으면.. 습
    print(hgtk.text.decompose("처리했ㅂ니다."))  #  앞 글자에 ㅅ 종성.. 습.
    print(hgtk.text.decompose("처리하ㅂ니다."))  # 종성이 없으면.. 종성으로 들어간다.
    print(hgtk.text.decompose("ㅂ시다"))
    # ㅂ시다 -> 이게 그렇게 문제가 있는 것 같다면.. 어차피 너가 해결해야하는 것이 그거니까.


if __name__ == '__main__':
    main()
