from typing import Callable, Dict, Optional

import numpy as np
import pandas as pd
from athena.src.utils import utils
from athena.src.utils.filters import filters_table
from athena.src.utils.optimizers import optimizer_table


class Pipeline:
    constraints: Optional[dict]
    optimizer: Dict[str, dict]
    filters: Dict[str, dict]
    data: pd.DataFrame
    raw_data: pd.DataFrame

    def __init__(
        self,
        data: pd.DataFrame,
        filters: Dict[str, dict],
        optimizer: Dict[str, dict],
        constraints: Optional[dict] = None,
    ) -> None:
        self.optimizer = optimizer
        self.filters = filters
        self.constraints = constraints
        self.date = data.index[-1]

        self.data = self._clean_data(df=data.iloc[-252 * 2 : -1])
        self.raw_data = self.data.copy()

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = utils.remove_young_tickers(df=df, min_days=120)

        return df

    def _apply_filters(self) -> None:
        for filter_name in self.filters:
            proper_filter_name = filter_name.split("->")[0]
            filter_function = filters_table(filter_name=proper_filter_name.lower())

            self.data = filter_function(
                df=self.data, parameters=self.filters.get(filter_name)
            )

    def _constrained_weights(
        self, optimizer_function: Callable, parameters: dict
    ) -> pd.DataFrame:
        from athena.src.services.constrainer.constrainer import \
            constrained_weights

        weights = constrained_weights(
            raw_df=self.raw_data,
            filtered_df=self.data,
            constraints=self.constraints,
            optimizer_function=optimizer_function,
            parameters=parameters,
            date=self.date,
        )

        return weights

    def _unconstrained_weights(
        self, optimizer_function: Callable, parameters: dict
    ) -> pd.DataFrame:
        optimizer = optimizer_function(df=self.data, parameters=parameters)
        weights = optimizer.get_weights()
        weights.index = [self.date]

        return weights

    def get_weights(self) -> pd.DataFrame:
        if self.filters:
            self._apply_filters()

        opt_name, parameters = (
            list(self.optimizer.keys())[0],
            list(self.optimizer.values())[0],
        )
        optimizer_function = optimizer_table(optimizer_name=opt_name.lower())

        constraints = {
            True: self._unconstrained_weights,
            False: self._constrained_weights,
        }

        weights = constraints[self.constraints is None](
            optimizer_function=optimizer_function, parameters=parameters
        )
        weights = weights.replace(0, np.nan).dropna(axis=1, how="all")

        return weights

    def get_allocations(self, cash: float = 20000) -> pd.DataFrame:
        weights = self.get_weights()
        money = weights * cash

        latest_prices = self.data["Close"][money.columns].iloc[-1]

        allocations = np.round(money / latest_prices)
        allocations = allocations.astype(int)

        return allocations
