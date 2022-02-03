import pandas as pd
from politetune.loaders import load_honorifics


def main():
    honorifics = load_honorifics()
    print(honorifics)

    # and... you could build a dataframe out of the dictionary.
    # should be useful for visualizing the rules later.

    df = pd.DataFrame(honorifics)
    print(df)

if __name__ == '__main__':
    main()