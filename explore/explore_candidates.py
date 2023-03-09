

import itertools
from pprint import pprint

possibility = [{1, 2, 3}, {4, 5}, set()
]

# cartesian product
candidates = itertools.product(*possibility)
pprint(list(candidates))