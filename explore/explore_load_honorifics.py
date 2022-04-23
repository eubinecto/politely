import pandas as pd
from politely.fetchers import fetch_honorifics


def main():
    honorifics = fetch_honorifics()
    print(honorifics)

    # and... you could build a dataframe out of the dictionary.
    # should be useful for visualizing the rules later.

    df = pd.DataFrame(honorifics)
    print(df)

if __name__ == '__main__':
    main()