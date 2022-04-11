from kps.fetchers import fetch_abbreviations
import pandas as pd


def main():
    abbreviations = fetch_abbreviations()
    df = pd.DataFrame.from_dict(abbreviations, orient='index', columns=["abbreviated"])
    print(df)
    print(df.loc["나의"])


if __name__ == '__main__':
    main()
