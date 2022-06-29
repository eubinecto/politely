from enum import Enum, auto


class Color(Enum):
    RED = auto()
    RED_VELVET = auto()
    BLUE = auto()


def main():
    print([color.name.lower() for color in Color])
    print(Color["RED"].value)


if __name__ == "__main__":
    main()
