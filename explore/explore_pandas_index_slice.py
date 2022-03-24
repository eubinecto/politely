from fetchers import fetch_rules
import pandas as pd


def main():
    rules = fetch_rules()
    styler = pd.DataFrame(rules).transpose().style
    subset = pd.IndexSlice[("friend", "private")]
    styler = styler.applymap(lambda x: x, subset=("friend", "private"))
    print(type(subset))
    print(subset)
    print(rules[subset[0]][subset[1]])  # 아하.



if __name__ == '__main__':
    main()