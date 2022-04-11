
"""
reference:
https://stackoverflow.com/a/59381603
"""

from kps.fetchers import fetch_rules
import pandas as pd


def main():
    rules = fetch_rules()
    df = pd.DataFrame(rules)
    print(df.loc['teacher']['private'])
    print(df.index)
    print(df.columns)


if __name__ == '__main__':
    main()