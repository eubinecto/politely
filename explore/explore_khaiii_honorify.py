from khaiii import KhaiiiApi

api = KhaiiiApi()

sents = [
    "시끄럽게 코고는 소리에 놀라서 난 잠이 깼다.",
    "나는 달리고 있어.",
    "나는 노래를 듣고 있어요.",
]

HONORIFICS = {
    "다/EF": ("어", "어요"),
    "어/EF": ("어", "어요"),
    "어요/EF": ("어", "어요"),
    "나/NP": ("나", "저"),
    "저/NP": ("나", "저")
}


def main():
    polite = 1
    for sent in sents:
        tokens = api.analyze(sent)
        lexicon2morphs = [(token.lex, list(map(str, token.morphs))) for token in tokens]
        # style 1 - list comprehension maniac
        tuned = [
            "".join([
                HONORIFICS[morph][polite] if morph in HONORIFICS
                else morph.split("/")[0]
                for morph in morphs
            ])
            if set(morphs) & set(HONORIFICS.keys()) else lex
            for lex, morphs in lexicon2morphs
        ]
        print(" ".join(tuned))  # right, you could just give up on highlighting.


if __name__ == '__main__':
    main()
