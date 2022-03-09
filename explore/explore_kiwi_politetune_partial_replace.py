
from kiwipiepy import Kiwi
kiwi = Kiwi()


def main():
    # This is much better!
    sent = "나는 나의 가방을 들었다."
    tokens = kiwi.tokenize(sent)
    # two-word
    for curr in tokens:
        print(curr)

    for idx, curr in enumerate(tokens):
        # what I think would be a better tactic is just to map out
        # every rule
        if f"{curr.form}+{curr.tag}" == "나+NP":
            after = tokens[idx + 1]
            if f"{after.form}+{after.tag}" == "의+JKG":
                sent = sent[:curr.start] + "저의" + sent[curr.end:]
            else:
                sent = sent[:curr.start] + "저" + sent[curr.end:]

        if f"{curr.form}+{curr.tag}" == "다+EF":
            sent = sent[:curr.start] + "어요" + sent[curr.end:]

    print(sent)


if __name__ == '__main__':
    main()
