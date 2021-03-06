# the patterns to use
HONORIFICS = {
    ("이/VCP", "다/EF", r"(\.|\!)/SF"): {
        1: ("이/VCP", "다/EF", r"(\.|\!)/SF"),
        2: ("이/VCP", "에요/EF", r"(\.|\!)/SF"),
        3: ("이/VCP", "읍니다/EF", r"(\.|\!)/SF"),
    },
    ("말/VX", "어/EF", r"(\.|\!)/SF"): {
        1: ("말/VX", "어/EF", r"(\.|\!)/SF"),
        2: ("말/VX", "어요/EF", r"(\.|\!)/SF"),
        3: ("마/VX", "십시오/EF", r"(\.|\!)/SF"),
    },
    ("말/VX", "어요/EF", r"(\.|\!)/SF"): {
        1: ("말/VX", "어/EF", r"(\.|\!)/SF"),
        2: ("말/VX", "어요/EF", r"(\.|\!)/SF"),
        3: ("마/VX", "십시오/EF", r"(\.|\!)/SF"),
    },
    ("보/VX", "어/EF", r"(\.|\!)/SF"): {
        1: ("보/VX", "어/EF", r"(\.|\!)/SF"),
        2: ("보/VX", "어요/EF", r"(\.|\!)/SF"),
        3: ("보/VX", "읍시다/EF", r"(\.|\!)/SF"),
    },
    ("보/VX", "어요/EF", r"(\.|\!)/SF"): {
        1: ("보/VX", "어/EF", r"(\.|\!)/SF"),
        2: ("보/VX", "어요/EF", r"(\.|\!)/SF"),
        3: ("보/VX", "읍시다/EF", r"(\.|\!)/SF"),
    },
    ("시/EP", "어요/EF", r"(\.|\!)/SF"): {
        1: ("어/EF", r"(\.|\!)/SF"),
        2: ("시/EP", "어요/EF", r"(\.|\!)/SF"),
        3: ("십/EP", "시오/EF", r"(\.|\!)/SF"),
    },
    ("시/EP", "어요/EF", "?/SF"): {
        1: ("어/EF", "?/SF"),
        2: ("시/EP", "어요/EF", "?/SF"),
        3: ("시/EP", "읍니까/EF", "?/SF"),
    },
    ("니/EF", "?/SF"): {
        1: ("니/EF", "?/SF"),
        2: ("나요/EF", "?/SF"),
        3: ("읍니까/EF", "?/SF"),
    },
    ("대/EF", "?/SF"): {
        1: ("대/EF", "?/SF"),
        2: ("대요/EF", "?/SF"),
        3: ("답니까/EF", "?/SF"),
    },
    ("대요/EF", "?/SF"): {
        1: ("대/EF", "?/SF"),
        2: ("대요/EF", "?/SF"),
        3: ("답니까/EF", "?/SF"),
    },
    ("어/EF", "?/SF"): {
        1: ("어/EF", "?/SF"),
        2: ("어요/EF", "?/SF"),
        3: ("읍니까/EF", "?/SF"),
    },
    ("어요/EF", "?/SF"): {
        1: ("어/EF", "?/SF"),
        2: ("어요/EF", "?/SF"),
        3: ("읍니까/EF", "?/SF"),
    },
    ("죠/EF", "?/SF"): {1: ("지/EF", "?/SF"), 2: ("죠/EF", "?/SF"), 3: ("읍니까/EF", "?/SF")},
    ("야/EF", "?/SF"): {1: ("야/EF", "?/SF"), 2: ("죠/EF", "?/SF"), 3: ("읍니까/EF", "?/SF")},
    ("습니까/EF", "?/SF"): {
        1: ("어/EF", "?/SF"),
        2: ("어요/EF", "?/SF"),
        3: ("습니까/EF", "?/SF"),
    },
    ("ㅂ니까/EF", "?/SF"): {
        1: ("어/EF", "?/SF"),
        2: ("어요/EF", "?/SF"),
        3: ("읍니까/EF", "?/SF"),
    },
    ("ㄹ까요/EF", "?/SF"): {
        1: ("ㄹ까/EF", "?/SF"),
        2: ("ㄹ까요/EF", "?/SF"),
        3: ("읍니까/EF", "?/SF"),
    },
    ("지/EF", "?/SF"): {1: ("지/EF", "?/SF"), 2: ("죠/EF", "?/SF"), 3: ("읍니까/EF", "?/SF")},
    ("을까/EF", "?/SF"): {
        1: ("을까/EF", "?/SF"),
        2: ("어요/EF", "?/SF"),
        3: ("읍니까/EF", "?/SF"),
    },
    ("을까요/EF", "?/SF"): {
        1: ("을까/EF", "?/SF"),
        2: ("을까요/EF", "?/SF"),
        3: ("읍니까/EF", "?/SF"),
    },
    ("나요/EF", "?/SF"): {
        1: ("어/EF", "?/SF"),
        2: ("나요/EF", "?/SF"),
        3: ("읍니까/EF", "?/SF"),
    },
    ("ᆫ다/EF", r"(\.|\!)/SF"): {
        1: ("ᆫ다/EF", r"(\.|\!)/SF"),
        2: ("어요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("는다/EF", r"(\.|\!)/SF"): {
        1: ("는다/EF", r"(\.|\!)/SF"),
        2: ("어요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("마/EF", r"(\.|\!)/SF"): {
        1: ("마/EF", r"(\.|\!)/SF"),
        2: ("마요/EF", r"(\.|\!)/SF"),
        3: ("말/VX", "시/EP", "ᆸ시오/EF", r"(\.|\!)/SF"),
    },
    ("마요/EF", r"(\.|\!)/SF"): {
        1: ("마/EF", r"(\.|\!)/SF"),
        2: ("마요/EF", r"(\.|\!)/SF"),
        3: ("말/VX", "시/EP", "ᆸ시오/EF", r"(\.|\!)/SF"),
    },
    ("ᆫ대요/EF", r"(\.|\!)/SF"): {
        1: ("ᆫ대/EF", r"(\.|\!)/SF"),
        2: ("ᆫ대요/EF", r"(\.|\!)/SF"),
        3: ("ᆫ답니다/EF", r"(\.|\!)/SF"),
    },
    ("아/EF", r"(\.|\!)/SF"): {
        1: ("아/EF", r"(\.|\!)/SF"),
        2: ("아요/EF", r"(\.|\!)/SF"),
        3: ("읍시다/EF", r"(\.|\!)/SF"),
    },
    ("다/EF", r"(\.|\!)/SF"): {
        1: ("다/EF", r"(\.|\!)/SF"),
        2: ("어요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("자/EF", r"(\.|\!)/SF"): {
        1: ("자/EF", r"(\.|\!)/SF"),
        2: ("어요/EF", r"(\.|\!)/SF"),
        3: ("읍시다/EF", r"(\.|\!)/SF"),
    },
    ("ᆯ게/EF", r"(\.|\!)/SF"): {
        1: ("ᆯ게/EF", r"(\.|\!)/SF"),
        2: ("ᆯ게요/EF", r"(\.|\!)/SF"),
        3: ("겠/EP", "습니다/EF", r"(\.|\!)/SF"),
    },
    ("ᆯ게요/EF", r"(\.|\!)/SF"): {
        1: ("ᆯ게/EF", r"(\.|\!)/SF"),
        2: ("ᆯ게요/EF", r"(\.|\!)/SF"),
        3: ("겠/EP", "습니다/EF", r"(\.|\!)/SF"),
    },
    ("어/EF", r"(\.|\!)/SF"): {
        1: ("어/EF", r"(\.|\!)/SF"),
        2: ("어요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("야/EF", r"(\.|\!)/SF"): {
        1: ("야/EF", r"(\.|\!)/SF"),
        2: ("에요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("어요/EF", r"(\.|\!)/SF"): {
        1: ("어/EF", r"(\.|\!)/SF"),
        2: ("어요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("아요/EF", r"(\.|\!)/SF"): {
        1: ("아/EF", r"(\.|\!)/SF"),
        2: ("아요/EF", r"(\.|\!)/SF"),
        3: ("읍시다/EF", r"(\.|\!)/SF"),
    },
    ("네요/EF", r"(\.|\!)/SF"): {
        1: ("네/EF", r"(\.|\!)/SF"),
        2: ("네요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("군요/EF", r"(\.|\!)/SF"): {
        1: ("군/EF", r"(\.|\!)/SF"),
        2: ("군요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("요/EF", r"(\.|\!)/SF"): {
        1: ("어/EF", r"(\.|\!)/SF"),
        2: ("요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("에요/EF", r"(\.|\!)/SF"): {
        1: ("야/EF", r"(\.|\!)/SF"),
        2: ("에요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("ᆫ대/EF", r"(\.|\!)/SF"): {
        1: ("ᆫ대/EF", r"(\.|\!)/SF"),
        2: ("ᆫ대요/EF", r"(\.|\!)/SF"),
        3: ("ᆫ답니다/EF", r"(\.|\!)/SF"),
    },
    ("세요/EF", r"(\.|\!)/SF"): {
        1: ("어/EF", r"(\.|\!)/SF"),
        2: ("세요/EF", r"(\.|\!)/SF"),
        3: ("십/EP", "시오/EF", r"(\.|\!)/SF"),
    },
    ("너라/EF", r"(\.|\!)/SF"): {
        1: ("너라/EF", r"(\.|\!)/SF"),
        2: ("세요/EF", r"(\.|\!)/SF"),
        3: ("십/EP", "시오/EF", r"(\.|\!)/SF"),
    },
    ("거라/EF", r"(\.|\!)/SF"): {
        1: ("거라/EF", r"(\.|\!)/SF"),
        2: ("세요/EF", r"(\.|\!)/SF"),
        3: ("십/EP", "시오/EF", r"(\.|\!)/SF"),
    },
    ("네/EF", r"(\.|\!)/SF"): {
        1: ("네/EF", r"(\.|\!)/SF"),
        2: ("네요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("라/EF", r"(\.|\!)/SF"): {
        1: ("라/EF", r"(\.|\!)/SF"),
        2: ("세요/EF", r"(\.|\!)/SF"),
        3: ("읍시다/EF", r"(\.|\!)/SF"),
    },
    ("ᆸ니다/EF", r"(\.|\!)/SF"): {
        1: ("어/EF", r"(\.|\!)/SF"),
        2: ("어요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("습니다/EF", r"(\.|\!)/SF"): {
        1: ("어/EF", r"(\.|\!)/SF"),
        2: ("어요/EF", r"(\.|\!)/SF"),
        3: ("읍니다/EF", r"(\.|\!)/SF"),
    },
    ("저/NP",): {1: ("나/NP",), 2: ("저/NP",), 3: ("저/NP",)},
    ("나/NP",): {1: ("나/NP",), 2: ("저/NP",), 3: ("저/NP",)},
    ("내/NP",): {1: ("내/NP",), 2: ("제/NP",), 3: ("제/NP",)},
    ("제/NP",): {1: ("내/NP",), 2: ("제/NP",), 3: ("제/NP",)},
    ("너/NP",): {1: ("너/NP",), 2: ("당신/NP",), 3: ("여러분/NP",)},
    ("저희/NP",): {1: ("우리/NP",), 2: ("저희/NP",), 3: ("저희/NP",)},
    ("우리/NP",): {1: ("우리/NP",), 2: ("저희/NP",), 3: ("저희/NP",)},
}

# define this with emoji to prevent confusion with + as a regex notation
DELIM = "➕"
