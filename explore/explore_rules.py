from politely.fetchers import fetch_rules


def main():
    rules = fetch_rules()
    print(rules.loc["teacher"]['private'])


if __name__ == '__main__':
    main()