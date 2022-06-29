
import numpy as np
import pandas as pd

from athena.src.core.services.filter import Filter
from athena.src.utils import utils


class Sortino(Filter):

    """
    """


    @staticmethod
    def process(raw_df: pd.DataFrame, num_tickers: int) -> pd.DataFrame:
        prices = raw_df["Close"]
        
        mean         = prices.pct_change().mean()
        negative_std = np.where(prices.pct_change() < 0, prices.pct_change(), 0).std()
        sortino      = (mean/negative_std).sort_values(ascending = False)

        top_tickers  = sortino.index[: num_tickers]
        processed_df = utils.rebuild_dataframe(raw_df = raw_df, top_tickers = top_tickers)

        return processed_df

    
def sortino_filter(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    num_tickers = parameters.get("num_tickers", None)

    sortino_df = Sortino.process(raw_df = df, num_tickers = num_tickers)

    return sortino_df
