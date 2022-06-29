
from abc import ABC, abstractmethod

import pandas as pd


class Filter(ABC):


    @abstractmethod
    def process(raw_df: pd.DataFrame, num_tickers: int) -> pd.DataFrame:
        pass