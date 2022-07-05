"""
regular expression -> can be used for query normalization.
using regular expressions.
해 | 해요 | 하자 ->
"""
import re

# https://stackoverflow.com/q/20765265
sent = "나랑 같이 해요!"
sent = re.sub(r"(해|해요|하자)(!|\\.)", r"해요\2", sent)
print(sent)

