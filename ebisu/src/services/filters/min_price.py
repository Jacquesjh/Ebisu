
import pandas as pd

from athena.src.core.services.filter import Filter
from athena.src.utils import utils


class MinPrice(Filter):


    @staticmethod
    def process(raw_df: pd.DataFrame, cutoff: float) -> pd.DataFrame:
        top_tickers = []

        for ticker in raw_df["Close"].columns:
            if raw_df["Close"][ticker][-1] >= cutoff:
                top_tickers.append(ticker)

        processed_df = utils.rebuild_dataframe(raw_df = raw_df, top_tickers = top_tickers)

        return processed_df


def min_price_filter(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    cutoff = parameters.get("cutoff", None)

    min_price_df = MinPrice.process(raw_df = df, cutoff = cutoff)

    return min_price_df