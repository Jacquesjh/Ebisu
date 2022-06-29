
import pandas as pd

from athena.src.core.services.filter import Filter
from athena.src.utils import utils


class Momentum(Filter):

    """
        
            Momentum is an investment strategy which selects, for investmentment universe, the stocks whose price 
        appreciated the most during a specific period. This period can vary from 1 year, to months, and usually
        the last month is excluded from the decision, following the principle that the month-to-month assets perfomarnce
        tends to invert.

        Momentum is considered a primary stock factor (a.k.a anomaly, or smart-beta factor) affectingstock returns.
        Academic research and practitioners's experience show that Momentum has been outperformingthe stock indices
        all over the world since 1927. The top research on Momentum is summarized in a concise and digestible way 
        in the 2015 book Quantitative Momentum, written by Dr. Wesley Grey and Dr. Jack Vogel.

        In this implementation, you can choose:

            num_tickers [int]: The number of tickers that you want after applying the filter;

            months [int]: The number of months to analyse the momentum. As I said, normally you want the use an interval
                of  1 year, 6 months or 3 months. Noting that the most recent month is not included in the computation.


    """


    @staticmethod
    def process(raw_df: pd.DataFrame, num_tickers: int, months: int) -> pd.DataFrame:
        prices = raw_df["Close"]

        if num_tickers > len(prices.columns):
            num_tickers = len(prices.columns)

        if months == 1:
            momentum = prices.iloc[-1, :]/prices.iloc[-20, :]

        else:
            momentum  = prices.iloc[-20, :]/prices.iloc[-20*months, :]
    
        sorted_df = momentum.sort_values(ascending = False)

        top_tickers  = sorted_df.index[: num_tickers]
        processed_df = utils.rebuild_dataframe(raw_df = raw_df, top_tickers = top_tickers)

        return processed_df


def momentum_filter(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:            
    num_tickers = parameters.get("num_tickers", None)
    months      = parameters.get("months", None)

    momentum_df = Momentum.process(raw_df = df, num_tickers = num_tickers, months = months)

    return momentum_df