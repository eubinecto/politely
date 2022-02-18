from typing import Tuple
import pandas as pd
from tuner import Tuner


class Visualiser:
    """
    given a tuner, the visualiser
    visualises how the rules are applied
    :return (rules, honorifics, abbreviations)
    """
    def __init__(self, tuner: Tuner):
        self.tuner = tuner

    def __call__(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        pass

        # highlighters ->

    def highlight_rules(self) -> Styler:
        styler = pd.DataFrame(self.tuner.RULES).transpose().style
        subset = pd.IndexSlice[(self.tuner.listener, self.tuner.visibility)]
        styler = styler.applymap(lambda x: "background-color: purple", subset=subset)
        return styler

    def highlight_honorifics(self) -> Styler:
        styler = pd.DataFrame(self.tuner.HONORIFICS).transpose().style
        for token in self.tuner.tokens:
            if f"{token.form}+{token.tag}" in self.tuner.HONORIFICS.keys():
                subset = pd.IndexSlice[(f"{token.form}+{token.tag}", self.tuner.polite)]
                styler = styler.applymap(lambda x: "background-color: purple", subset=subset)
        return styler