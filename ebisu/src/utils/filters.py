
from typing import Callable

import pandas as pd


def filters_table(filter_name: str) -> Callable:
    table = {
        "momentum"  : momentum,
        "volume"    : volume,
        "random"    : random,
        "min_price" : min_price,
        "max_price" : max_price,
        "romad"     : romad,
        "volatility": volatility,
        "sharpe"    : sharpe,
        "sortino"   : sortino,
    }

    return table.get(filter_name, None)


def momentum(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    from athena.src.services.filters.momentum import momentum_filter

    momentum_df = momentum_filter(df = df, parameters = parameters)

    return momentum_df


def volume(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    from athena.src.services.filters.volume import volume_filter

    volume_df = volume_filter(df = df, parameters = parameters)

    return volume_df


def random(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    from athena.src.services.filters.random import random_filter

    random_df = random_filter(df = df, parameters = parameters)
    
    return random_df


def min_price(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    from athena.src.services.filters.min_price import min_price_filter

    min_price_df = min_price_filter(df = df, parameters = parameters)

    return min_price_df


def max_price(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    from athena.src.services.filters.max_price import max_price_filter
    max_price_df = max_price_filter(df = df, parameters = parameters)

    return max_price_df


def romad(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    from athena.src.services.filters.romad import romad_filter

    romad_df = romad_filter(df = df, parameters = parameters)

    return romad_df


def volatility(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    from athena.src.services.filters.volatility import volatility_filter

    volatility_df = volatility_filter(df = df, parameters = parameters)

    return volatility_df


def sharpe(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    from athena.src.services.filters.sharpe import sharpe_filter

    sharpe_df = sharpe_filter(df = df, parameters = parameters)

    return sharpe_df


def sortino(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    from athena.src.services.filters.sortino import sortino_filter

    sortino_df = sortino_filter(df = df, parameters = parameters)

    return sortino_df