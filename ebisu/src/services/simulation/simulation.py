
from datetime import datetime
import multiprocessing

import numpy as np
import pandas as pd
import ray

from athena.src.services.backtest.backtest import Backtest
from athena.src.services.simulation.random_stuff import get_random_strategy
from athena.src.utils.metrics import metrics_df
from athena.src.utils import utils


class Simulation:


    def __init__(self, portfolio_size: int, min_num_filters: int, max_num_filters: int, constraints: dict, rebalance_interval: str) -> None:
        ray.init(ignore_reinit_error = True)

        self.num_workers        = multiprocessing.cpu_count()
        self.constraints        = constraints
        self.min_num_filters    = min_num_filters
        self.portfolio_size     = portfolio_size
        self.max_num_filters    = max_num_filters
        self.rebalance_interval = rebalance_interval


    def run_universe(self, data: pd.DataFrame, start_date: datetime, num_possibilities: int) -> pd.DataFrame:
        metrics = pd.DataFrame()

        self.get_many_strategies(data = data, num_strategies = num_possibilities)

        strategies = self.strategies

        index_strategies      = list(strategies.keys())
        strategies_per_worker = list(utils.split_list(my_list = index_strategies, n_parts = self.num_workers))

        future_dfs = []

        for _worker in range(self.num_workers):
            dfs = run_partial_universe.remote(indexes = strategies_per_worker[_worker], strategies = strategies, data = data, start_date = start_date, rebalance_interval = self.rebalance_interval)

            future_dfs.append(dfs)

        dfs = [ray.get(df) for df in future_dfs]

        for df in dfs:
            metrics = pd.concat([metrics, df], axis = 1)

        return metrics


    def get_many_strategies(self, data: pd.DataFrame, num_strategies: int) -> None:
        strategies  = dict()
        num_tickers = len(data.columns.levels[1])

        for i in range(num_strategies):
            strategy = get_strategy(num_tickers = num_tickers, min_num_filters = self.min_num_filters, max_num_filters = self.max_num_filters, portfolio_size = self.portfolio_size, constraints = self.constraints)

            strategies.update({i: strategy})

        self.strategies = strategies


def get_strategy(num_tickers: int, min_num_filters: int, max_num_filters: int, portfolio_size: int, constraints: dict) -> dict:
    total_tickers  = num_tickers
    num_filters    = np.random.randint(min_num_filters, max_num_filters + 1)
    portfolio_size = portfolio_size

    strategy = get_random_strategy(total_tickers = total_tickers, num_filters = num_filters, portfolio_size = portfolio_size)
    strategy["constraints"] = constraints

    return strategy


def backtest_strategy(data: pd.DataFrame, strategy: dict, start_date: datetime, rebalance_interval: str) -> pd.DataFrame:
    backtest = Backtest(data = data, filters = strategy["filters"], optimizer = strategy["optimizer"],
                        start_date = start_date, constraints = strategy["constraints"], rebalance_interval = rebalance_interval)
    
    backtest.backtest(plot_snapshot = False)

    df_returns = backtest.returns

    return df_returns


@ray.remote
def run_partial_universe(indexes: list, strategies: dict, data: pd.DataFrame, start_date: datetime, rebalance_interval: str) -> pd.DataFrame:
    metrics = pd.DataFrame()

    for index in indexes:
        strategy = strategies.get(index)
        returns  = backtest_strategy(data = data, strategy = strategy, start_data = start_date, rebalance_interval = rebalance_interval)

        df = metrics_df(returns = returns)
        df.columns = [index]

        metrics = pd.concat([metrics, df], axis = 1)

    return metrics