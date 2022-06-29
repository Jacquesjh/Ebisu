
import pandas as pd

from athena.src.core.services.filter import Filter


class MACD(Filter):

    """
        TODO  Figure out how to implement properly

        PROBLEM: this will tell the pipeline only the point of entr/exit, when the point passes it will get out



    """


    @staticmethod
    def process(raw_df: pd.DataFrame, short_span: int, long_span: int) -> pd.DataFrame:
        exp_short = raw_df["Close"].ewm(short_span).mean()
        exp_long  = raw_df["Close"].ewm(long_span).mean()

        macd = exp_short - exp_long
        macd = macd/raw_df["Close"]
        
        top_tickers = []

        for ticker in macd.columns:
            value = macd[ticker].iloc[-1]
            slope = value - macd[ticker].iloc[-2]

            if value > 0 and slope > 0:
                top_tickers.append(ticker)

        processed_df = dict()

        for level in raw_df.columns.levels[0]:
            processed_df.update({level: raw_df[level][top_tickers]})

        return pd.concat(processed_df, axis = 1)