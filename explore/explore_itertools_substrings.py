"""
https://stackoverflow.com/a/41204206
"""

import itertools


def main():
    x = ["시키/VV", "었/EP", "어/EF", "./SF"]
    substrings = [x[i:j] for i, j in itertools.combinations(range(len(x) + 1), 2)]
    for sub in substrings:
        print(sub)


if __name__ == "__main__":
    main()
