from khaiii import KhaiiiApi
import itertools


api = KhaiiiApi()

sents = [
    "시끄럽게 코고는 소리에 놀라서 난 잠이 깼다.",
    "나는 달리고 있어.",
    "나는 노래를 듣고 있어요.",
    "엄마와 함께 밥을 먹고 있어.",
    "엄마가 심부름을 시켰어.",
    "그는 전설이다.",
]

HONORIFICS = {
    "이/VCP+다/EF": ("이야", "이에요"),
    "다/EF": ("어", "어요"),
    "어/EF": ("어", "어요"),
    "어요/EF": ("어", "어요"),
    "나/NP": ("나", "저"),
    "저/NP": ("나", "저"),
    "가/JKS": ("가", "께서"),
    "엄마/NNG": ("엄마", "어머니")
}


def main():
    polite = 1
    for sent in sents:
        tokens = api.analyze(sent)
        lexicon2morphs = [(token.lex, list(map(str, token.morphs))) for token in tokens]
        # style 1 - list comprehension maniac
        out = list()
        for lex, morphs in lexicon2morphs:
            # this is to be used just for matching
            substrings = ["+".join(morphs[i:j]) for i, j in itertools.combinations(range(len(morphs) + 1), 2)]
            if set(substrings) & set(HONORIFICS.keys()):  # need to make sure any patterns match joined.
                tuned = "+".join(morphs)
                for pattern in HONORIFICS.keys():
                    tuned = tuned.replace(pattern, HONORIFICS[pattern][polite])
                tuned = "".join([token.split("/")[0] for token in tuned.split("+")])
                out.append(tuned)
            else:
                out.append(lex)
        print(" ".join(out))
"""
when polite = 0
시끄럽게 코고는 소리에 놀라서 저ㄴ 잠이 깨었어요.
저는 달리고 있어요.
저는 노래를 듣고 있어요.

when polite = 1 
시끄럽게 코고는 소리에 놀라서 나ㄴ 잠이 깨었어.
나는 달리고 있어.
나는 노래를 듣고 있어.
"""

if __name__ == '__main__':
    main()
