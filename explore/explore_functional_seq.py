from functional import seq


def main():
    res = (
        seq(1, 2, 3, 4)
        .map(lambda x: x * 2)
        .filter(lambda x: x > 4)
        .reduce(lambda x, y: x + y)
    )
    print(res)  # you could reduce it.. or
    res = seq(1, 2, 3, 4).map(lambda x: x * 2).to_list()
    print(res)  # or you could turn it into a list


if __name__ == "__main__":
    main()
