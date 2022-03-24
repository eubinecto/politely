
import pandas as pd


before = [
    "난",
    "달려"
]

after = [
    "`전`",
    "달`려요`"
]


def main():
    df = pd.DataFrame(zip(before, after), columns=["before", "after"])
    print(df)


# yup! so that's how you build it. All you need now is
"""
  before  after
0      난    `전`
1     달려  달`려요`
"""

if __name__ == '__main__':
    main()
