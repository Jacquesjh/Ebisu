
from datetime import datetime

import pandas as pd

from athena.src.services.pipeline.pipeline import Pipeline
from athena.src.services.plotting import plots
from athena.src.utils import utils


class Backtest:


    optimizer         : dict
    filters           : dict
    rebalance_interval: str
    backtesting_years : int
    data              : pd.DataFrame
    weights           : pd.DataFrame
    assets_returns    : pd.DataFrame
    returns           : pd.DataFrame


    def __init__(self, data: pd.DataFrame, filters: dict, optimizer: dict, start_date: datetime, constraints: dict, rebalance_interval: str) -> None:
        self.optimizer   = optimizer
        self.filters     = filters
        self.constraints = constraints

        self.rebalance_interval = rebalance_interval
        self.start_date         = start_date

        self.data = data


    def _get_weights(self, dates: list) -> pd.DataFrame:
        df_weights = pd.DataFrame()

        for date in dates:
            raw_df = self.data.loc[: date]

            pipeline = Pipeline(data = raw_df, filters = self.filters, optimizer = self.optimizer, constraints = self.constraints)
            weights  = pipeline.get_weights()
            weights  = utils.remove_duplicate_columns(weights)

            df_weights = pd.concat([df_weights, weights])
        
        df_weights = df_weights.sort_index()

        return df_weights


    def _get_returns_dataframe(self, weights: pd.DataFrame) -> pd.Series:
        indexes = self.data["Close"].loc[weights.index[0]: ].index
        returns = pd.DataFrame(columns = ["returns"], index = indexes)

        for index in indexes:
            """
                The backtest buys at Open price, so this if statment is the return of the day the backtest bought.
                So in this case, I compare the Close price of day 0 to the Buy price of day 0. Outside this case,
                I compare the Close price of day 0 and the Close price of day -1.
            """
            if index in weights.index:
                current_weights = weights.loc[index].dropna()

                buy_prices = self.data["Open"][current_weights.index].loc[index]
                ref_prices = buy_prices

            close_prices  = self.data["Close"][current_weights.index].loc[index]
            asset_returns = (close_prices - ref_prices)/ref_prices

            day_return = (asset_returns*current_weights).sum()
            returns["returns"].loc[index] = day_return

            ref_prices = close_prices

        return returns["returns"].dropna()


    def backtest(self, plot_snapshot: bool = True, make_html: bool = False) -> None:
        dates = utils.get_dates(raw_df = self.data, rebalance_interval = self.rebalance_interval, start_date = self.start_date)

        weights = self._get_weights(dates = dates)
        returns = self._get_returns_dataframe(weights = weights)

        self.weights = weights
        self.returns = returns

        if plot_snapshot:
            plots.make_snapshot(returns = returns)

        if make_html:
            plots.make_html(returns = returns)