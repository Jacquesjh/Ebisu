
from typing import Callable

import pandas as pd


def optimizer_table(optimizer_name: str) -> Callable:
    table = {
        "hrp": hrp,
        "ewp": ewp
    }

    return table.get(optimizer_name, None)


def ewp(df: pd.DataFrame, parameters: None) -> Callable:
    from athena.src.services.optimization.ewp import ewp_optimizer

    ewp = ewp_optimizer(df = df, parameters = parameters)

    return ewp


def hrp(df: pd.DataFrame, parameters: dict) -> Callable:
    from athena.src.services.optimization.hrp import hrp_optimizer

    hrp = hrp_optimizer(df = df, parameters = parameters)

    return hrp