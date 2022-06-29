
import pandas as pd

from athena.src.core.services.filter import Filter
from athena.src.utils import utils


class Volatility(Filter):

    """
    """


    @staticmethod
    def process(raw_df: pd.DataFrame, num_tickers: int) -> pd.DataFrame:
        prices = raw_df["Close"]
        
        std = prices.pct_change().std()
        std = std.sort_values()

        top_tickers  = std.index[: num_tickers]
        processed_df = utils.rebuild_dataframe(raw_df = raw_df, top_tickers = top_tickers)

        return processed_df


def volatility_filter(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    num_tickers = parameters.get("num_tickers", None)

    volatility_df = Volatility.process(raw_df = df, num_tickers = num_tickers)

    return volatility_df