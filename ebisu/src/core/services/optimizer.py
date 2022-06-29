
from abc import ABC, abstractmethod

import pandas as pd


class Optimizer(ABC):
    

    @abstractmethod
    def __init__(self, historical_data: pd.DataFrame) -> None:
        pass


    @abstractmethod
    def get_weights(self) -> pd.DataFrame:
        pass