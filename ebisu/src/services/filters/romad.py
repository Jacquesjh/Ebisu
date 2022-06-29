
import pandas as pd

from athena.src.core.services.filter import Filter
from athena.src.utils import utils


class RoMAD(Filter):

    """
    """


    @staticmethod
    def process(raw_df: pd.DataFrame, num_tickers: int) -> pd.DataFrame:
        prices = raw_df["Close"]
        
        df = pd.DataFrame(columns = prices.columns, index = ["romad"])

        for ticker in prices.columns:
            values = prices[ticker].dropna()

            total_return = (values.values[-1] - values.values[0])/values.values[0]
            mdd = max_drawdown(values = values)

            df[ticker]["romad"] = total_return/mdd

        df = df.transpose()["romad"].sort_values(ascending = False)

        top_tickers  = df.index[: num_tickers]
        processed_df = utils.rebuild_dataframe(raw_df = raw_df, top_tickers = top_tickers)

        return processed_df


def max_drawdown(values: pd.Series) -> float:
    roll_max           = values.cummax()
    daily_drawdown     = values/roll_max - 1.0
    max_daily_drawdown = daily_drawdown.cummin()

    max_drawdown = abs(max_daily_drawdown[-1])

    return max_drawdown


def romad_filter(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    num_tickers = parameters.get("num_tickers", None)

    romad_df = RoMAD.process(raw_df = df, num_tickers = num_tickers)

    return romad_df