import re


def main():
    if re.match(".*\\+?다/EF\\+?.*", "했+다/EF"):
        print("matched")


if __name__ == "__main__":
    main()
