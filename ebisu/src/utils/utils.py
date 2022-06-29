
from typing import Callable, List

from datetime import datetime
import pandas as pd


def remove_young_tickers(df: pd.DataFrame, min_days: int) -> pd.DataFrame:
    prices = df["Close"]

    ok_tickers = list()

    for ticker in prices.columns:
        if len(prices[ticker].dropna()) >= min_days:
            ok_tickers.append(ticker)

    cleaned_df = rebuild_dataframe(raw_df = df, top_tickers = ok_tickers)
    
    return cleaned_df


def remove_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:,~df.columns.duplicated()].copy()


def split_list(my_list: list, n_parts: int) -> Callable:
    """
    https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    """
    k, m = divmod(len(my_list), n_parts)

    return (my_list[i*k + min(i, m): (i + 1)*k + min(i + 1, m)] for i in range(n_parts))


def get_dates(raw_df: pd.DataFrame, rebalance_interval: str, start_date: datetime) -> List[datetime]:
    table = {
        "daily"   : get_daily_dates,
        "weekly"  : get_weekly_dates,
        "biweekly": get_biweekly_dates,
        "monthly" : get_monthly_dates
    }

    dates = table.get(rebalance_interval)(data = raw_df, start_date = start_date)

    return dates


def get_daily_dates(data: pd.DataFrame, start_date: datetime) -> list:
    dates = pd.to_datetime(data.index[data.index > start_date])

    return dates


def get_weekly_dates(data: pd.DataFrame, start_date: datetime) -> list:
    dates = get_daily_dates(data = data, start_date = start_date)
    dates = pd.to_datetime([date for date in dates if date.weekday() == 0])
    
    return dates


def get_biweekly_dates(data: pd.DataFrame, start_date: datetime) -> list:
    dates = get_weekly_dates(data = data, start_date = start_date)
    dates = dates[:: 2]                                                         # deletes every other date

    return dates


def get_monthly_dates(data: pd.DataFrame, start_date: datetime) -> list:
    dates = get_biweekly_dates(data = data, start_date = start_date)
    dates = dates[:: 2]

    return dates


def validate_rebalance_intervals(interval: str) -> None:
    valid_rebalance_intervals = ["daily", "weekly", "biweekly", "monthly"]

    if interval not in valid_rebalance_intervals:
        raise ValueError(f"The given rebalance interval {interval} is not valid. Must be one of {valid_rebalance_intervals}.")


def validate_domain_sectors(sectors: List[str]) -> None:
    valid_sectors = ["Servicos Comerciais", "Comunicacoes", "Consumiveis Duraveis", "Consumiveis nao Duraveis",
                     "Consumo de Servicos", "Sevicos de Logistica", "Tecnologia Eletronica", "Mineirais Energeticos",
                     "Financeiro", "Servicos de Saude", "Tecnologia em Saude", "Servicos Industriais", "Minerais nao Energeticos",
                     "Industrias de Processamento", "Produtor Manufatureiro", "Varejo", "Servico de Tecnologia", "Transporte", "Servico Publico"]

    for sector in sectors:
        if sector not in valid_sectors:
            raise ValueError(f"The given sector {sector} is not valid. Must be one of {valid_sectors}.")


def validate_domains(domains: List[str]) -> None:
        valid_domains = ["stocks", "bdrs", "variable etfs", "fixed etfs", "fiis"]

        for domain in domains:
            if domain not in valid_domains:
                raise ValueError(f"The domain {domain} is not valid, must be one of {valid_domains}.")


def rebuild_dataframe(raw_df: pd.DataFrame, top_tickers: List[str]) -> pd.DataFrame:
    processed_df = dict()

    for level in raw_df.columns.levels[0]:
        processed_df.update({level: raw_df[level][top_tickers]})

    return pd.concat(processed_df, axis = 1)
