"""
reference:
https://stackoverflow.com/a/59381603
"""

from politely.fetchers import fetch_rules
import pandas as pd


def main():
    rules = fetch_rules()
    df = pd.DataFrame(rules).transpose()

    subsets = pd.IndexSlice[(0, 1), "col1"]
    df.style.applymap(lambda x: "background-color: yellow", subset=subsets)
    print(df)

    # toy example
    df = pd.DataFrame(
        {"i1": [0, 0, 0, 1, 1, 1], "i2": [0, 1, 2, 0, 1, 2], "col1": [1, 2, 3, 4, 5, 6]}
    ).set_index(["i1", "i2"])

    subset = pd.IndexSlice[[(0, 1), (1, 1)]]
    styler = df.style.applymap(lambda x: "background-color: yellow", subset=subset)
    print(styler)


if __name__ == "__main__":
    main()
