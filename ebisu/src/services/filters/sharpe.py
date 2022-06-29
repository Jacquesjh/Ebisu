
import pandas as pd

from athena.src.core.services.filter import Filter
from athena.src.utils import utils


class Sharpe(Filter):

    """
    """


    @staticmethod
    def process(raw_df: pd.DataFrame, num_tickers: int) -> pd.DataFrame:
        prices = raw_df["Close"]
        
        mean   = prices.pct_change().mean()
        std    = prices.pct_change().std()
        sharpe = (mean/std).sort_values(ascending = False)

        top_tickers  = sharpe.index[: num_tickers]
        processed_df = utils.rebuild_dataframe(raw_df = raw_df, top_tickers = top_tickers)

        return processed_df


def sharpe_filter(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    num_tickers = parameters.get("num_tickers", None)

    sharpe_df = Sharpe.process(raw_df = df, num_tickers = num_tickers)

    return sharpe_df