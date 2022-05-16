from politely import Styler
from unittest import TestCase


def main():
    styler = Styler()
    testcase = TestCase()
    testcase.assertEqual("저는 쓰레기를 줍습니다.",
                         styler("저는 쓰레기를 주워요.", 3))
    testcase.assertEqual("자, 같이 쓰레기를 주웁시다.",
                         styler("자, 같이 쓰레기를 주워요.", 3))


if __name__ == '__main__':
    main()
