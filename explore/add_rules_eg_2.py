from pprint import pprint

from politely import SELF, Styler
styler = Styler()
styler.rules.clear()
sent = "아빠가 정실에 들어간다."
styler.add_rules(
    {
        r"(?P<MASK>(아빠|아버지|아버님)🏷NNG)": (
            {f"아빠🏷NNG"},
            {f"아버지🏷NNG", f"아버님🏷NNG"},
            {f"아버지🏷NNG", f"아버님🏷NNG"}
        ),
        r"(아빠|아버지|아버님)🏷NNG🔗(?P<MASK>\S+?🏷JKS)": (
            {SELF},
            {f"께서🏷JKS"},
            {f"께서🏷JKS"}
        ),
        r"(?P<MASK>ᆫ다🏷EF)": (
            {SELF},
            {"시🏷EP🔗어요🏷EF"},
            {"시🏷EP🔗습니다🏷EF"},
        )
    }
)
print(styler(sent, 1))
pprint(styler.logs['guess']['out'])