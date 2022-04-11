from khaiii import KhaiiiApi
import itertools


api = KhaiiiApi()

sents = [
    "시끄럽게 코고는 소리에 놀라서 난 잠이 깼다.",
    "나는 달리고 있어.",
    "나는 달린다.",
    "나는 달려.",
    "나는 노래를 듣고 있어요.",
    "엄마와 함께 밥을 먹고 있어.",
    "엄마가 심부름을 시켰어.",
    "그는 전설이다.",
    "그는 전설이에요."
]

HONORIFICS = {
    "이/VCP+다/EF": ("이/VCP+다/EF", "이/VCP+에요/EF"),
    "이/VCP+에요/EF": ("이/VCP+다/EF", "이/VCP+에요/EF"),
    "ㄴ다/EF": ("ㄴ다/EF", "어요/EF"),
    "다/EF": ("다/EF", "어요/EF"),
    "어/EF": ("어/EF", "어요/EF"),
    "어요/EF": ("어/EF", "어요/EF"),
    "나/NP": ("나/NP", "저/NP"),
    "저/NP": ("나/NP", "저/NP"),
    "가/JKS": ("가/JKS", "께서/JKS"),
    "엄마/NNG": ("엄마/NNG", "어머니/NNG")
}

ABBREVIATIONS = {
    "저ㄴ": "전",
    "리어": "려",
    "키었": "켰"
}


def main():
    politeness = 1
    history = list()
    for sent in sents:
        print("========")
        tokens = api.analyze(sent)
        lexicon2morphs = [(token.lex, list(map(str, token.morphs))) for token in tokens]
        print("morphemes:", lexicon2morphs)
        # style 1 - list comprehension maniac
        out = list()
        for lex, morphs in lexicon2morphs:
            # look, how do we know if those morphs are valid or invalid?
            # you've got to go through the patterns for sure.
            # if there was no "continue", then we append the lex.
            tuned = "+".join(morphs)
            for pattern in HONORIFICS.keys():
                if pattern in tuned:
                    honorific = HONORIFICS[pattern][politeness]
                    if honorific not in tuned:  # this is the if statement to use for logging the history.
                        tuned = tuned.replace(pattern, honorific)
                        history.append((pattern, honorific))
            # if something has changed, then go for it, but otherwise just use the lex.
            if tuned != "+".join(morphs):
                tuned = "".join([token.split("/")[0] for token in tuned.split("+")])
                out.append(tuned)
            else:
                out.append(lex)
        out = " ".join(out)
        for key, val in ABBREVIATIONS.items():
            out = out.replace(key, val)
        print("history:", history)
        print("out:", out)
        history.clear()

"""
when politeness = 0
========
morphemes: [('시끄럽게', ['시끄럽/VA', '게/EC']), ('코고는', ['코/NNG', '골/VV', '는/ETM']), ('소리에', ['소리/NNG', '에/JKB']), ('놀라서', ['놀라/VV', '아서/EC']), ('난', ['나/NP', 'ㄴ/JX']), ('잠이', ['잠/NNG', '이/JKS']), ('깼다.', ['깨/VV', '었/EP', '다/EF', './SF'])]
history: []
out: 시끄럽게 코고는 소리에 놀라서 난 잠이 깼다.
========
morphemes: [('나는', ['나/NP', '는/JX']), ('달리고', ['달리/VV', '고/EC']), ('있어.', ['있/VX', '어/EF', './SF'])]
history: []
out: 나는 달리고 있어.
========
morphemes: [('나는', ['나/NP', '는/JX']), ('달린다.', ['달리/VV', 'ㄴ다/EF', './SF'])]
history: []
out: 나는 달린다.
========
morphemes: [('나는', ['나/NP', '는/JX']), ('달려.', ['달리/VV', '어/EF', './SF'])]
history: []
out: 나는 달려.
========
morphemes: [('나는', ['나/NP', '는/JX']), ('노래를', ['노래/NNG', '를/JKO']), ('듣고', ['듣/VV', '고/EC']), ('있어요.', ['있/VX', '어요/EF', './SF'])]
history: [('어요/EF', '어/EF')]
out: 나는 노래를 듣고 있어.
========
morphemes: [('엄마와', ['엄마/NNG', '와/JKB']), ('함께', ['함께/MAG']), ('밥을', ['밥/NNG', '을/JKO']), ('먹고', ['먹/VV', '고/EC']), ('있어.', ['있/VX', '어/EF', './SF'])]
history: []
out: 엄마와 함께 밥을 먹고 있어.
========
morphemes: [('엄마가', ['엄마/NNG', '가/JKS']), ('심부름을', ['심부름/NNG', '을/JKO']), ('시켰어.', ['시키/VV', '었/EP', '어/EF', './SF'])]
history: []
out: 엄마가 심부름을 시켰어.
========
morphemes: [('그는', ['그/NP', '는/JX']), ('전설이다.', ['전설/NNG', '이/VCP', '다/EF', './SF'])]
history: []
out: 그는 전설이다.
========
morphemes: [('그는', ['그/NP', '는/JX']), ('전설이에요.', ['전설/NNG', '이/VCP', '에요/EF', './SF'])]
history: [('이/VCP+에요/EF', '이/VCP+다/EF')]
out: 그는 전설이다.
"""

"""
when politeness = 1
========
morphemes: [('시끄럽게', ['시끄럽/VA', '게/EC']), ('코고는', ['코/NNG', '골/VV', '는/ETM']), ('소리에', ['소리/NNG', '에/JKB']), ('놀라서', ['놀라/VV', '아서/EC']), ('난', ['나/NP', 'ㄴ/JX']), ('잠이', ['잠/NNG', '이/JKS']), ('깼다.', ['깨/VV', '었/EP', '다/EF', './SF'])]
history: [('나/NP', '저/NP'), ('다/EF', '어요/EF')]
out: 시끄럽게 코고는 소리에 놀라서 전 잠이 깨었어요.
========
morphemes: [('나는', ['나/NP', '는/JX']), ('달리고', ['달리/VV', '고/EC']), ('있어.', ['있/VX', '어/EF', './SF'])]
history: [('나/NP', '저/NP'), ('어/EF', '어요/EF')]
out: 저는 달리고 있어요.
========
morphemes: [('나는', ['나/NP', '는/JX']), ('달린다.', ['달리/VV', 'ㄴ다/EF', './SF'])]
history: [('나/NP', '저/NP'), ('ㄴ다/EF', '어요/EF')]
out: 저는 달려요.
========
morphemes: [('나는', ['나/NP', '는/JX']), ('달려.', ['달리/VV', '어/EF', './SF'])]
history: [('나/NP', '저/NP'), ('어/EF', '어요/EF')]
out: 저는 달려요.
========
morphemes: [('나는', ['나/NP', '는/JX']), ('노래를', ['노래/NNG', '를/JKO']), ('듣고', ['듣/VV', '고/EC']), ('있어요.', ['있/VX', '어요/EF', './SF'])]
history: [('나/NP', '저/NP')]
out: 저는 노래를 듣고 있어요.
========
morphemes: [('엄마와', ['엄마/NNG', '와/JKB']), ('함께', ['함께/MAG']), ('밥을', ['밥/NNG', '을/JKO']), ('먹고', ['먹/VV', '고/EC']), ('있어.', ['있/VX', '어/EF', './SF'])]
history: [('엄마/NNG', '어머니/NNG'), ('어/EF', '어요/EF')]
out: 어머니와 함께 밥을 먹고 있어요.
========
morphemes: [('엄마가', ['엄마/NNG', '가/JKS']), ('심부름을', ['심부름/NNG', '을/JKO']), ('시켰어.', ['시키/VV', '었/EP', '어/EF', './SF'])]
history: [('가/JKS', '께서/JKS'), ('엄마/NNG', '어머니/NNG'), ('어/EF', '어요/EF')]
out: 어머니께서 심부름을 시켰어요.
========
morphemes: [('그는', ['그/NP', '는/JX']), ('전설이다.', ['전설/NNG', '이/VCP', '다/EF', './SF'])]
history: [('이/VCP+다/EF', '이/VCP+에요/EF')]
out: 그는 전설이에요.
========
morphemes: [('그는', ['그/NP', '는/JX']), ('전설이에요.', ['전설/NNG', '이/VCP', '에요/EF', './SF'])]
history: []
out: 그는 전설이에요.
"""

if __name__ == '__main__':
    main()
