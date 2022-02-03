"""
regular expression -> can be used for query normalization.
using regular expressions.
해 | 해요 | 하자 ->
"""
import re


def main():
    sent = "나랑 같이 해요"
    sent = re.sub(r'(해|해요|하자)$', "해요", sent)
    print(sent)


if __name__ == '__main__':
    main()
