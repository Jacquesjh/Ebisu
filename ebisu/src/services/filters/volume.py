import pandas as pd
from athena.src.core.services.filter import Filter
from athena.src.utils import utils


class Volume(Filter):

    """

        Volume is a factor that usually is taken into consideration by investors. It simply shows
    how much of a ticker was traded during a specific interval of days, months or years. Volume indicates
    liquidity, and liquidity is essential for any investment. A bad volume (liquidity) means that is very
    difficult to sell your shares when needed. How much do you own when you have 1 trillion dollars worth
    beer in Mars? You own zero, because you can't convert your goods (shares) in money. Therefore, looking
    for tickers with high volume is always a good choice. How high depends on the situation.

    In this implementation you can tweak a few parameters:

        num_tickers [int]: The number of tickers that will be left after the filter;

        months Optional[int]: The number of months that you want the analyse the volume. It will give you
            the mean of this interval. If not specified, the algorithm will use the last 6 months.


    """

    @staticmethod
    def process(raw_df: pd.DataFrame, num_tickers: int, days: int) -> pd.DataFrame:
        volume_df = raw_df["Volume"]

        if num_tickers > len(volume_df.columns):
            num_tickers = len(volume_df.columns)

        sorted_df = volume_df.iloc[-days:].mean().sort_values(ascending=False)

        # sorted_df = volume_df.iloc[-20*months: ].mean().sort_values(ascending = False)

        top_tickers = sorted_df.index[:num_tickers]
        processed_df = utils.rebuild_dataframe(raw_df=raw_df, top_tickers=top_tickers)

        return processed_df


def volume_filter(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    num_tickers = parameters.get("num_tickers", None)
    days = parameters.get("days", None)

    volume_df = Volume.process(raw_df=df, num_tickers=num_tickers, days=days)

    return volume_df
