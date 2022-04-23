import pandas as pd
from politely.fetchers import fetch_rules, fetch_honorifics


def main():
    df = pd.DataFrame(fetch_rules())
    print(df.transpose())
    df = pd.DataFrame(fetch_honorifics())
    print(df.transpose())

if __name__ == '__main__':
    main()
