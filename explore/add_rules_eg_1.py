from politely import Styler
styler = Styler()
sent = "한글은 한국의 글자이다."
styler.rules.clear()  # just for demonstration
print(styler(sent, 1))  # should be wrong
styler.add_rules(
    {"이🏷VCP🔗(?P<MASK>다🏷EF)": (
        {"다🏷EF"},
        {"에요🏷EF"},  # 에요.
        {"습니다🏷EF"},
    )
    })
print(styler(sent, 1))  # should be this