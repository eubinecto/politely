"""
regular expression -> can be used for query normalization.
using regular expressions.
해 | 해요 | 하자 ->
"""
import re
# what do you want?
# you do want sub... but maybe, do that individually?
# here, how do I preserve the last character, without backreference?

# named capturing groups are referenced with \g<name> syntax
print(re.sub(r"(해|해요|하자)(?P<named>[!.?])", r"해요\g<named>", "이거 같이 하자!"))
print(re.sub(r"(해|해요|하자)(?P<named>[!.?])", r"해요\g<named>", "이거 같이 해?"))
print(re.sub(r"(해|해요|하자)(?P<named>[!.?])", r"해요\g<named>", "이거 같이 해요."))
