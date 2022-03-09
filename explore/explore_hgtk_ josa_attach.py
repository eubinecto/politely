
import hgtk


def main():
    # 단어에.. 조사를 붙일 수 있다.
    print(hgtk.josa.attach('하늘', hgtk.josa.EUN_NEUN))
    print(hgtk.josa.attach('바다', hgtk.josa.EUN_NEUN))
    print(hgtk.josa.attach('하늘', hgtk.josa.EUL_REUL))
    print(hgtk.josa.attach('바다', hgtk.josa.EUL_REUL))
    print(hgtk.josa.attach('하늘', hgtk.josa.IDA_DA))
    print(hgtk.josa.attach('바다', hgtk.josa.IDA_DA))
    print(hgtk.josa.attach('하늘', hgtk.josa.EURO_RO))
    print(hgtk.josa.attach('바다', hgtk.josa.EURO_RO))
    print(hgtk.josa.attach('태양', hgtk.josa.EURO_RO))
    print(hgtk.josa.attach('하늘', hgtk.josa.GWA_WA))
    print(hgtk.josa.attach('바다', hgtk.josa.GWA_WA))

    # 다음과 같이 조사를 두음법칙에 맞게 붙이는 것이 가능하다.
    """
    하늘은
    바다는
    하늘을
    바다를
    하늘이다
    바다다
    하늘로
    바다로
    태양으로
    하늘과
    바다와
    """


if __name__ == '__main__':
    main()