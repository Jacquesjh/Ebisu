
from datetime import datetime
from typing import Callable, Dict, List

import numpy as np
import pandas as pd


class Constrainer:

    """

        constraints = {
            "invest_sections": {0.15: ["VALE3.SA", "TAEE11.SA"], 0.30: ["FIXA11.SA", "IRFM11.SA"]}
            "invest_tickers": ["FIXA11.SA", "IRFM11.SA"]
        }

        Robovespa Conservador:

        constraints = {
            "invest_section": {0.75: ["FIXA11.SA", "IRFM11.SA"]}
        }


    """

    constraints: dict
    raw_df     : pd.DataFrame                   # I need the raw dataframe to pull the data of tickers that were not selected in the filters
                                                # for example, FIXA11 data was in the raw_df but not in the filtered_df, that's why I need it
    filtered_df: pd.DataFrame


    def __init__(self, raw_df: pd.DataFrame, filtered_df: pd.DataFrame,  constraints: dict) -> None:
        self.constraints = constraints
        self.raw_df      = raw_df.copy()
        self.filtered_df = filtered_df


    def _apply_constraints(self) -> dict:
        dataframes = dict()

        for constraint in self.constraints:
            constraint_function = self._constraints_table(constraint)
            dataframes = {**dataframes, **constraint_function(args = self.constraints[constraint])}

        return dataframes

    
    def _constraints_table(self, constraint: str) -> None:
        constraint_table = {
            "invest_sections": self._invest_sections,
            "invest_tickers": self._invest_tickers
        }

        return constraint_table.get(constraint, None)


    def _invest_tickers(self, args: List[str]) -> Dict[float, pd.DataFrame]:
        tickers = list(self.filtered_df["Close"].columns) + args
        tickers = list(set(tickers))

        processed_df = dict()

        for level in self.filtered_df.columns.levels[0]:
            processed_df.update({level: self.raw_df[level][tickers]})

        processed_df = pd.concat(processed_df, axis = 1)

        return {1.00: processed_df}


    def _dynamic_percentage(self, low: float, high: float) -> float:
        prices = self.filtered_df["Close"]

        lookback_return = 7
        returns = prices.pct_change().dropna(how = "all")

        return_track = (1 + returns.iloc[-lookback_return: ]).cumprod().iloc[-1].mean() - 1

        negative_returns = pd.DataFrame(np.where(returns.iloc[-20: ] < 0, returns.iloc[-20: ], 0))

        negative_volatility = negative_returns.std().mean()

        negative_volatility_cutoff = 0.04

        if negative_volatility >= negative_volatility_cutoff or return_track < 0:
            percentage = high

        else:
            percentage = low

        return percentage


    def _invest_sections(self, args: Dict[float, List[str]]) -> Dict[float, pd.DataFrame]:
        sections_dataframes = dict()

        for percentage, section in args.items():
            if type(percentage) == tuple:
                percentage = self._dynamic_percentage(low = percentage[0], high = percentage[1])

            processed_df = dict()
            section      = list(set(section))

            for level in self.raw_df.columns.levels[0]:
                processed_df.update({level: self.raw_df[level][section]})

            processed_df = pd.concat(processed_df, axis = 1)
            section_dict = {percentage: processed_df}

            sections_dataframes = {**sections_dataframes, **section_dict}

        return sections_dataframes


    def process(self) -> Dict[float, pd.DataFrame]:
        dataframes = self._apply_constraints()
        
        return dataframes


def constrained_weights(raw_df: pd.DataFrame, filtered_df: pd.DataFrame, constraints: dict, optimizer_function: Callable, parameters: dict, date: datetime) -> pd.DataFrame:
    constrainer = Constrainer(raw_df = raw_df, filtered_df = filtered_df, constraints = constraints)
    dataframes  = constrainer.process()

    percentage_left = 1.00 - sum(dataframes.keys())
    
    if percentage_left in list(dataframes.keys()):
        percentage_left += 0.01

    dataframes[percentage_left] = filtered_df

    weights = pd.DataFrame()

    for percentage, df in dataframes.items():
        optimizer    = optimizer_function(df = df, parameters = parameters)
        part_weights = optimizer.get_weights()

        part_weights.index = [date]

        weights = pd.concat([weights, percentage*part_weights], axis = 1)
    
    return weights