import inspect


def save_args():
    myframe = inspect.currentframe()
    # crawl up
    out = inspect.getargvalues(myframe.f_back)
    print(out.locals)


def show_hello_world_basic(name="World", more="haha"):
    # gets the current frame and examines arg
    save_args()
    # prints greeting
    print("Hello {}!".format(name))


def main():
    show_hello_world_basic()


if __name__ == '__main__':
    main()