
import random

import pandas as pd

from athena.src.core.services.filter import Filter
from athena.src.utils import utils


class Random(Filter):

    """


            The Random strategy simply randomly selects N assets from a dataframe.
        This simplistic strategy follows the idea that sometimes, in the investing sphere, very simple
        technique tend to outperform, or perform similarly, much more sophisticated ones. With this idea
        in mind, I found it worth it to include this selection option in this backtest (mainly out of curiosity).

        In this implementation you can tweak:

            num_tickers [int]: The number of assets that you want to end up being selected.


    """


    @staticmethod
    def process(raw_df: pd.DataFrame, num_tickers: int) -> pd.DataFrame:
        available_tickers = list(raw_df["Close"].columns)

        top_tickers = []

        if num_tickers > len(available_tickers):
            num_tickers = len(available_tickers)

        for _ in range(num_tickers):
            random.seed(37)
            chosen = random.choice(available_tickers)

            available_tickers.remove(chosen)
            top_tickers.append(chosen)

        processed_df = utils.rebuild_dataframe(raw_df = raw_df, top_tickers = top_tickers)

        return processed_df


def random_filter(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    num_tickers = parameters.get("num_tickers", None)

    random_df = Random.process(raw_df = df, num_tickers = num_tickers)
    
    return random_df