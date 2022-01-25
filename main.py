"""
그냥 처음엔 막코딩하자. just put everything under here.
It's okay to write dirty stuff, at least as of right now.
"""
import argparse
from typing import List, Dict, Tuple
from konlpy.tag import Okt
from termcolor import colored
import re

RULES: Dict[str, Tuple[int, int]] = {
    "t": (1, 1),  # teacher
    "baw": (1, 1),  # boss at work
    "os": (0, 0),  # older sister
    "ob": (0, 0),  # older brother
    "oc": (0, 0),  # older cousin
    "ys": (0, 0),  # younger sister
    "yb": (0, 0),  # younger brother
    "yc": (0, 0),  # younger cousin
    "u": (1, 1),  # uncle
    "f": (0, 1),  # friend
    "gpa": (1, 1),  # grandpa
    "gma": (1, 1),  # grandma
    "m": (0, 1),  # mum
    "d": (1, 1),  # dad
    "sc": (1, 1)  # shop clerk
}

HONORIFICS: Dict[str, Tuple[str, str]] = {
    "하다": ("해", "해요"),  # this covers pretty much all the -하다 verbs.
    "마시다": ("마셔", "마셔요"),
    "알다": ("알아", "알아요"),
    "모르다": ("몰라", "몰라요"),
    "듣다": ("들어", "들어요"),
    "사다": ("사", "사요"),
    "보다": ("봐", "봐요"),
    "가다": ("가", "가요"),
    "오다": ("와", "와요"),
    "아프다": ("아파", "아파요"),
    "목마르다": ("목말라", "목말라요"),
    "배고프다": ("배고파", "배고파요"),
    "고맙다": ("고마워", "고마워요")
}

# M1 quark
JVM_PATH = '/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/bin/java'


def main():
    # parsing the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--sent", "--s", type=str, default="나는 공부할래")
    # choose the two options
    parser.add_argument("--listener", "--l", type=str, choices=RULES.keys())
    parser.add_argument("--visibility", "--v", type=int, choices=[0, 1])  # 0 = private, 1 = public.

    args = parser.parse_args()
    # decide if you should be polite or not
    polite = RULES[args.listener][args.visibility]
    # first, tokenize & lemmatize words
    okt = Okt(jvmpath=JVM_PATH)
    # then, polite-tune the tokens.
    tuned = args.sent
    for token, lemma in zip(okt.morphs(args.sent, stem=False), okt.morphs(args.sent, stem=True)):
        if lemma in HONORIFICS.keys() and token != HONORIFICS[lemma][polite]:
            tuned = tuned.replace(token, colored(HONORIFICS[lemma][polite], color="blue"))
    # print out the results
    print(f"{args.sent} -> {tuned}")
    print(f"listener: {args.listener},"
          f"\nvisibility: {args.visibility},"
          f"\npoliteness: {polite}")


if __name__ == '__main__':
    main()
