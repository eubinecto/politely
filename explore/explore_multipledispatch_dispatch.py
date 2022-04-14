"""
method overloading in python.
An example of polymorphism.
Didn't we could do this in Python!

Guido's article:
https://www.artima.com/weblogs/viewpost.jsp?thread=101605
"""

from multipledispatch import dispatch


@dispatch(int, int)
def add(a: int,  b: int) -> int:
    """
    add two numbers
    """
    return a + b


@dispatch(list)
def add(a: list) -> int:
    """
    sum up a list
    """
    return sum(a)


# you can do this with a member instance as well
class Styler:

    @dispatch(str, str, str)
    def __call__(self, sent: str,
                 listener: str,
                 environ: str):
        """
        Tune the sentence, but determine the politeness
        from the given options.
        """
        print(sent, listener, environ)

    @dispatch(str, int)
    def __call__(self, sent: str, politeness: int):
        """
        Tune the sentence with a given politeness level.
        """
        print(sent, politeness)


def main():
    print(add(1, 2))
    print(add([1, 2, 3, 4, 5]))
    styler = Styler()
    styler("hi", "friends", "private")
    styler("hi", 2)


if __name__ == '__main__':
    main()
